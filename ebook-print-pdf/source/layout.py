"""Validate the public inputs and turn the Pandoc tree into paged HTML."""
import html, json, math, re, subprocess, unicodedata
from pathlib import Path
from urllib.parse import urlparse
from bs4 import BeautifulSoup


def norm(text):
    return re.sub(r'\s+', '', unicodedata.normalize('NFKC', text).replace('\u00ad', ''))


def load_input(root):
    root = Path(root)
    for name in ('print.json', 'manuscript.md'):
        if not (root / name).is_file():
            raise ValueError('missing required input: ' + name)
    for p in root.rglob('*'):
        if p.is_symlink():
            raise ValueError('input symlinks are not supported')
    cfg = json.loads((root / 'print.json').read_text())
    if not isinstance(cfg,dict):
        raise ValueError('print.json: expected a JSON object')
    if type(cfg.get('schema_version')) is not int or cfg['schema_version'] != 1:
        raise ValueError('print.json: schema_version must be 1')
    if not isinstance(cfg.get('title'), str) or not cfg['title'].strip():
        raise ValueError('print.json: title must be nonempty text')
    for key, low, high in [('trim_width_mm',120,220), ('trim_height_mm',180,300),
                           ('bleed_mm',0,3), ('margin_mm',15,25), ('body_pt',9,16)]:
        v = cfg.get(key)
        if isinstance(v,bool) or not isinstance(v,(int,float)) or not math.isfinite(v) or not low <= v <= high:
            raise ValueError(f'print.json: {key} must be a number in {low}–{high}')
    if cfg['trim_width_mm']-2*cfg['margin_mm'] < cfg['body_pt']*0.35278*10:
        raise ValueError('print.json: impossible geometry; fewer than ten body ems fit between margins')
    md = (root / 'manuscript.md').read_text()
    if not md.strip():
        raise ValueError('manuscript.md is empty')
    ast = json.loads(subprocess.check_output(['pandoc',str(root/'manuscript.md'),'-f','markdown','-t','json'], timeout=60))
    if ast.get('meta'):
        raise ValueError('use print.json for metadata; manuscript YAML metadata is not supported')
    if not any(b['t']=='Header' and b['c'][0]==1 for b in ast['blocks']):
        raise ValueError('manuscript.md needs at least one level-one chapter heading')
    return cfg, ast


