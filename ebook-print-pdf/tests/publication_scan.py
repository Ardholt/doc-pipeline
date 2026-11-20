"""Inventory and static checks for the case tree."""
import hashlib, json, re, sys
from pathlib import Path
from PIL import Image
from pypdf import PdfReader
from pypdf.generic import IndirectObject

root=Path(sys.argv[1]);dest=Path(sys.argv[2]);files=[];issues=[]
private=[b'/home/',b'BEGIN PRIVATE KEY',b'BEGIN RSA PRIVATE KEY']
secret_patterns=[rb'AKIA[0-9A-Z]{16}',rb'ghp_[A-Za-z0-9]{36}',rb'sk-[A-Za-z0-9]{32,}']
for path in sorted(root.rglob('*')):
    if not path.is_file() or path==dest or path.name=='publication-scan.json':continue
    rel=str(path.relative_to(root));data=path.read_bytes()
    files.append({'path':rel,'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()})
    if any(x.startswith('.') for x in path.relative_to(root).parts):issues.append({'path':rel,'issue':'unexpected hidden file'})
    if data.startswith((b'MZ',b'\x7fELF')):issues.append({'path':rel,'issue':'unexpected executable binary'})
    if path.name!='publication_scan.py':
        if any(v in data for v in private) or any(re.search(p,data) for p in secret_patterns):issues.append({'path':rel,'issue':'private marker or secret-shaped content'})
    if path.suffix=='.pdf':
        r=PdfReader(path)
        if r.metadata is not None or '/Metadata' in r.trailer['/Root']:issues.append({'path':rel,'issue':'PDF metadata'})
        if r.attachments or '/OpenAction' in r.trailer['/Root']:issues.append({'path':rel,'issue':'PDF active content or attachment'})
        forbidden={'/JS','/JavaScript','/Launch','/RichMedia','/AA','/EmbeddedFile','/AcroForm'}
        seen=set()
        def walk(obj):
            if isinstance(obj,IndirectObject):
                key=(obj.idnum,obj.generation)
                if key in seen:return
                seen.add(key);obj=obj.get_object()
            if isinstance(obj,dict):
                for key,value in obj.items():
                    if str(key) in forbidden:issues.append({'path':rel,'issue':'active PDF object: '+str(key)})
                    walk(value)
            elif isinstance(obj,list):
                for value in obj:walk(value)
        for generation,entries in r.xref.items():
            for object_id in entries:
                if object_id:walk(IndirectObject(object_id,generation,r))
        for pg in r.pages:
            for a in pg.get('/Annots',[]):
                a=a.get_object()
                if a.get('/Subtype')!='/Link' or a.get('/A',{}).get('/S') not in (None,'/URI','/GoTo'):issues.append({'path':rel,'issue':'unexpected annotation action'})
    elif path.suffix=='.png':
        im=Image.open(path)
        if im.info:issues.append({'path':rel,'issue':'PNG ancillary metadata','keys':list(im.info)})
    elif path.suffix=='.html':
        scripts=re.findall(rb'<script\b([^>]*)>',data,re.I)
        if any(b'https://static.cloudflareinsights.com/beacon.min.js' not in attrs for attrs in scripts):issues.append({'path':rel,'issue':'unexpected HTML script'})
        if re.search(rb'<(?:iframe|object|embed)\b|\bon(?:load|error|click)\s*=',data,re.I):issues.append({'path':rel,'issue':'active HTML element or handler'})
    elif path.suffix=='.svg':
        if re.search(rb'<\s*(script|foreignObject)|<!ENTITY|(?:href\s*=)',data,re.I):issues.append({'path':rel,'issue':'active SVG/resource reference'})
    if path.suffix in ('.md','.json','.html','.svg','.py','.sh','.yml') and path.name!='publication_scan.py':
        if re.search(rb'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b',data):issues.append({'path':rel,'issue':'email-shaped content'})
result={'schema_version':1,'scope':'Case files; hashes exclude this self-referential report. Static secret/privacy and active-content malware checks, plus PDF/PNG internals. No signature antivirus engine was available to this case scan.','status':'PASS' if not issues else 'FAIL','files':files,'issues':issues,'manual_read':'README, manuscript, source, layout and test code reviewed; document/page renders reviewed separately in visual-review.json.'}
dest.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(result['status']+': publication scan; '+str(len(files))+' files; '+str(len(issues))+' issues')
if issues:sys.exit(1)
