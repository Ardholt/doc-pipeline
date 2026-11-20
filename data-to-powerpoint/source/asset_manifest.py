"""Write per-file provenance entries for the reviewed case tree."""
import json
from pathlib import Path
root=Path(__file__).resolve().parents[1]
entries=[]
for path in sorted(root.rglob('*')):
    if not path.is_file() or path.name in ('asset-manifest.json','publication.json'): continue
    name=path.relative_to(root).as_posix()
    if name=='output/font-licences/DejaVu.txt':
        origin='Verbatim Debian fonts-dejavu-core 2.37-6 copyright and licence notice'
        licence='Bitstream Vera licence; DejaVu changes public domain; retained packaging notices'
    elif name.startswith(('output/','media/','proof/')):
        origin='Generated from input/data.csv and input/deck.json by this pipeline, or recorded from checks of those outputs; page captures use the shared harness layout and vendored GitHub Markdown CSS'
        licence='MIT for original content and layouts; DejaVu font terms apply to embedded font programs; shared GitHub Markdown CSS retains its MIT notice in harness/licenses/github-markdown-css.txt'
    elif name.startswith('input/'):
        origin='Newly authored anonymous department figures and display settings, Genco Doganay'
        licence='MIT'
    elif name=='Dockerfile':
        origin='Shared document harness recipe adapted with the declared presentation dependency pins'
        licence='MIT; installed dependencies retain their own package licences'
    else:
        origin='Original case text, implementation or verification code, Genco Doganay; README follows the shared case-page layout'
        licence='MIT'
    entries.append({'path':'data-to-powerpoint/'+name,'origin':origin,'licence':licence})
print(json.dumps({'schema_version':1,'files':entries,'self_entry':{'path':'data-to-powerpoint/proof/asset-manifest.json','origin':'Generated exhaustive file provenance inventory','licence':'MIT'},'audit_entry':{'path':'data-to-powerpoint/proof/publication.json','origin':'Generated exact file hash and static safety inventory','licence':'MIT'}},indent=2))