class Renderer:
    def __init__(self, root):
        self.root = Path(root)
        self.records = []
        self.notes = []
        self.links = []
        self.assets = []
        self.chapter = 0
        self.headings = []

    def inlines(self, nodes):
        out = []
        for n in nodes:
            t,c = n['t'], n.get('c')
            if t=='Str': out.append(html.escape(c))
            elif t in ('Space','SoftBreak'): out.append(' ')
            elif t=='LineBreak': out.append('<br>')
            elif t in ('Emph','Strong','Strikeout','Superscript','Subscript','SmallCaps'):
                tag={'Emph':'em','Strong':'strong','Strikeout':'s','Superscript':'sup','Subscript':'sub','SmallCaps':'span'}[t]
                out.append(f'<{tag}>'+self.inlines(c)+f'</{tag}>')
            elif t=='Code': out.append('<code>'+html.escape(c[1])+'</code>')
            elif t=='Quoted':
                a,b = ('“','”') if c[0]['t']=='DoubleQuote' else ('‘','’')
                out.append(a+self.inlines(c[1])+b)
            elif t=='Note':
                number=len(self.notes)+1
                self.notes.append({'number':number,'text':''})
                note=self.blocks(c, note=True)
                plain=BeautifulSoup(note,'html.parser').get_text(' ',strip=True)
                self.notes[number-1]['text']=plain
                out.append(f'<span class="footnote" id="note-{number}">{note}</span>')
            elif t=='Link':
                target=c[2][0]
                if not (target.startswith('#') or urlparse(target).scheme in ('https','http')):
                    raise ValueError('links must be fragment links or HTTP(S) links')
                self.links.append(target)
                out.append('<a href="'+html.escape(target,quote=True)+'">'+self.inlines(c[1])+'</a>')
            elif t=='Image':
                src=c[2][0]
                asset=(self.root/src).resolve()
                if not asset.is_relative_to(self.root.resolve()) or not asset.is_file() or asset.suffix.lower()!='.svg':
                    raise ValueError('illustrations must be local SVG files inside input')
                svg=asset.read_text()
                if re.search(r'<\s*(script|foreignObject)|(?:href\s*=)|(?:url\s*\()|<!ENTITY|<!DOCTYPE',svg,re.I):
                    raise ValueError('SVG must be self-contained, without scripts or resource references')
                self.assets.append(src)
                caption=self.inlines(c[1])
                out.append('<figure><img src="'+html.escape(asset.as_uri(),quote=True)+'" alt="'+html.escape(BeautifulSoup(caption,'html.parser').get_text(),quote=True)+'"><figcaption>'+caption+'</figcaption></figure>')
            elif t=='Span': out.append(self.inlines(c[1]))
            else: raise ValueError('unsupported Markdown inline type: '+t)
        return ''.join(out)

    def record(self, fragment, kind):
        soup=BeautifulSoup(fragment,'html.parser')
        for node in soup.select('.footnote'):
            node.replace_with('\ue000'+node['id'].split('-')[-1]+'\ue001')
        marked=soup.get_text(' ',strip=True)
        parts=[{'note':int(p[1:-1])} if p.startswith('\ue000') else {'text':p} for p in re.split(r'(\ue000[0-9]+\ue001)',marked)]
        text=re.sub(r'\ue000[0-9]+\ue001','',marked)
        if text:
            self.records.append({'id':f'b{len(self.records)+1:04d}','kind':kind,'chapter':self.chapter,'text':text,'parts':parts})

    def blocks(self, nodes, note=False):
        out=[]
        for n in nodes:
            t,c=n['t'],n.get('c')
            if t in ('Para','Plain'):
                fragment=self.inlines(c)
                if not note: self.record(fragment,'paragraph')
                if '<figure>' in fragment: out.append(fragment)
                else: out.append(('<span>' if note else '<p>')+fragment+('</span> ' if note else '</p>'))
            elif t=='Header':
                level,attr,inline=c
                if level==1: self.chapter+=1
                fragment=self.inlines(inline)
                self.record(fragment,'heading')
                identifier=attr[0]
                self.headings.append({'level':level,'id':identifier,'text':BeautifulSoup(fragment,'html.parser').get_text(),'chapter':self.chapter})
                out.append(f'<h{level} id="{html.escape(identifier,quote=True)}">{fragment}</h{level}>')
            elif t=='BlockQuote': out.append('<blockquote>'+self.blocks(c,note)+'</blockquote>')
            elif t in ('BulletList','OrderedList'):
                tag='ul' if t=='BulletList' else 'ol'
                items=c if t=='BulletList' else c[1]
                attr='' if t=='BulletList' else f' start="{c[0][0]}"'
                out.append(f'<{tag}{attr}>'+''.join('<li>'+self.blocks(item,note)+'</li>' for item in items)+f'</{tag}>')
            elif t=='HorizontalRule': out.append('<hr>')
            elif t=='CodeBlock':
                fragment=html.escape(c[1]); self.record(fragment,'code')
                out.append('<pre>'+fragment+'</pre>')
            elif t=='Div': out.append(self.blocks(c[1],note))
            elif t=='Null': pass
            else: raise ValueError('unsupported Markdown block type: '+t)
        return ''.join(out)


