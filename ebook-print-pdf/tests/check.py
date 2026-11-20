"""Read existing output and fail if its bytes or source-derived content have changed."""
import json, sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'source'))
from inspect_pdf import inspect, sha


def check(root,out):
    findings=inspect(root,out)
    failed=[x['name'] for x in findings['checks'] if not x['passed']]
    report=json.loads((out/'report.json').read_text())
    for name,digest in report['input_hashes'].items():
        if not (root/name).is_file() or sha(root/name)!=digest: failed.append('input hash: '+name)
    for name,digest in report['output_hashes'].items():
        if not (out/name).is_file() or sha(out/name)!=digest: failed.append('output hash: '+name)
    if findings['counts']!=report['counts']: failed.append('measured counts disagree with report')
    if findings['checks']!=report['checks']: failed.append('measured checks disagree with report')
    if failed: raise ValueError('; '.join(failed))
    print('PASS: existing PDF independently checked against manuscript, geometry, fonts, notes, links and hashes')

if __name__=='__main__':
    try: check(Path(sys.argv[1]),Path(sys.argv[2]))
    except Exception as e:
        print('FAIL: '+str(e),file=sys.stderr);sys.exit(1)
