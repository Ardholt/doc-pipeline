"""Compare document content and report facts across two independent runs."""
import json
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'source'))
from forms import inspect_docx, need, write_json


def compare(first, second):
    left=json.loads((first/'report.json').read_text()); right=json.loads((second/'report.json').read_text())
    facts=['schema_version','case','input_hashes','transformations','counts','measurements','checks','tools','uncertainties','human_steps']
    for key in facts: need(left[key]==right[key], 'repeat-run report facts differ: '+key)
    files=sorted(name for name in left['output_hashes'] if name.endswith('.docx'))
    for name in files:
        need(inspect_docx(first/name)==inspect_docx(second/name),'repeat-run DOCX content or controls differ: '+name)
    # Metadata and ZIP bytes may differ, but rasterized page content must agree too.
    images=sorted(name for name in left['output_hashes'] if name.endswith('.png') and '/' not in name)
    for name in images: need(left['output_hashes'][name]==right['output_hashes'][name], 'repeat-run rendered pixels differ: '+name)
    return {'schema_version':1,'passed':True,'compared_report_facts':facts,'compared_docx':files,'identical_rendered_images':images,'excluded':'Elapsed times, archive bytes and application-generated revision/control IDs are not a stability claim; DOCX inspection compares values, labels, controls, wrappers and row geometry.'}


if __name__=='__main__':
    result=compare(Path(sys.argv[1]),Path(sys.argv[2]))
    write_json(sys.argv[3], result)
    print('PASS: repeat-run document content, report facts and rendered pixels agree')