def make_html(cfg, ast, root):
    r=Renderer(root)
    body=r.blocks(ast['blocks'])
    if r.chapter==0: raise ValueError('no chapters found')
    w,h,b,m,pt=[cfg[k] for k in ('trim_width_mm','trim_height_mm','bleed_mm','margin_mm','body_pt')]
    title=html.escape(cfg['title'])
    subtitle=html.escape(cfg.get('subtitle','')).replace('\n','<br>') if isinstance(cfg.get('subtitle',''),str) else ''
    css=f'''
@font-face {{font-family:Book;src:url(file:///usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf)}}
@font-face {{font-family:Book;src:url(file:///usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf);font-weight:bold}}
@font-face {{font-family:Book;src:url(file:///usr/share/fonts/truetype/dejavu/DejaVuSerif-Italic.ttf);font-style:italic}}
@font-face {{font-family:Label;src:url(file:///usr/share/fonts/truetype/dejavu/DejaVuSans.ttf)}}
@page {{size:{w+2*b}mm {h+2*b}mm;margin:{m+b+10}mm {m+b}mm;
 @top-center {{content:string(chapter);font:8pt Label;vertical-align:bottom;padding-bottom:4mm}}
 @bottom-center {{content:counter(page);font:9pt Book;vertical-align:top;padding-top:4mm}}
 @footnote {{border-top:0.4pt solid #777;padding-top:2.5mm;margin-top:3mm}}
}}
@page :left {{@top-center {{content:string(book)}}}}
@page :blank {{@top-center {{content:none}} @bottom-center {{content:none}}}}
@page title {{@top-center {{content:none}} @bottom-center {{content:none}}}}
@page opening {{@top-center {{content:none}}}}
html {{font-family:Book;color:#191919;font-size:{pt}pt;line-height:1.43}}
body {{margin:0}}
.title {{page:title;break-after:page;padding-top:35mm}}
.book-title {{font-size:29pt;line-height:1.2;font-weight:normal;string-set:book content()}}
.subtitle {{font:10pt Label;margin-top:12mm;line-height:1.6}}
.contents {{page:title;break-after:page}}
.contents h2 {{font:18pt Book;margin:12mm 0}}
.contents a {{display:block;font-size:10pt;line-height:1.5;margin-bottom:4mm}}
.contents a::after {{content:leader('.') target-counter(attr(href),page)}}
h1 {{break-before:right;string-set:chapter content();font:normal 24pt/1.2 Book;margin:16mm 0 10mm;break-after:avoid}}
h2 {{font:normal 14pt/1.3 Book;margin:7mm 0 3mm;break-after:avoid}}
h3,h4,h5,h6 {{font-size:12pt;break-after:avoid}}
p {{margin:0 0 3mm;text-align:justify;hyphens:none;orphans:3;widows:3}}
h1+p {{text-indent:0}}
p+p {{text-indent:4mm}}
ul,ol {{padding-left:7mm;margin:3mm 0 5mm}}
li p {{text-align:left;margin-bottom:1mm;text-indent:0}}
blockquote {{font-style:italic;margin:5mm 6mm;border-left:0.7pt solid #888;padding-left:4mm}}
blockquote p {{text-align:left}}
a {{color:inherit;text-decoration:none}}
.footnote {{float:footnote;footnote-display:block;font-size:{pt*0.78}pt;line-height:1.3;text-indent:0}}
::footnote-call {{content:counter(footnote);font-size:{pt*0.7}pt;vertical-align:super;line-height:1}}
::footnote-marker {{content:counter(footnote) '. ';font-size:100%}}
figure {{margin:5mm 0;break-inside:avoid}}
figure img {{display:block;width:100%;height:auto;max-height:60mm}}
figcaption {{font:8.5pt/1.4 Label;margin-top:2mm;text-align:center}}
pre {{white-space:pre-wrap;font-size:9pt}}
'''
    toc=''.join('<a href="#'+html.escape(x['id'],quote=True)+'">'+html.escape(x['text'])+'</a>' for x in r.headings if x['level']==1)
    front=f'<section class="title"><div class="book-title">{title}</div><div class="subtitle">{subtitle}</div></section><section class="contents"><h2>Contents</h2>{toc}</section>'
    doc=f'<!doctype html><html lang="en"><head><meta charset="utf-8"><style>{css}</style></head><body>{front}{body}</body></html>'
    return doc,r
