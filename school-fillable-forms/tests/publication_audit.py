"""Offline sensitive-data and active-content audit of the delivered case tree.

This is a bounded static payload scan, not a general antivirus service.
"""
import hashlib
import json
import re
import struct
import sys
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET


def audit(root, output):
    files=[]; findings=[]; archives=[]; pngs=[]
    excluded={'proof/publication-review.json','output/publication-audit.json','proof/publication-audit.json'}
    sensitive=[re.compile(x,re.I) for x in (r'-----BEGIN [A-Z ]*PRIVATE KEY-----',r'gh[pousr]_[A-Za-z0-9]{30,}',r'AKIA[A-Z0-9]{16}',r'\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}',r'/home/[^\s<>]+',r'/run/user/\d+')]
    forbidden_names=('vbaproject','activex','embeddings/','customxml/','comments','oleobject')
    for path in sorted(root.rglob('*')):
        if not path.is_file(): continue
        relative=path.relative_to(root).as_posix()
        if relative in excluded: continue
        data=path.read_bytes()
        files.append({'path':relative,'sha256':hashlib.sha256(data).hexdigest(),'bytes':len(data)})
        if '__pycache__' in path.parts: findings.append(relative+': runtime file')
        if data.startswith((b'MZ',b'\x7fELF')): findings.append(relative+': executable binary')
        texts=[]
        if path.suffix=='.docx':
            with zipfile.ZipFile(path) as archive:
                parts=archive.namelist(); archives.append({'path':relative,'parts':parts})
                for name in parts:
                    if any(key in name.lower() for key in forbidden_names) or name.startswith('docProps/'):
                        findings.append(relative+': active content or unwanted property part '+name)
                    content=archive.read(name)
                    if content.startswith((b'MZ',b'\x7fELF',b'\xd0\xcf\x11\xe0')): findings.append(relative+': executable/OLE member')
                    if name.endswith(('.xml','.rels')):
                        text=content.decode(); texts.append(text)
                        tree=ET.fromstring(content)
                        for node in tree.iter():
                            if node.get('TargetMode')=='External': findings.append(relative+': external relationship')
                            if node.tag.split('}')[-1] in ('vanish','webHidden','ins','del'): findings.append(relative+': hidden/revision content')
        elif path.suffix=='.pdf':
            from pypdf import PdfReader
            reader=PdfReader(path); catalog=reader.trailer['/Root']
            if reader.metadata or '/Metadata' in catalog or reader.attachments: findings.append(relative+': PDF metadata or attachment')
            for key in ('/OpenAction','/AA','/OCProperties','/AcroForm'):
                if key in catalog: findings.append(relative+': active or hidden PDF catalog feature '+key)
            for page in reader.pages:
                if page.get('/Annots') or page.get('/AA'): findings.append(relative+': PDF action or annotation')
                texts.append(page.extract_text())
        elif path.suffix=='.png':
            pos=8; chunks=[]
            while pos<len(data):
                length=struct.unpack('>I',data[pos:pos+4])[0]; tag=data[pos+4:pos+8].decode('ascii'); chunks.append(tag); pos+=length+12
                if tag in ('tEXt','iTXt','zTXt','eXIf'): findings.append(relative+': PNG metadata '+tag)
            pngs.append({'path':relative,'chunks':chunks})
        else:
            try: texts=[data.decode('utf-8')]
            except UnicodeDecodeError: findings.append(relative+': unexpected binary type')
        # Dependency copyright records retain upstream legal notices verbatim.
        legal_notice=relative.startswith('output/font-licenses/')
        if not legal_notice and relative != 'tests/publication_audit.py':
            for text in texts:
                if any(pattern.search(text) for pattern in sensitive): findings.append(relative+': sensitive/contact/path pattern')
    result={'schema_version':1,'status':'passed' if not findings else 'failed','scope':'Sensitive-pattern scan plus static OOXML/PDF active-content and PNG metadata audit; current case tree, including decompressed DOCX XML and extracted PDF text. Code publishing read is recorded separately.','limits':['Not a general antivirus engine or guarantee against unknown malware.','Upstream font copyright records are retained verbatim and excluded from contact-pattern matching; signature definitions in this audit script are reviewed separately.','Evidence inventories exclude their own audit/review files to avoid recursive hashes.','Live URLs are not fetched in the offline run.'],'excluded_self_evidence':sorted(excluded),'findings':findings,'files':files,'docx_packages':archives,'pngs':pngs}
    output.write_text(json.dumps(result,indent=2)+'\n')
    if findings: raise ValueError('Publication audit failed: '+'; '.join(findings))
    print('PASS: sensitive-pattern, archive active-content, PDF metadata/action and PNG metadata scans')


if __name__=='__main__': audit(Path(sys.argv[1]),Path(sys.argv[2]))
