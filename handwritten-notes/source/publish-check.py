"""Static audit and exhaustive file hash inventory."""
import hashlib,json,re,struct,sys,zipfile
from pathlib import Path
root=Path(sys.argv[1]);records=[];issues=[]
for p in sorted(root.rglob('*')):
    if not p.is_file() or p.relative_to(root).as_posix()=='proof/publication-scan.json':continue
    rel=p.relative_to(root).as_posix();data=p.read_bytes()
    records.append({'file':rel,'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()})
    if any(part in ('.git','__pycache__') for part in p.parts):issues.append(rel+': repository or runtime path')
    if data.startswith((b'MZ',b'\x7fELF')):issues.append(rel+': unexpected binary executable')
    if p.suffix in ('.md','.json','.py','.sh','.svg','.html','.yml'):
        s=data.decode('utf-8')
        if re.search(r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}',s):issues.append(rel+': email-shaped text')
        if re.search(r'(?:gh[pousr]_[A-Za-z0-9]{20,}|AKIA[A-Z0-9]{16}|-----BEGIN [A-Z ]*PRIVATE KEY-----)',s):issues.append(rel+': credential-shaped text')
    if p.suffix=='.png':
        offset=8;chunks=[]
        while offset<len(data):
            length=struct.unpack('>I',data[offset:offset+4])[0];typ=data[offset+4:offset+8].decode();chunks.append(typ);offset+=12+length
        if set(chunks)&{'tEXt','zTXt','iTXt','eXIf'}:issues.append(rel+': image metadata')
    if p.suffix=='.docx':
        with zipfile.ZipFile(p) as z:
            for n in z.namelist():
                if n.startswith('docProps/') or re.search(r'(vbaProject|activeX|embeddings/|comments\d*\.xml)',n):issues.append(rel+': unexpected package part '+n)
                if n.endswith('.rels') and b'TargetMode="External"' in z.read(n):issues.append(rel+': external relationship')
                if n.endswith('.xml'):
                    content=z.read(n).decode('utf-8')
                    if re.search(r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}',content):issues.append(rel+': email-shaped text in '+n)
                    if re.search(r'/(?:home|Users)/|-----BEGIN [A-Z ]*PRIVATE KEY-----',content):issues.append(rel+': private content in '+n)
    if p.suffix=='.pdf' and re.search(rb'/(?:JavaScript|JS|EmbeddedFile|Launch|RichMedia)\b',data):issues.append(rel+': active/embedded PDF payload')
report={'schema_version':1,'scope':'Case file tree.','scanner':'Python standard-library static publication audit','scanner_version':sys.version.split()[0],'coverage':['All files hashed and inventoried','Credential-shaped strings and email-shaped text in public text files; email/private-path checks in DOCX XML','PNG ancillary metadata','DOCX package properties, macros, embedded payloads and external relationships','PDF active-content and attachment signatures','Unexpected native executable headers and private file paths'],'limitations':['Static inspection is not an antivirus signature database or a malware-free certification.','Live links are not fetched in this offline scan.'],'files':records,'issues':issues,'status':'PASS' if not issues else 'FAIL'}
print(json.dumps(report,indent=2))
if issues:sys.exit(1)
