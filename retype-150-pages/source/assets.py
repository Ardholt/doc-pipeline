"""Write an exhaustive per-file provenance inventory for the case tree."""
import sys
from pathlib import Path
from common import sha,write_json
case=Path(sys.argv[1]); target=case/'source/asset-manifest.json'
items=[]
for p in sorted(case.rglob('*')):
    if not p.is_file() or '__pycache__' in p.parts or 'generated' in p.relative_to(case).parts:continue
    rel=str(p.relative_to(case))
    if p.parent==case and p.suffix=='.log':continue
    if rel=='source/DejaVuSansMono.ttf':
        licence='Bitstream Vera permission; DejaVu changes public domain';origin='Unmodified DejaVu Sans Mono 2.37; DejaVu project distribution';source=['licenses/DejaVu.txt']
    elif rel=='licenses/DejaVu.txt':
        licence='Retained Bitstream Vera permission notice';origin='DejaVu fonts copyright notice, font portion only; unrelated Debian packaging notices omitted';source=['https://dejavu-fonts.github.io/']
    elif rel=='input/scan.pdf':
        licence='MIT original content; rendered DejaVu glyphs under Bitstream Vera permission';origin='Original typed records rendered fresh as raster-only pages';source=['source/reference.json','source/generate.py','source/DejaVuSansMono.ttf']
    elif rel=='input/review.csv':
        licence='MIT';origin='Original literal corrections from visual inspection of the source scan';source=['input/scan.pdf','source/review-record.md']
    elif p.suffix in ('.png','.pdf','.docx','.html'):
        licence='MIT original content; DejaVu font permission; GitHub Markdown CSS MIT where present';origin='Derived from the shipped scan and delivered document by the recorded applications';source=['input/scan.pdf','input/review.csv','output/report.json','licenses/DejaVu.txt','../harness/licenses/github-markdown-css.txt']
    else:
        licence='MIT';origin='Original code, text or generated measurements by Genco Doganay';source=['LICENSE']
    item={'path':rel,'licence':licence,'provenance':origin,'sources':source}
    if p!=target and rel!='proof/publication.json' and not rel.startswith('proof/antivirus'):item['sha256']=sha(p)
    else:item['note']='Inventory/scan evidence is listed without a mutually recursive hash.'
    items.append(item)
if not any(i['path']=='source/asset-manifest.json' for i in items):items.append({'path':'source/asset-manifest.json','licence':'MIT','provenance':'Original per-file provenance inventory by Genco Doganay','sources':['LICENSE'],'note':'This inventory is listed without its own recursive hash.'})
write_json(target,{'schema_version':1,'files':items,'runtime_fonts':[{'file':'/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf','use':'Document body, screenshots and figure labels','licence':'Bitstream Vera permission; DejaVu changes public domain','notice':'licenses/DejaVu.txt'},{'file':'/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf','use':'Document headings and table headers','licence':'Bitstream Vera permission; DejaVu changes public domain','notice':'licenses/DejaVu.txt'},{'file':'/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf','use':'Pages layout headings and figures','licence':'Bitstream Vera permission; DejaVu changes public domain','notice':'licenses/DejaVu.txt'},{'file':'/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf','use':'Code text in page screenshots','licence':'Bitstream Vera permission; DejaVu changes public domain','notice':'licenses/DejaVu.txt'}]})
print(f'PASS: provenance inventory covers {len(items)} files')
