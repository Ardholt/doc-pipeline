#!/usr/bin/env python3
"""Static publication checks; no antivirus-engine claim."""
import hashlib,json,re,struct,sys,zipfile
from pathlib import Path
root=Path(sys.argv[1]); destination=Path(sys.argv[2])
files=[]; failures=[]
private=[b'BEGIN '+b'PRIVATE KEY', b'/home/[a-z0-9_-]+/', b'AKIA'+b'[0-9A-Z]{16}', b'ghp_'+b'[A-Za-z0-9]{36}']
for f in sorted(root.rglob('*')):
    if not f.is_file() or f==destination: continue
    rel=f.relative_to(root).as_posix(); data=f.read_bytes()
    if any(part in ['__pycache__'] for part in f.parts): failures.append(rel+': runtime file')
    if any(re.search(p,data) for p in private): failures.append(rel+': private marker')
    if data.startswith((b'\x7fELF',b'MZ')): failures.append(rel+': executable binary')
    if f.suffix=='.png':
        pos=8; chunks=[]
        while pos<len(data):
            size=struct.unpack('>I',data[pos:pos+4])[0]; kind=data[pos+4:pos+8].decode();chunks.append(kind);pos+=size+12
        if any(c in chunks for c in ['tEXt','zTXt','iTXt','eXIf']): failures.append(rel+': image metadata')
    if f.suffix=='.epub':
        with zipfile.ZipFile(f) as z:
            for n in z.namelist():
                if '..' in Path(n).parts or n.startswith('/'): failures.append(rel+': unsafe ZIP path')
                if re.search(b'<(?:script|iframe)|javascript:|<!ENTITY',z.read(n),re.I): failures.append(rel+': active EPUB content')
    if f.suffix in ['.md','.json','.xhtml'] and 'licenses/' not in rel:
        if re.search(rb'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}',data): failures.append(rel+': contact address')
    files.append({'file':rel,'sha256':hashlib.sha256(data).hexdigest(),'bytes':len(data)})
result={'schema_version':1,'scope':'Exact delivered case tree except this inventory output; static secret/contact markers, private filenames, executable signatures, EPUB active content and archive paths, PNG ancillary metadata. Prose and screenshots were read separately.','scanner':'Python standard-library publication policy check 1.0','malware_check':'Static executable-signature and EPUB active-content checks; not a signature antivirus scan. Only the documented browser reader contains local interaction JavaScript; offline page render retains the public analytics reference.','files':files,'findings':failures,'status':'PASS' if not failures else 'FAIL'}
destination.write_text(json.dumps(result,indent=2)+'\n')
print(result['status']+': publication static scan')
if failures: print('\n'.join(failures));sys.exit(1)
