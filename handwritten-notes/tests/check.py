"""Inspect delivered content independently of converter exit status."""
import hashlib,json,re,sys,zipfile
from pathlib import Path
from xml.etree import ElementTree as ET
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'source'))
from model import load,ordered,text,mapping,uncertainty
from pypdf import PdfReader
W='{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
def digest(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def inspect(src,out,hashes=True):
    pages,tr=load(src); seq=[b for p in ordered(pages,tr) for b in p['blocks']]
    with zipfile.ZipFile(out/'notes.docx') as z:
        root=ET.fromstring(z.read('word/document.xml'))
        paras=root.findall('.//'+W+'body/'+W+'p')
        def paragraph_text(p):
            return ''.join((el.text or '') if el.tag==W+'t' else '\t' if el.tag==W+'tab' else '\n' if el.tag in (W+'br',W+'cr') else '' for el in p.iter())
        actual=[paragraph_text(p) for p in paras]
        assert actual==[b['text'] for b in seq], 'DOCX text/order mismatch'
        for p,b in zip(paras,seq):
            style=p.find(W+'pPr/'+W+'pStyle')
            expected={'heading':'Heading1','paragraph':None,'bullet':'ListBullet'}[b['kind']]
            assert (style.get(W+'val') if style is not None else None)==expected,'DOCX block formatting mismatch'
        assert not any(n.startswith('docProps/') for n in z.namelist()),'DOCX properties retained'
        assert not any(x in z.read('word/document.xml') for x in (b'<w:del',b'<w:ins',b'<w:vanish',b'<w:comment')), 'Hidden/revision content'
        assert not any(b'TargetMode="External"' in z.read(n) for n in z.namelist() if n.endswith('.rels')), 'External relationship'
    assert (out/'notes.txt').read_text()==text(pages,tr),'TXT text mismatch'
    assert json.loads((out/'mapping.json').read_text())==mapping(pages,tr),'Page/block mapping mismatch'
    assert json.loads((out/'uncertainties.json').read_text())==uncertainty(pages,tr),'Uncertainty list mismatch'
    pdf=PdfReader(out/'preview.pdf')
    normalize=lambda s:re.sub(r'\s+','',s).replace('•','').replace('\uf0b7','')
    assert normalize(''.join(p.extract_text() for p in pdf.pages))==normalize(text(pages,tr)), 'PDF text mismatch'
    assert not pdf.metadata and not pdf.xmp_metadata,'PDF metadata retained'
    assert not any(p.get('/Annots') for p in pdf.pages),'PDF annotations'
    report=json.loads((out/'report.json').read_text())
    assert report['counts']=={'source_pages':len(pages['pages']),'blocks':len(seq),'unclear_tokens':sum(b['text'].count('[unclear]') for b in seq),'pdf_pages':len(pdf.pages)},'Report count mismatch'
    assert report['input_hashes']=={p.relative_to(src).as_posix():digest(p) for p in sorted(src.rglob('*')) if p.is_file()},'Input hashes mismatch'
    if hashes:
        for n,h in report['output_hashes'].items(): assert digest(out/n)==h,'Output hash mismatch: '+n
    return len(seq)
if __name__=='__main__':
    try:
        n=inspect(*map(Path,sys.argv[1:3])); print(f'PASS: existing output; {n} blocks, literal uncertainty, mapping, DOCX styles, PDF text and metadata')
    except Exception as e:
        print('FAIL: '+str(e),file=sys.stderr);sys.exit(1)
