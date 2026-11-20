"""Publication inventory, content/metadata checks and local case-page links."""
import hashlib, json, re, sys
from pathlib import Path
from PIL import Image
from pypdf import PdfReader
from pypdf.generic import DictionaryObject, ArrayObject, IndirectObject
root,out=map(Path,sys.argv[1:3]); slug='pdf-layout-compression'
# Run from a clone of this repository: python audit.py CLONE_ROOT OUTPUT_DIR (writes OUTPUT_DIR/publication-audit.json).
roots=[root/slug,root/'harness']
shared=[root/'LICENSE',root/'toolchain'/f'{slug}.json']
missing=[str(p.relative_to(root)) for p in shared if not p.is_file()]
if missing: sys.exit('Missing files; run this from a clone of the repository: '+', '.join(missing))
files=sorted([p for base in roots for p in base.rglob('*') if p.is_file()]+shared)
excluded={f'{slug}/proof/publication-audit.json'}
files=[p for p in files if str(p.relative_to(root)) not in excluded]
findings=[]; inventory=[]; pdfs=[]; pngs=[]
for p in files:
    rel=str(p.relative_to(root)); data=p.read_bytes()
    inventory.append({'path':rel,'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()})
    if any(part.startswith('.') or part=='__pycache__' for part in p.relative_to(root).parts): findings.append({'file':rel,'rule':'private filename'})
    if p.suffix=='.pdf':
        r=PdfReader(p,strict=True); bad=[]; seen=set()
        def walk(v):
            if isinstance(v,IndirectObject):
                key=(v.idnum,v.generation)
                if key in seen: return
                seen.add(key); v=v.get_object()
            if isinstance(v,DictionaryObject):
                for key,value in v.items():
                    if key in ('/JavaScript','/JS','/Launch','/EmbeddedFiles','/OpenAction','/AA','/RichMedia','/URI'): bad.append(key)
                    walk(value)
            elif isinstance(v,ArrayObject):
                for value in v: walk(value)
        walk(r.trailer['/Root'])
        texts='\n'.join(p.extract_text() or '' for p in r.pages)
        if re.search(r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}',texts): bad.append('contact in document text')
        if r.metadata or r.xmp_metadata: bad.append('Info or XMP metadata')
        if bad: findings.append({'file':rel,'rule':'PDF metadata/active-content/contact','keys':sorted(set(bad))})
        pdfs.append({'path':rel,'pages':len(r.pages),'info_absent':not bool(r.metadata),'xmp_absent':not bool(r.xmp_metadata),'active_content_findings':len(bad)})
    elif p.suffix=='.png':
        im=Image.open(p)
        bad=[k for k in im.info if k.lower() not in ('dpi','gamma','srgb','transparency')]
        if bad: findings.append({'file':rel,'rule':'PNG metadata','keys':bad})
        pngs.append({'path':rel,'width':im.width,'height':im.height,'text_exif_absent':not bad})
    else:
        try: text=data.decode('utf-8')
        except UnicodeDecodeError: findings.append({'file':rel,'rule':'unreviewed binary type'}); continue
        rules={'private_key':r'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----',
               'credential':r'\b(?:ghp_[A-Za-z0-9]{30,}|AKIA[A-Z0-9]{16})\b',
               'machine_path':r'/home/[a-z][^\s"<>]+'}
        for name,pattern in rules.items():
            if re.search(pattern,text): findings.append({'file':rel,'rule':name})
        if 'licenses/' not in rel and p.name!='audit.py' and re.search(r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}',text):
            findings.append({'file':rel,'rule':'email outside required licence notice'})
links=[]; md=root/slug/'README.md'
for target in re.findall(r'\]\(([^)]+)\)|(?:href|src)="([^"]+)"',md.read_text()):
    value=target[0] or target[1]
    if value.startswith('https://'):
        links.append({'target':value,'status':'external; not fetched in the offline run'})
    else:
        exists=(md.parent/value.split('#')[0]).exists()
        links.append({'target':value,'status':'local target exists' if exists else 'MISSING'})
        if not exists: findings.append({'file':str(md.relative_to(root)),'rule':'missing local link','target':value})
report={'schema_version':1,'scope':'explicit case and harness files',
        'checks':['local link resolution','document text contact scan','secret pattern scan','private path/name scan','PDF active objects and Info/XMP','PNG text/EXIF metadata','publishing file inventory'],
        'inventory':inventory,'pdfs':pdfs,'pngs':pngs,'links':links,'findings':findings,
        'limitations':['Pattern scans are not a guarantee of absence. ClamAV evidence is separate.','Live Pages, GitHub blob and Actions URLs are not fetched in the offline run.']}
out.mkdir(parents=True,exist_ok=True); (out/'publication-audit.json').write_text(json.dumps(report,indent=2)+'\n')
print(('PASS' if not findings else 'FAIL')+f': publication audit; {len(files)} files, {len(pdfs)} PDFs, {len(pngs)} PNGs, {len(findings)} findings')
if findings:
    for finding in findings: print(json.dumps(finding))
    sys.exit(1)
