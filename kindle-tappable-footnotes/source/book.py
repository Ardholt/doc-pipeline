"""Source parsing, EPUB packaging and independent document inspection."""
import copy, hashlib, json, re, subprocess, zipfile
from pathlib import Path
from lxml import etree, html

NS={'x':'http://www.w3.org/1999/xhtml','epub':'http://www.idpf.org/2007/ops','opf':'http://www.idpf.org/2007/opf'}
EPUB='{'+NS['epub']+'}'
def run(args):
    return subprocess.check_output(args,text=True,stderr=subprocess.PIPE,timeout=120)
def norm(s): return ' '.join(s.split())
def digest(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def dump(p,obj): p.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
def render(ast,blocks):
    value=dict(ast,blocks=blocks,meta={})
    p=subprocess.run(['pandoc','-f','json','-t','html5','--wrap=none'],input=json.dumps(value),text=True,capture_output=True,timeout=60)
    if p.returncode: raise ValueError('Pandoc HTML conversion failed: '+p.stderr)
    root=html.fragment_fromstring(p.stdout,create_parent='div')
    return ''.join(etree.tostring(c,encoding='unicode',method='xml') for c in root)
def visible(fragment): return norm(html.fragment_fromstring(fragment,create_parent='div').text_content())
def load(inp):
    for filename in ['book.json','manuscript.md']:
        if not (inp/filename).is_file(): raise ValueError('missing required input: '+filename)
    meta=json.loads((inp/'book.json').read_text())
    if not isinstance(meta,dict): raise ValueError('book.json must be an object')
    if type(meta.get('schema_version')) is not int or meta['schema_version']!=1: raise ValueError('book.json schema_version must be the integer 1')
    for key in ['title','language','identifier']:
        if not isinstance(meta.get(key),str) or not meta[key].strip(): raise ValueError('book.json '+key+' must be a nonempty string')
    if not re.fullmatch(r'[A-Za-z]{2,8}(?:-[A-Za-z0-9]{1,8})*',meta['language']): raise ValueError('book.json language must be a language tag')
    raw=(inp/'manuscript.md').read_text()
    if not raw.strip(): raise ValueError('manuscript.md must not be empty')
    # Diagnose undefined or unused references before Pandoc can leave literal markup.
    defs=re.findall(r'^\[\^([^\]]+)\]:',raw,re.M)
    refs=re.findall(r'(?<!\\)\[\^([^\]]+)\](?!:)',raw)
    if len(defs)!=len(set(defs)): raise ValueError('duplicate footnote definition')
    if set(refs)!=set(defs): raise ValueError('footnote definitions and references must match')
    ast=json.loads(run(['pandoc','-f','markdown-smart','-t','json',str(inp/'manuscript.md')]))
    notes=[]; audit=[]; keys={}
    def walk(obj):
        if isinstance(obj,list): return [walk(x) for x in obj]
        if not isinstance(obj,dict): return obj
        kind=obj.get('t')
        if kind in ['RawBlock','RawInline','Image','Math','Table','Cite']:
            raise ValueError('unsupported manuscript element: '+kind+'; use text, headings, lists, quotes and footnotes')
        if kind=='Link': raise ValueError('external and authored hyperlinks are outside this input boundary')
        if kind=='Note':
            key=json.dumps(obj['c'],sort_keys=True)
            if key not in keys:
                keys[key]=len(notes)+1
                notes.append(copy.deepcopy(obj['c']))
            n=keys[key]; r=len(audit)+1
            audit.append({'reference_id':f'ref-{r}','note_id':f'note-{n}','forward':f'notes.xhtml#note-{n}','return':f'chapter.xhtml#ref-{r}','number':n})
            return {'t':'RawInline','c':['html',f'<a id="ref-{r}" href="notes.xhtml#note-{n}" epub:type="noteref" role="doc-noteref" aria-label="Note {n}"><sup>{n}</sup></a>']}
        return {k:walk(v) for k,v in obj.items()}
    converted=walk(copy.deepcopy(ast))
    # Validate note contents through the same supported-element walk without changing note references.
    for n in notes:
        if any(x in json.dumps(n) for x in ['"Note"','"RawBlock"','"RawInline"','"Image"','"Link"','"Math"','"Table"','"Cite"']): raise ValueError('unsupported content within a footnote')
    if not audit: raise ValueError('manuscript.md must contain footnotes')
    body=render(converted,converted['blocks'])
    note_html=[render(ast,n) for n in notes]
    clean=html.fragment_fromstring(body,create_parent='div')
    for a in clean.xpath('.//a'):
        a.drop_tree()
    mapping={'schema_version':1,'normalization':'Collapse Unicode whitespace to one space; remove generated note markers, note headings and return labels. Punctuation, case and Unicode are retained. Identical note bodies share one destination.','body_text':norm(clean.text_content()),'structure':[{'tag':e.tag,'text':norm(e.text_content())} for e in clean.iter() if e.tag in ['h1','h2','h3','h4','h5','h6','ul','ol','li','blockquote','strong','em','pre','code']],'notes':[{'id':f'note-{i+1}','text':visible(v)} for i,v in enumerate(note_html)],'references':audit}
    return meta,body,note_html,mapping

def xhtml(title,body,lang):
    from html import escape
    return f'<?xml version="1.0" encoding="UTF-8"?><html xmlns="{NS["x"]}" xmlns:epub="{NS["epub"]}" lang="{escape(lang)}" xml:lang="{escape(lang)}"><head><title>{escape(title)}</title><link rel="stylesheet" href="style.css"/></head><body>{body}</body></html>'

def build(inp,out):
    from html import escape
    meta,body,notes,mapping=load(inp)
    note_body='<h1>Notes</h1>'
    for i,n in enumerate(notes,1):
        refs=[r for r in mapping['references'] if r['number']==i]
        returns=' '.join(f'<a class="return" href="{r["return"]}">Return to passage {r["reference_id"].split("-")[1]}</a>' for r in refs)
        note_body+=f'<aside id="note-{i}" epub:type="footnote" role="doc-footnote"><h2>Note {i}</h2><div class="note-text">{n}</div><p class="returns">{returns}</p></aside>'
    root=html.fragment_fromstring(body,create_parent='div')
    headings=[(h.get('id'),norm(h.text_content())) for h in root.xpath('.//h1|.//h2|.//h3|.//h4|.//h5|.//h6')]
    nav='<nav epub:type="toc" id="toc"><h1>Contents</h1><ol>'+''.join(f'<li><a href="chapter.xhtml#{escape(i)}">{escape(t)}</a></li>' for i,t in headings)+'<li><a href="notes.xhtml">Notes</a></li></ol></nav>'
    manifest='<item id="chapter" href="chapter.xhtml" media-type="application/xhtml+xml"/><item id="notes" href="notes.xhtml" media-type="application/xhtml+xml"/><item id="nav" href="nav.xhtml" media-type="application/xhtml+xml" properties="nav"/><item id="css" href="style.css" media-type="text/css"/>'
    opf=f'''<?xml version="1.0" encoding="utf-8"?><package xmlns="{NS['opf']}" version="3.0" unique-identifier="book-id" xml:lang="{escape(meta['language'])}"><metadata xmlns:dc="http://purl.org/dc/elements/1.1/"><dc:identifier id="book-id">{escape(meta['identifier'])}</dc:identifier><dc:title>{escape(meta['title'])}</dc:title><dc:language>{escape(meta['language'])}</dc:language><meta property="dcterms:modified">2026-01-01T00:00:00Z</meta></metadata><manifest>{manifest}</manifest><spine><itemref idref="chapter"/><itemref idref="notes"/></spine></package>'''
    files={'mimetype':'application/epub+zip','META-INF/container.xml':'<?xml version="1.0"?><container xmlns="urn:oasis:names:tc:opendocument:xmlns:container" version="1.0"><rootfiles><rootfile full-path="EPUB/package.opf" media-type="application/oebps-package+xml"/></rootfiles></container>','EPUB/package.opf':opf,'EPUB/chapter.xhtml':xhtml(meta['title'],body,meta['language']),'EPUB/notes.xhtml':xhtml('Notes',note_body,meta['language']),'EPUB/nav.xhtml':xhtml('Contents',nav,meta['language']),'EPUB/style.css':(Path(__file__).parent/'book.css').read_text()}
    with zipfile.ZipFile(out/'book.epub','w') as z:
        for name,content in files.items():
            info=zipfile.ZipInfo(name,(2026,1,1,0,0,0)); info.compress_type=zipfile.ZIP_STORED if name=='mimetype' else zipfile.ZIP_DEFLATED
            z.writestr(info,content.encode())
    dump(out/'source-map.json',mapping)
    return mapping

def inspect(inp,epub):
    meta,_,_,expected=load(inp)
    with zipfile.ZipFile(epub) as z:
        assert z.namelist()[0]=='mimetype' and z.getinfo('mimetype').compress_type==0,'EPUB mimetype must be first and stored'
        assert z.read('mimetype')==b'application/epub+zip','invalid mimetype'
        assert len(z.namelist())==len(set(z.namelist())),'duplicate archive path'
        assert set(z.namelist())=={'mimetype','META-INF/container.xml','EPUB/package.opf','EPUB/chapter.xhtml','EPUB/notes.xhtml','EPUB/nav.xhtml','EPUB/style.css'},'unexpected archive resource'
        docs={name:etree.fromstring(z.read('EPUB/'+name)) for name in ['chapter.xhtml','notes.xhtml','nav.xhtml','package.opf']}
    opf=docs['package.opf']; assert opf.get('version')=='3.0','not EPUB 3'
    assert opf.xpath('//opf:spine/opf:itemref/@idref',namespaces=NS)==['chapter','notes'],'wrong reading order'
    dc={'dc':'http://purl.org/dc/elements/1.1/'}
    for key in ['title','language','identifier']: assert opf.xpath('string(//dc:'+key+')',namespaces=dc)==meta[key],'metadata mismatch'
    assert len(opf.find('{'+NS['opf']+'}metadata'))==4,'unexpected metadata'
    for name,doc in docs.items():
        ids=doc.xpath('//@id'); assert len(ids)==len(set(ids)),'duplicate IDs in '+name
        assert not doc.xpath('//comment()|//x:script|//x:iframe',namespaces=NS),'unexpected embedded content'
    for name in ['chapter.xhtml','notes.xhtml','nav.xhtml']:
        for a in docs[name].xpath('//x:a',namespaces=NS):
            href=a.get('href',''); file,_,frag=href.partition('#')
            assert file in docs,'unresolved link '+href
            if frag: assert len(docs[file].xpath('//*[@id=$v]',v=frag))==1,'missing destination '+href
    chapter=docs['chapter.xhtml']; notes=docs['notes.xhtml']
    refs=chapter.xpath('//x:a[@epub:type="noteref"]',namespaces=NS)
    assert len(refs)==len(expected['references']),'reference count mismatch'
    for r,a in zip(expected['references'],refs):
        assert a.get('id')==r['reference_id'] and a.get('href')==r['forward'],'forward destination mismatch'
        assert a.get('role')=='doc-noteref','missing noteref role'
        note=notes.xpath('//*[@id=$v]',v=r['note_id'])[0]
        assert note.get(EPUB+'type')=='footnote' and note.get('role')=='doc-footnote','missing footnote semantics'
        assert len(note.xpath('.//x:a[@href=$v]',namespaces=NS,v=r['return']))==1,'return destination mismatch'
    assert len(notes.xpath('//x:a',namespaces=NS))==len(refs),'unexpected return links'
    for a in refs:
        tail=a.tail or ''; parent=a.getparent(); previous=a.getprevious()
        if previous is not None: previous.tail=(previous.tail or '')+tail
        else: parent.text=(parent.text or '')+tail
        parent.remove(a)
    body=chapter.find('{'+NS['x']+'}body')
    assert norm(''.join(body.itertext()))==expected['body_text'],'manuscript text differs'
    structure=[{'tag':etree.QName(e).localname,'text':norm(''.join(e.itertext()))} for e in body.iter() if etree.QName(e).localname in ['h1','h2','h3','h4','h5','h6','ul','ol','li','blockquote','strong','em','pre','code']]
    assert structure==expected['structure'],'heading, list or emphasis structure differs'
    note_text=notes.xpath('//x:div[@class="note-text"]',namespaces=NS)
    assert len(note_text)==len(expected['notes']),'note count mismatch'
    for actual,wanted in zip(note_text,expected['notes']): assert norm(''.join(actual.itertext()))==wanted['text'],'note text differs'
    return expected
