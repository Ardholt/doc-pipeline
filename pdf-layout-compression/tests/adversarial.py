import json, shutil, sys, tempfile
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'source'))
from common import *
from check import inspect
from pypdf.generic import ContentStream, ArrayObject, DictionaryObject, TextStringObject

inp,out=map(Path,sys.argv[1:3]); records=[]
def rejected(name,fn):
    try: fn()
    except (ValueError,AssertionError) as e:
        records.append({'name':name,'passed':True,'diagnostic':str(e)[:500]}); print('PASS: rejected '+name)
    else: raise AssertionError('FAIL: accepted '+name)
with tempfile.TemporaryDirectory() as td:
    tmp=Path(td); a=tmp/'input with spaces'; b=tmp/'output with spaces'; a.mkdir(); b.mkdir()
    shutil.copy(inp/'input.pdf',a/'input.pdf'); shutil.copy(inp/'repair.json',a/'repair.json')
    for mutation in ['missing page','changed text','cropped page','missing image']:
        r=PdfReader(out/'fixed.pdf'); w=PdfWriter()
        for p in (r.pages[:-1] if mutation=='missing page' else r.pages): w.add_page(p)
        if mutation=='changed text':
            stream=ContentStream(w.pages[0].get_contents(),w)
            for i,(operands,operator) in enumerate(stream.operations):
                if operator in (b'Tj',b'TJ'):
                    del stream.operations[i]; break
            w.pages[0].replace_contents(stream)
        if mutation=='cropped page': w.pages[0].cropbox=RectangleObject((90,90,500,700))
        if mutation=='missing image':
            resources=w.pages[0]['/Resources']['/XObject']
            for key in list(resources):
                if resources[key].get('/Subtype')=='/Image': del resources[key]; break
        w._info=None
        with (b/'fixed.pdf').open('wb') as f: w.write(f)
        rejected(mutation,lambda:inspect(a,b))
    w=PdfWriter(); w.append(inp/'input.pdf'); w.encrypt('restricted')
    with (a/'input.pdf').open('wb') as f: w.write(f)
    rejected('encrypted input',lambda:load_input(a))
    (a/'input.pdf').write_bytes(b'%PDF-1.7\ninvalid')
    rejected('malformed input',lambda:load_input(a))
    (a/'input.pdf').unlink(); rejected('missing input',lambda:load_input(a))
    w=PdfWriter(); w.append(inp/'input.pdf')
    w.pages[0][NameObject('/Annots')]=ArrayObject([DictionaryObject({NameObject('/Subtype'):NameObject('/Text'),NameObject('/Contents'):TextStringObject('Review')})])
    with (a/'input.pdf').open('wb') as f: w.write(f)
    rejected('annotation before processing',lambda:load_input(a))
    shutil.copy(inp/'input.pdf',a/'input.pdf')
    cfg=json.loads((inp/'repair.json').read_text()); cfg['margin_mm']=7
    save(a/'repair.json',cfg); rejected('out-of-range margin',lambda:load_input(a))
    cfg['margin_mm']='ten'; save(a/'repair.json',cfg); rejected('wrong value type',lambda:load_input(a))
    # Independently authored reference is separate from the converter's input extraction.
    source=json.loads((Path(__file__).resolve().parents[1]/'source/content.json').read_text())
    r=PdfReader(out/'fixed.pdf')
    for spec,p in zip(source['pages'],r.pages):
        expected=' '.join([spec['title'],spec['subtitle'],*spec['lines'],spec['caption'],'UP','BASE',spec['note'],spec['footer']]).split()
        assert words(p)==expected,'authored reference mismatch'
    records.append({'name':'authored reference matches every output word','passed':True})
    # Exercise physical quarter-turns rather than /Rotate flags alone.
    for angle in (90,180,270):
        r=PdfReader(inp/'input.pdf'); p=r.pages[0]
        p.rotate(angle); p.transfer_rotation_to_content()
        cfg=json.loads((inp/'repair.json').read_text())
        normalize(r,cfg,tmp/'oriented.pdf')
        text=words(PdfReader(tmp/'oriented.pdf').pages[0])
        assert text==words(PdfReader(inp/'input.pdf').pages[0])
    records.append({'name':'physical quarter-turn text conservation','passed':True})
    # Poppler pads page filenames once a document has ten or more pages.
    w=PdfWriter(); source_pdf=PdfReader(inp/'input.pdf')
    for i in range(10): w.add_page(source_pdf.pages[i%len(source_pdf.pages)])
    w._info=None
    with (a/'input.pdf').open('wb') as f: w.write(f)
    cfg=json.loads((inp/'repair.json').read_text()); cfg.update(margin_mm=20,image_dpi=200)
    save(a/'repair.json',cfg)
    command([sys.executable,str(Path(__file__).resolve().parents[1]/'source/pipeline.py'),str(a),str(b)],timeout=180)
    measured=json.loads((b/'report.json').read_text())
    assert measured['counts']['pages']==10
    assert (b/'previews/hero.png').is_file()
    records.append({'name':'ten-page input, padded preview filenames, margin 20 mm and image setting 200 dpi','passed':True,'observed_pages':measured['counts']['pages']})

save(out/'adversarial.json',{'schema_version':1,'checks':records})
print('PASS: mutation tests and independent authored reference')
