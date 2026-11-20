"""Exercise repeatability and replacement input paths containing spaces."""
import csv, hashlib, json, os, shutil, subprocess, sys, tempfile, zipfile
from pathlib import Path
from pypdf import PdfReader


def content(out):
    with zipfile.ZipFile(out/'deck.pptx') as z:
        package=hashlib.sha256(b''.join(n.encode()+z.read(n) for n in sorted(z.namelist()))).hexdigest()
    return {'pptx_package_content_sha256':package,'pdf_text_sha256':hashlib.sha256('\n'.join(p.extract_text() for p in PdfReader(out/'deck.pdf').pages).encode()).hexdigest()}

def execute(inp,out):
    with tempfile.TemporaryDirectory() as profile:
        env=dict(os.environ,LO_PROFILE_URI=Path(profile).as_uri())
        proc=subprocess.run([sys.executable,'/case/source/pipeline.py',str(inp),str(out)],capture_output=True,text=True,timeout=240,env=env)
    if proc.returncode: raise ValueError(proc.stdout+proc.stderr)
    return json.loads((out/'report.json').read_text())

def main():
    records=[]
    with tempfile.TemporaryDirectory() as temp:
        base=Path(temp); inp=base/'input with spaces'; out=base/'output with spaces';shutil.copytree('/case/input',inp)
        before={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in inp.iterdir()}
        first=execute(inp,out); first_content=content(out)
        second=execute(inp,out); second_content=content(out)
        fields=('input_hashes','transformations','counts','checks','tools','uncertainties','human_steps')
        if any(first[k]!=second[k] for k in fields) or first_content!=second_content:raise ValueError('repeat run changed document content or report facts')
        if before!={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in inp.iterdir()}:raise ValueError('input changed')
        records.append({'test':'identical runs and paths containing spaces','passed':True,'content':first_content,'report_fields_compared':fields,'input_hashes_unchanged':True})
        cfg={'schema_version':1,'title':'Recorded department figures','currency':'GBP','department_order':['D','B','A','C'],'colours':{'A':'#146C78','B':'#3656A8','C':'#B24930','D':'#7156A8'}}
        (inp/'deck.json').write_text(json.dumps(cfg))
        with (inp/'data.csv').open('w') as stream:
            writer=csv.writer(stream);writer.writerow(['period','department','revenue','cost'])
            for m in range(1,5):
                for d in ['A','B','C','D']:
                    writer.writerow([f'2026-{m:02}',d,f'{1000+m}.01',f'{1100-m}.02' if d=='C' else f'{500+m}.00'])
        changed=execute(inp,out)
        if changed['counts']['slides']!=9 or changed['counts']['editable_charts']!=13:raise ValueError('replacement data did not expand the slide structure')
        records.append({'test':'replacement values, cents, order and adaptive pagination','passed':True,'counts':changed['counts'],'native_chart_checks':changed['checks']})
    print(json.dumps({'schema_version':1,'scope':'Full offline pipeline runs in temporary directories, including rendering and checks. Excludes Docker argument parser; separate shell evidence covers mount paths.','checks':records},indent=2))

if __name__=='__main__':
    try: main()
    except Exception as exc: print('FAIL: '+str(exc),file=sys.stderr);sys.exit(1)
