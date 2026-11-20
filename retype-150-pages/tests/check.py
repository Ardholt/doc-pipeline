"""Inspect existing deliverables; no OCR, conversion or rebuilding required."""
import csv, io, json, re, sys, tempfile, zipfile
from pathlib import Path
from xml.etree import ElementTree as ET
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'source'))
from common import NS,sha,block_text,docx_pages,normalized,distance
from extract import parse_tsv,infer_blocks,apply_review,review_rows,restore_blocks
from score import score
from layout import audit


def require(ok, message):
    if not ok:raise ValueError(message)


def compare_document(pages,path):
    actual=docx_pages(path)
    require([p['page'] for p in actual]==[p['page'] for p in pages],'DOCX source-page order or count differs')
    for expected,got in zip(pages,actual):
        require(got['text']==expected['final_text'],f"DOCX text differs on source page {expected['page']}")
        require(got['blocks']==expected['blocks'],f"DOCX headings, paragraphs or table cells differ on source page {expected['page']}")


def semantics():
    tests=[]
    def reject(fn):
        try:fn()
        except ValueError:return
        raise ValueError('Expected rejection was not raised')
    row=lambda a,b,p=1,n=2:{'page':p,'find':a,'replace':b,'reason':'Verified reading','row':n}
    require(apply_review('K001: 25 + 2 = 27.',[],1)==('K001: 25 + 2 = 27.',[]),'Absent review changed text')
    text,log=apply_review('K001: 25 + 2 = 27.',[row('25','26'),row('26 + 2 = 27','26 + 2 = 28',n=3)],1)
    require(text=='K001: 26 + 2 = 28.' and len(log)==2,'Ordered literal review failed')
    require(apply_review('A.*B',[row('.*','[x]')],1)[0]=='A[x]B','Review incorrectly treats text as regex')
    require(apply_review('same',[row('same','new',p=2)],1)[0]=='same','Review leaked to another page')
    reject(lambda:apply_review('twice twice',[row('twice','once')],1))
    reject(lambda:apply_review('missing',[row('absent','present')],1))
    reject(lambda:apply_review('banana',[row('ana','x')],1))
    require(apply_review('one two',[row('one two','one\ntwo')],1)[0]=='one\ntwo','Multiline literal review failed')
    require(distance('K001, 27.','K001; 28.')==2,'Punctuation or number metric failed')
    require(distance(['a','b'],['a','c','b'])==1,'Word edit metric failed')
    with tempfile.TemporaryDirectory() as temp:
        p=Path(temp)/'review.csv'
        require(review_rows(p,1)==[],'No-review schema failed')
        p.write_text('page,find,replace,reason\n1,"a,b","a;c",Check\n')
        require(review_rows(p,1)[0]['find']=='a,b','Quoted CSV failed')
        p.write_text('page,find,replace,reason\n2,a,b,Check\n'); reject(lambda:review_rows(p,1))
        p.write_text('page,find,replace\n1,a,b\n'); reject(lambda:review_rows(p,1))
    return {'name':'review_semantics','passed':True,'observation':'Absent review; sequential exact replacements; literal punctuation; page isolation; zero/multiple matches rejected; quoted CSV and invalid page/schema checks.'}


def mutation_check(pages,path):
    with zipfile.ZipFile(path) as z:parts={n:z.read(n) for n in z.namelist()}
    count=0
    with tempfile.TemporaryDirectory() as temp:
        for mode in ('text','table','order'):
            root=ET.fromstring(parts['word/document.xml'])
            if mode=='text':
                node=root.find('.//w:t',NS); node.text=(node.text or '')+'!'
            elif mode=='table':
                node=root.find('.//w:tbl/w:tr/w:tc//w:t',NS)
                if node is None:continue
                node.text='DAMAGED'
            else:
                marks=[m for m in root.findall('.//w:bookmarkStart',NS) if m.get('{'+NS['w']+'}name','').startswith('source_page_')]
                if len(marks)<2:marks[0].set('{'+NS['w']+'}name','source_page_999')
                else:
                    a=marks[0].get('{'+NS['w']+'}name'); b=marks[1].get('{'+NS['w']+'}name')
                    marks[0].set('{'+NS['w']+'}name',b); marks[1].set('{'+NS['w']+'}name',a)
            target=Path(temp)/'damaged.docx'
            with zipfile.ZipFile(target,'w',zipfile.ZIP_DEFLATED) as z:
                for n,data in parts.items():z.writestr(n,ET.tostring(root) if n=='word/document.xml' else data)
            try:compare_document(pages,target)
            except ValueError:count+=1
            else:raise ValueError(f'Damaged {mode} was not detected')
    return {'name':'mutation_detection','passed':True,'observation':f'{count} deliberately damaged DOCX variants rejected by text/structure checks, independently of hashes.'}


