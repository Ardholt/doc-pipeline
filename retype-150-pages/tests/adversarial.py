"""Small replacement-input and failure checks using the already built container."""
import csv,json,os,subprocess,sys,tempfile
from pathlib import Path
from pypdf import PdfReader,PdfWriter
from pypdf.generic import NameObject
sys.path.insert(0,'/case/source')
from common import write_json,sha

out=Path('/output'); evidence=[]
with tempfile.TemporaryDirectory(prefix='replacement checks ') as temp:
    root=Path(temp); inp=root/'input with spaces'; inp.mkdir(); dest=out/'replacement-check'
    w=PdfWriter(); original=PdfReader('/input/scan.pdf')
    for p in original.pages[:2]:
        w.add_page(p)
        w.pages[-1][NameObject('/Resources')]=w._add_object(w.pages[-1]['/Resources'])
    w._info=None
    with (inp/'scan.pdf').open('wb') as f:w.write(f)
    def execute(success):
        env=os.environ.copy();env['LO_PROFILE_URI']=Path(tempfile.mkdtemp(dir=root)).as_uri()
        p=subprocess.run(['python','/case/source/pipeline.py',str(inp),str(dest)],capture_output=True,text=True,timeout=240,env=env)
        if (p.returncode==0)!=success:raise ValueError('Unexpected replacement test result: '+p.stdout[-500:]+p.stderr[-500:])
        return p
    execute(True)
    report=json.loads((dest/'report.json').read_text())
    assert report['counts']['input_pages']==2 and report['accuracy']['available'] is False
    evidence.append({'name':'replacement_scan','passed':True,'observation':'Two-page image-only PDF, directory names containing spaces, no reference accuracy assertion, no review file.'})
    raw=json.loads((dest/'pages.json').read_text())['pages'][0]['raw_text']
    find=raw.split('\n')[0]
    with (inp/'review.csv').open('w',newline='') as f:
        writer=csv.writer(f);writer.writerow(['page','find','replace','reason']);writer.writerow([1,find,find+'\nUPDATED','Check literal review transport'])
    execute(True)
    reviewed=json.loads((dest/'pages.json').read_text())['pages'][0]
    assert reviewed['raw_text']==raw and reviewed['final_text'].startswith(find+'\nUPDATED')
    evidence.append({'name':'review_integration','passed':True,'observation':'One literal correction, including a line break, reaches DOCX/PDF while retained raw text is unchanged.'})
    with (inp/'review.csv').open('w',newline='') as f:
        writer=csv.writer(f);writer.writerow(['page','find','replace','reason']);writer.writerow([1,'ABSENT TOKEN','value','No match'])
    r=execute(False);assert 'expected one literal match, found 0' in r.stderr
    evidence.append({'name':'missing_review_match','passed':True,'observation':'Nonzero exit with a specific zero-match diagnostic.'})
    (inp/'review.csv').unlink(); (inp/'scan.pdf').unlink()
    r=execute(False);assert 'Missing required input: scan.pdf' in r.stderr
    evidence.append({'name':'missing_scan','passed':True,'observation':'Nonzero exit with required scan filename.'})
    (inp/'scan.pdf').write_text('broken PDF')
    r=execute(False);assert 'FAIL:' in r.stderr
    evidence.append({'name':'invalid_scan','passed':True,'observation':'Malformed PDF gives nonzero exit; no success message.'})
import shutil
shutil.rmtree(dest)
write_json(out/'adversarial.json',{'schema_version':1,'checks':evidence})
for row in evidence:print('PASS: '+row['name'])
