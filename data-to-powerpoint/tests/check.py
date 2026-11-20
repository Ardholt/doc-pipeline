"""Inspect delivered chart caches, embedded sheets, slide text, PDF and metadata."""
import hashlib, io, json, re, sys, zipfile
from decimal import Decimal
from pathlib import Path
from xml.etree import ElementTree as ET
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'source'))
from data import read_inputs, sums, money
from pptx import Presentation
from pypdf import PdfReader
from PIL import Image

NS={'c':'http://schemas.openxmlformats.org/drawingml/2006/chart','a':'http://schemas.openxmlformats.org/drawingml/2006/main','s':'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}

def ensure(test,message):
    if not test: raise ValueError(message)

def workbook_values(raw):
    z=zipfile.ZipFile(io.BytesIO(raw))
    ensure(not any(n.startswith('docProps/') for n in z.namelist()),'embedded workbook properties remain')
    ss=[]
    if 'xl/sharedStrings.xml' in z.namelist():
        ss=[''.join(e.itertext()) for e in ET.fromstring(z.read('xl/sharedStrings.xml'))]
    root=ET.fromstring(z.read('xl/worksheets/sheet1.xml')); cells={}
    for c in root.findall('.//s:c',NS):
        v=c.find('s:v',NS)
        if v is not None:
            cells[c.get('r')]=ss[int(v.text)] if c.get('t')=='s' else Decimal(v.text)
    return cells

def expected_charts(cfg,rows,periods):
    result=[]; order=cfg['department_order']
    for start in range(0,len(order),6):
        group=order[start:start+6]
        result.append(('overview',None,group,[('Revenue',[sums([r for r in rows if r['department']==d])['revenue'] for d in group])],[r['line'] for r in rows if r['department'] in group]))
    for start in range(0,len(order),3):
        for d in order[start:start+3]:
            dr=[r for r in rows if r['department']==d]; total=sums(dr)
            result.append(('comparison',d,[d],[('Revenue',[total['revenue']]),('Cost',[total['cost']])],[r['line'] for r in dr]))
    for pstart in range(0,len(periods),3):
        ps=periods[pstart:pstart+3]
        for start in range(0,len(order),3):
            for d in order[start:start+3]:
                dr=sorted([r for r in rows if r['department']==d and r['period'] in ps],key=lambda r:r['period'])
                result.append(('trend',d,[p[5:] for p in ps],[(d+' profit',[r['revenue']-r['cost'] for r in dr])],[r['line'] for r in dr]))
    return result

def inspect(inp,out,hashes=True):
    cfg,rows,periods=read_inputs(inp); deck=Presentation(out/'deck.pptx'); z=zipfile.ZipFile(out/'deck.pptx')
    expected=expected_charts(cfg,rows,periods); charts=[(n+1,sh.chart) for n,s in enumerate(deck.slides) for sh in s.shapes if sh.has_chart]
    ensure(len(charts)==len(expected),'native chart count differs from input expectations')
    mappings=json.loads((out/'source-map.json').read_text())['charts']
    ensure(len(mappings)==len(charts),'source map chart count mismatch')
    points=0
    for (slide,ch),(kind,dep,cats,series,lines),mapping in zip(charts,expected,mappings):
        xml=ET.fromstring(z.read(str(ch.part.partname).lstrip('/')))
        ensure(mapping['slide']==slide and mapping['source_lines']==lines and mapping['part']==str(ch.part.partname).lstrip('/'),'source map does not match actual chart/source lines')
        actual=xml.findall('.//c:barChart/c:ser',NS)
        ensure(len(actual)==len(series),'chart series count mismatch')
        for i,(a,(name,values)) in enumerate(zip(actual,series)):
            names=[e.text for e in a.findall('c:tx/c:strRef/c:strCache/c:pt/c:v',NS)]
            ensure(names==[name],'chart series name mismatch')
            labels=[e.text for e in a.findall('c:cat/c:strRef/c:strCache/c:pt/c:v',NS)]
            nums=[Decimal(e.text) for e in a.findall('c:val/c:numRef/c:numCache/c:pt/c:v',NS)]
            ensure(labels==cats and nums==values,f'chart cache mismatch on slide {slide}: {kind} {dep}')
            points+=len(nums)
            if dep:
                colour=a.find('c:spPr/a:solidFill/a:srgbClr',NS)
                ensure(colour is not None and colour.get('val').upper()==(cfg['colours'][dep][1:].upper() if i==0 else 'CAD2D9'),'department/cost colour mismatch')
            else:
                colours=[p.find('c:spPr/a:solidFill/a:srgbClr',NS).get('val').upper() for p in a.findall('c:dPt',NS)]
                ensure(colours==[cfg['colours'][d][1:].upper() for d in cats],'overview order/colours mismatch')
        rels=[r for r in ch.part.rels.values() if r.reltype.endswith('/package')]
        ensure(len(rels)==1,'chart must have one embedded workbook')
        cells=workbook_values(rels[0].target_part.blob)
        expected_cells={f'A{i+2}':v for i,v in enumerate(cats)}
        for j,(name,values) in enumerate(series,1):
            col=chr(65+j); expected_cells[col+'1']=name
            expected_cells.update({f'{col}{i+2}':v for i,v in enumerate(values)})
        ensure(cells==expected_cells,f'embedded workbook mismatch on slide {slide}')
        minimum=Decimal(xml.find('.//c:valAx/c:scaling/c:min',NS).get('val')); maximum=Decimal(xml.find('.//c:valAx/c:scaling/c:max',NS).get('val'))
        ensure(minimum<=min([Decimal(0)]+[v for _,vs in series for v in vs]) and maximum>=max([Decimal(0)]+[v for _,vs in series for v in vs]),'chart axis conceals values or zero')
    texts=['\n'.join(sh.text for sh in s.shapes if sh.has_text_frame) for s in deck.slides]
    totals=sums(rows)
    for v in totals.values(): ensure(money(v) in texts[0],'visible title-slide total mismatch')
    ensure(cfg['title'] in texts[0],'visible deck title mismatch')
    for i,s in enumerate(deck.slides):
        ensure(s._element.get('show')!='0','hidden slide present')
        for sh in s.shapes:
            ensure(sh.left>=0 and sh.top>=0 and sh.left+sh.width<=deck.slide_width+100 and sh.top+sh.height<=deck.slide_height+100,'shape outside slide bounds')
            ensure(sh.shape_type!=13,'slide contains a raster picture instead of editable content')
    reader=PdfReader(out/'deck.pdf')
    for (slide,_),(_,_,_,series,_) in zip(charts,expected):
        rendered=(reader.pages[slide-1].extract_text() or '').replace('−','-')
        for _,values in series:
            for value in values:
                ensure(money(value) in rendered,f'rendered chart label missing on slide {slide}: {money(value)}')
    ensure(len(reader.pages)==len(deck.slides),'PDF page count mismatch')
    pdftext='\n'.join(p.extract_text() or '' for p in reader.pages).replace('−','-')
    ensure(cfg['title'] in pdftext and all(money(v) in pdftext for v in totals.values()),'rendered PDF lost title or a financial total')
    for mapping in json.loads((out/'source-map.json').read_text())['slides']:
        ensure(mapping['headline'] in texts[mapping['slide']-1],'visible slide takeaway differs from source map')
    ensure(not reader.metadata and '/Metadata' not in reader.trailer['/Root'],'PDF metadata remains')
    ensure(not any(n.startswith('docProps/') or '/comments' in n or n.endswith('.bin') for n in z.namelist()),'PPTX properties/comments/executable content present')
    for name in z.namelist():
        if name.endswith('.rels'):
            ensure(all(r.get('TargetMode')!='External' for r in ET.fromstring(z.read(name))),'external relationship present')
    for p in reader.pages:
        ensure('/Annots' not in p and '/Metadata' not in p,'PDF annotations or page metadata remain')
    images=sorted((out/'slides').glob('slide-*.png'))
    ensure(len(images)==len(deck.slides),'slide image count mismatch')
    for p in images:
        im=Image.open(p); ensure(not im.info,'PNG metadata remains')
    if hashes:
        report=json.loads((out/'report.json').read_text())
        ensure(report['input_hashes']=={n:hashlib.sha256((inp/n).read_bytes()).hexdigest() for n in ('data.csv','deck.json')},'input hash mismatch')
        for name,digest in report['output_hashes'].items():
            ensure(hashlib.sha256((out/name).read_bytes()).hexdigest()==digest,'output hash mismatch: '+name)
        ensure(report['counts']['slides']==len(deck.slides) and report['counts']['editable_charts']==len(charts) and report['counts']['totals']=={k:str(v) for k,v in totals.items()},'report facts differ from files')
    return [{'name':'Chart caches and embedded workbooks reconcile','passed':True,'observation':f'{points} plotted values matched exact decimal input aggregates across {len(charts)} native charts.'},{'name':'Department order, colours, axes and source mapping','passed':True,'observation':'Order and colours match deck.json; axes include zero and all values; source line maps match chart parts.'},{'name':'Editable text and rendered totals','passed':True,'observation':f'{len(deck.slides)} native slides and PDF pages; title and revenue/cost/profit totals present; no raster slide pictures.'},{'name':'Package metadata and hashes','passed':True,'observation':'No PPTX/workbook properties, comments, external relationships, PDF metadata/annotations or PNG metadata; input/output hashes match.'}]

if __name__=='__main__':
    try:
        results=inspect(Path(sys.argv[1]),Path(sys.argv[2]))
        if '--json' in sys.argv: print(json.dumps(results))
        else:
            for r in results: print('PASS: '+r['name'])
    except Exception as exc:
        print('FAIL: '+str(exc),file=sys.stderr);sys.exit(1)
