"""Fault injection and alternate public input checks, run inside the same image."""
import json, shutil, sys, tempfile
from pathlib import Path
from pypdf import PdfReader, PdfWriter
from pypdf.generic import RectangleObject, DecodedStreamObject, NameObject, TextStringObject
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'source'))
from layout import load_input, make_html
from inspect_pdf import inspect, sha
from pipeline import clean_pdf
from weasyprint import HTML


def run(root,out):
    results=[]
    def record(name, passed, observation):
        results.append({'name':name,'passed':passed,'observation':observation})
        if not passed: raise ValueError(name+': '+str(observation))
    with tempfile.TemporaryDirectory() as tmp:
        work=Path(tmp); changed=work/'changed'; changed.mkdir()
        for mutation in ('trim_box','removed_page','erased_text','removed_link','damaged_link'):
            w=PdfWriter(clone_from=str(out/'interior.pdf'));w.metadata=None
            if mutation=='trim_box': w.pages[0].trimbox=RectangleObject([0,0,200,300])
            elif mutation=='removed_page': w.remove_page(3)
            elif mutation=='erased_text':
                p=w.pages[3]; stream=DecodedStreamObject();stream.set_data(b'');p.replace_contents(stream)
            elif mutation=='damaged_link':
                for p in w.pages:
                    for ref in p.get('/Annots',[]): ref.get_object()[NameObject('/Dest')]=TextStringObject('missing-target')
            else:
                for p in w.pages:
                    if '/Annots' in p: del p['/Annots']
            w.write(changed/'interior.pdf')
            facts=inspect(root,changed)
            failed=[x['name'] for x in facts['checks'] if not x['passed']]
            expected={'trim_box':'page_boxes','removed_page':'source_text_and_order','erased_text':'source_text_and_order','removed_link':'contents_links','damaged_link':'navigation_targets'}[mutation]
            record(mutation,expected in failed,{'detected_by':failed,'hash_check_used':False})
        inputs=work/'input with spaces';inputs.mkdir()
        base=json.loads((root/'print.json').read_text())
        (inputs/'manuscript.md').write_text('# Looking closely\n\nA café window holds a quiet reflection. A leaf turns.[^n]\n\n## A second look\n\n1. Record the light.\n2. Return to the edge.\n\n> Leave room beneath the sentence.\n\nSee [the opening](#looking-closely).\n\n[^n]: The accent and the note both belong to the text.\n')
        for name,override in [('narrow_bleed',{'trim_width_mm':120,'trim_height_mm':180,'bleed_mm':3,'margin_mm':25}),('wide_trim',{'trim_width_mm':220,'trim_height_mm':300,'bleed_mm':0,'margin_mm':15})]:
            cfg={**base,**override};(inputs/'print.json').write_text(json.dumps(cfg))
            cfg,ast=load_input(inputs);doc,_=make_html(cfg,ast,inputs)
            HTML(string=doc,base_url=str(inputs)).write_pdf(work/'raw.pdf')
            clean_pdf(work/'raw.pdf',changed/'interior.pdf',cfg)
            facts=inspect(inputs,changed);failed=[x['name'] for x in facts['checks'] if not x['passed']]
            record(name,not failed,{'settings':override,'failures':failed,'pages':facts['counts']['pages']})
        for name,override in [('negative_width',{'trim_width_mm':-1}),('wrong_type',{'bleed_mm':'3'}),('body_too_large',{'body_pt':80}),('missing_title',{'title':None})]:
            (inputs/'print.json').write_text(json.dumps({**base,**override}))
            try: load_input(inputs);failed=False;message='accepted invalid input'
            except ValueError as e: failed=True;message=str(e)
            record(name,failed,message)
        (inputs/'print.json').unlink()
        try: load_input(inputs);failed=False;message='accepted missing settings'
        except ValueError as e: failed=True;message=str(e)
        record('missing_print_json',failed,message)
    return {'schema_version':1,'status':'PASS','checks':results}

if __name__=='__main__':
    try:
        result=run(Path(sys.argv[1]),Path(sys.argv[2]));Path(sys.argv[3]).write_text(json.dumps(result,indent=2)+'\n');print('PASS: fault injection and alternate input checks')
    except Exception as e:
        print('FAIL: '+str(e),file=sys.stderr);sys.exit(1)
