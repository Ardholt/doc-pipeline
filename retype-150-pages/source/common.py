"""Shared serialization, document inspection and exact text metrics."""
import hashlib, json, re, subprocess, zipfile
from pathlib import Path
from xml.etree import ElementTree as ET

NS={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}

def sha(path):
    h=hashlib.sha256()
    with Path(path).open('rb') as f:
        for block in iter(lambda:f.read(1024*1024),b''): h.update(block)
    return h.hexdigest()

def write_json(path, data):
    Path(path).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')

def run(args, timeout=180):
    r=subprocess.run([str(a) for a in args],capture_output=True,text=True,timeout=timeout)
    if r.returncode: raise ValueError(f'{Path(str(args[0])).name} failed (exit {r.returncode}): {r.stderr[-500:]}')
    return r.stdout

def normalized(s):
    return ' '.join(s.split())

def block_text(blocks):
    return '\n\n'.join('\n'.join('\t'.join(r) for r in b['rows']) if b['kind']=='table' else b['text'] for b in blocks)

def distance(a,b):
    """Exact unit-cost Levenshtein using a bit-vector; accepts strings or tokens."""
    if not a:return len(b)
    peq={}
    for i,c in enumerate(a):peq[c]=peq.get(c,0)|(1<<i)
    pv=~0; mv=0; score=len(a); last=1<<(len(a)-1)
    for c in b:
        eq=peq.get(c,0); xv=eq|mv; xh=(((eq&pv)+pv)^pv)|eq
        ph=mv|~(xh|pv); mh=pv&xh
        if ph&last:score+=1
        if mh&last:score-=1
        ph=(ph<<1)|1; mh<<=1
        pv=mh|~(xv|ph); mv=ph&xv
    return score

def metric(reference, actual):
    a=normalized(reference); b=normalized(actual)
    chars=len(a); words=len(a.split())
    ce=distance(a,b); we=distance(a.split(),b.split())
    return {'reference_characters':chars,'character_edits':ce,'character_accuracy_percent':round(100*(1-ce/chars),6) if chars else None,
            'reference_words':words,'word_edits':we,'word_accuracy_percent':round(100*(1-we/words),6) if words else None}

def aggregate(items):
    d={k:sum(i[k] for i in items) for k in ('reference_characters','character_edits','reference_words','word_edits')}
    d['character_accuracy_percent']=round(100*(1-d['character_edits']/d['reference_characters']),6)
    d['word_accuracy_percent']=round(100*(1-d['word_edits']/d['reference_words']),6)
    return d

def paragraph_text(node):
    pieces=[]
    for child in node.iter():
        if child.tag=='{'+NS['w']+'}t':pieces.append(child.text or '')
        elif child.tag=='{'+NS['w']+'}tab':pieces.append('\t')
        elif child.tag in ('{'+NS['w']+'}br','{'+NS['w']+'}cr'):pieces.append('\n')
    return ''.join(pieces)


def docx_pages(path):
    with zipfile.ZipFile(path) as z:
        root=ET.fromstring(z.read('word/document.xml'))
    result=[]; current=None
    for node in root.find('w:body',NS):
        tag=node.tag.split('}')[-1]
        if tag=='p':
            marks=node.findall('w:bookmarkStart',NS)
            names=[m.get('{'+NS['w']+'}name','') for m in marks]
            ids=[n for n in names if re.fullmatch(r'source_page_\d+',n)]
            if ids:
                current={'page':int(ids[0].rsplit('_',1)[1]),'blocks':[]}; result.append(current)
            text=paragraph_text(node)
            if text:
                if current is None: raise ValueError('DOCX text before first source-page bookmark')
                style=node.find('w:pPr/w:pStyle',NS)
                kind='heading' if style is not None and style.get('{'+NS['w']+'}val','').startswith('Heading') else 'paragraph'
                current['blocks'].append({'kind':kind,'text':text})
        elif tag=='tbl':
            if current is None: raise ValueError('DOCX table outside source mapping')
            rows=[['\n'.join(paragraph_text(p) for p in c.findall('w:p',NS)) for c in r.findall('w:tc',NS)] for r in node.findall('w:tr',NS)]
            current['blocks'].append({'kind':'table','rows':rows})
    for p in result:p['text']=block_text(p['blocks'])
    return result

def strip_docx(path):
    from lxml import etree as XML
    relns='http://schemas.openxmlformats.org/package/2006/relationships'
    ctns='http://schemas.openxmlformats.org/package/2006/content-types'
    temp=Path(path).with_suffix('.clean.docx')
    with zipfile.ZipFile(path) as src, zipfile.ZipFile(temp,'w',zipfile.ZIP_DEFLATED) as dst:
        for n in sorted(src.namelist()):
            if n.startswith(('docProps/','customXml/')):continue
            data=src.read(n)
            if n.endswith('.rels'):
                root=XML.fromstring(data)
                for child in list(root):
                    if child.get('Target','').startswith(('docProps/','../customXml/')):root.remove(child)
                data=XML.tostring(root,encoding='utf-8',xml_declaration=True)
            if n=='[Content_Types].xml':
                root=XML.fromstring(data)
                for child in list(root):
                    if child.get('PartName','').startswith(('/docProps/','/customXml/')):root.remove(child)
                data=XML.tostring(root,encoding='utf-8',xml_declaration=True)
            info=zipfile.ZipInfo(n,(2020,1,1,0,0,0)); info.compress_type=zipfile.ZIP_DEFLATED
            dst.writestr(info,data)
    temp.replace(path)

def strip_pdf(src,dst):
    from pypdf import PdfReader,PdfWriter
    reader=PdfReader(src); writer=PdfWriter()
    for p in reader.pages:
        for k in ('/Metadata','/Annots','/PieceInfo'):
            if k in p:del p[k]
        writer.add_page(p)
    writer._info=None
    with Path(dst).open('wb') as f:writer.write(f)
