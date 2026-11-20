"""Offline case inventory, local links and bounded static safety checks."""
import hashlib, io, json, re, sys, zipfile
from pathlib import Path


def audit(root):
    records=[]; findings=[]
    patterns={
        'private key':re.compile(rb'-----BEGIN (?:RSA |OPENSSH |EC )?PRIVATE KEY-----'),
        'service credential':re.compile(rb'(?:gh[pousr]_[A-Za-z0-9]{30,}|AKIA[A-Z0-9]{16}|sk-[A-Za-z0-9]{40,})'),
        'private absolute path':re.compile(rb'/(?:home|Users)/[A-Za-z0-9_-]+/'),
        'contact field':re.compile(rb'(?:mailto:|tel:|(?:Email|Phone|Address):\s*\S)',re.I),
    }
    def scan(name,raw,depth=0):
        if depth>3: findings.append({'path':name,'issue':'archive nesting exceeds inspection boundary'});return
        # Licence notices are retained verbatim and separately inventoried.
        if not name.endswith(('DejaVu.txt','Liberation.txt','LICENSE')) and not name.endswith('publication.py'):
            for kind,pattern in patterns.items():
                if pattern.search(raw): findings.append({'path':name,'issue':kind})
        if raw[:2]==b'MZ' or raw[:4]==b'\x7fELF': findings.append({'path':name,'issue':'unexpected executable binary'})
        if raw[:4]==b'PK\x03\x04':
            with zipfile.ZipFile(io.BytesIO(raw)) as z:
                for n in z.namelist():
                    if n.startswith('/') or '..' in Path(n).parts: findings.append({'path':name,'issue':'unsafe archive member'})
                    if n.lower().endswith(('.exe','.dll','.js','.vbs','.bin')): findings.append({'path':name+'!'+n,'issue':'active embedded content'})
                    scan(name+'!'+n,z.read(n),depth+1)
        if name.endswith('.pdf') and re.search(rb'/(?:JavaScript|JS|Launch|EmbeddedFile|OpenAction)\b',raw): findings.append({'path':name,'issue':'active PDF action or attachment'})
    for p in sorted(root.rglob('*')):
        if not p.is_file() or p.name=='publication.json': continue
        rel=p.relative_to(root).as_posix()
        raw=p.read_bytes();scan(rel,raw)
        records.append({'path':rel,'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()})
    md=(root/'README.md').read_text()
    links=re.findall(r'\]\(([^)]+)\)|(?:src|href)="([^"]+)"',md)
    checked=[];external=[]
    for pair in links:
        link=next(x for x in pair if x)
        if link.startswith('https://'): external.append(link);continue
        path=(root/link.split('#')[0]).resolve()
        if not path.is_file(): findings.append({'path':link,'issue':'broken local README link'})
        checked.append(link)
    return {'schema_version':1,'scope':'Exact case folder, including recursive PPTX/XLSX package bytes; local README links.','scanner':'Python standard-library static credential/contact, active-content and archive checks; no signature antivirus engine was available.','inventory':records,'local_links':sorted(set(checked)),'external_links':sorted(set(external)),'findings':findings,'passed':not findings}

if __name__=='__main__':
    root=Path(sys.argv[1]);result=audit(root);print(json.dumps(result,indent=2));sys.exit(0 if result['passed'] else 1)