def validate(inp,out,case):
    from pypdf import PdfReader
    from PIL import Image
    report=json.loads((out/'report.json').read_text()); mapping=json.loads((out/'pages.json').read_text()); pages=mapping['pages']
    checks=[]
    for n,h in report['input_hashes'].items():require(sha(inp/n)==h,f'Input hash differs: {n}')
    for n,h in report['output_hashes'].items():require(sha(out/n)==h,f'Output hash differs: {n}')
    checks.append({'name':'hashes','passed':True,'observation':'All declared input and output SHA-256 values match existing files.'})
    scan=PdfReader(inp/'scan.pdf'); require(len(scan.pages)==len(pages),'Scan and mapping page counts differ')
    require([p['page'] for p in pages]==list(range(1,len(pages)+1)),'Missing or duplicated mapped page')
    require([p['id'] for p in pages]==[f'page-{i:03d}' for i in range(1,len(pages)+1)],'Invalid or repeated page identifier')
    require(all(not (p.extract_text() or '').strip() for p in scan.pages),'Scan has hidden text')
    reviews=review_rows(inp/'review.csv',len(pages)); events=[]
    for p in pages:
        require(p['source']=='scan.pdf' and p['source_page']==p['page'] and p['docx_bookmark']==f"source_page_{p['page']:03d}",'Source mapping fields differ')
        stem=f"page-{p['page']:03d}"; raw=(out/'raw'/f'{stem}.txt').read_text().removesuffix('\n')
        lines,_=parse_tsv((out/'raw'/f'{stem}.tsv').read_text()); blocks=infer_blocks(lines)
        require(block_text(blocks)==raw==p['raw_text'],'Raw text does not match retained extraction')
        final,log=apply_review(raw,reviews,p['page']); events.extend(log)
        require(final==p['final_text']==block_text(p['blocks']),'Review log or final text differs')
        require(restore_blocks(final,blocks)==p['blocks'],'Reconstructed blocks differ')
    events.sort(key=lambda event:event['row'])
    corrections=json.loads((out/'corrections.json').read_text()); require(corrections['events']==events,'Correction audit differs')
    compare_document(pages,out/'retyped.docx')
    checks.append({'name':'page_text_structure','passed':True,'observation':f'{len(pages)} pages in source order. Raw TSV, raw text, literal review, DOCX headings, paragraphs and table cells reconcile.'})
    accuracy=json.loads((out/'accuracy.json').read_text()); require(accuracy=={'schema_version':1,**score(inp/'scan.pdf',out,case)},'Accuracy facts differ from independently recomputed metrics')
    if accuracy.get('available'):require(accuracy['structure_exact_pages']==len(pages),'Reference heading/paragraph/table structure differs')
    checks.append({'name':'independent_reference','passed':True,'observation':'Metrics recomputed from actual DOCX XML against separately authored source, or explicitly unavailable for a replacement scan.'})
    require(json.loads((out/'layout.json').read_text())==audit(out/'preview.pdf'),'PDF layout measurements differ')
    checks.append({'name':'pdf_text_bounds','passed':True,'observation':'Poppler word boxes measured on every cleaned PDF page remain inside the page edge band.'})
    pdf=PdfReader(out/'preview.pdf')
    expected=normalized(' '.join(p['final_text'] for p in pages)); actual=normalized(' '.join(p.extract_text() or '' for p in pdf.pages))
    require(actual==expected,'LibreOffice PDF text differs from delivered DOCX text')
    require(not pdf.metadata and '/Metadata' not in pdf.trailer['/Root'],'PDF metadata remains')
    for page in pdf.pages:
        require('/Annots' not in page and '/Metadata' not in page,'PDF annotation or page metadata remains')
        for font in page['/Resources'].get('/Font',{}).values():
            font=font.get_object()
            for f in font.get('/DescendantFonts',[font]):
                f=f.get_object(); desc=f.get('/FontDescriptor')
                require(desc is not None and any(k in desc.get_object() for k in ('/FontFile','/FontFile2','/FontFile3')),'PDF font is not embedded')
    with zipfile.ZipFile(out/'retyped.docx') as z:
        require(not any(n.startswith('docProps/') for n in z.namelist()),'DOCX properties remain')
        xml=z.read('word/document.xml'); root=ET.fromstring(xml)
        require(not any(root.findall('.//w:'+tag,NS) for tag in ('vanish','ins','del','commentRangeStart')),'Hidden text or revision data remains')
        require(not any('vba' in n.lower() or 'embedding' in n.lower() for n in z.namelist()),'Executable or embedded content found')
        for n in z.namelist():
            if n.endswith('.rels'):require(b'TargetMode="External"' not in z.read(n),'External DOCX relationship found')
    for p in list((out/'media').glob('*.png'))+list((out/'page-previews').glob('*.png')):require(not Image.open(p).info,f'PNG metadata remains in {p.name}')
    checks.append({'name':'render_and_metadata','passed':True,'observation':'Cleaned LibreOffice PDF is searchable with the same normalized text as DOCX; PDF fonts embedded; DOCX properties/revisions/external links and PDF/PNG metadata absent.'})
    require(report['counts']['input_pages']==len(pages) and report['counts']['preview_pages']==len(pdf.pages),'Reported page count differs')
    require(report['counts']['tables']==sum(b['kind']=='table' for p in pages for b in p['blocks']),'Reported table count differs')
    checks.extend([semantics(),mutation_check(pages,out/'retyped.docx')])
    for check in checks:print('PASS: '+check['name'],flush=True)
    return checks

if __name__=='__main__':
    try:validate(Path(sys.argv[1]),Path(sys.argv[2]),Path(__file__).resolve().parents[1])
    except Exception as exc:print(f'FAIL: {exc}',file=sys.stderr);sys.exit(1)
