"""Check local case-page destinations; distinguish external URLs from local evidence."""
import json,re,sys
from pathlib import Path
from urllib.parse import unquote,urlparse
root=Path(sys.argv[1]);readme=(root/'README.md').read_text()
targets=re.findall(r'\]\(([^)]+)\)',readme)+re.findall(r'(?:href|src)="([^"]+)"',readme)
local=[];external=[];failed=[]
for target in sorted(set(targets)):
    if target.startswith('https://'): external.append({'url':target,'status':'external; not fetched in the offline run'});continue
    path=(root/unquote(urlparse(target).path)).resolve()
    exists=path.is_file();local.append({'target':target,'exists':exists})
    if not exists: failed.append(target)
result={'schema_version':1,'status':'PASS' if not failed else 'FAIL','local':local,'external':external,'surface':'Relative links have the same case-folder base on GitHub and Pages; the root LICENSE sits one level up. External workflow badge and workflow URL are not fetched in the offline run.'}
Path(sys.argv[2]).write_text(json.dumps(result,indent=2)+'\n')
print(result['status']+': README local proof and download links')
if failed:sys.exit(1)
