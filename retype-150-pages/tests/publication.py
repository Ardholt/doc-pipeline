"""Inventory and inspect publication files, including document package internals."""
import hashlib,json,re,sys,zipfile
from pathlib import Path
from xml.etree import ElementTree as ET
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'source'))
from common import sha,write_json

case=Path(sys.argv[1]).resolve(); destination=Path(sys.argv[2])
ignored={'__pycache__'}; findings=[]; inventory=[]; links=[]
patterns={
 'private_key':rb'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----',
 'service_token':rb'(?:gh[pousr]_[A-Za-z0-9]{30,}|AKIA[A-Z0-9]{16})',
 'private_path':rb'/(?:home|Users|var/lib)/[A-Za-z0-9_.-]+/',
}
for p in sorted(case.rglob('*')):
    if not p.is_file() or p==destination or any(x in ignored for x in p.parts):continue
    rel=str(p.relative_to(case))
    if rel.startswith('generated/') or p.suffix=='.log' and p.parent==case:continue
    data=p.read_bytes(); inventory.append({'path':rel,'sha256':sha(p),'bytes':len(data)})
    # The scanner's literal signatures are not document findings.
    if p.name!='publication.py' and p.suffix in ('.md','.json','.csv','.txt','.html','.py','.sh','.yml','.env'):
        for name,pattern in patterns.items():
            if re.search(pattern,data,re.I):findings.append({'file':rel,'issue':name})
        if p.suffix=='.md':
            text=data.decode('utf-8')
            for url in re.findall(r'\]\(([^)]+)\)',text):
                if url.startswith(('https://','http://','#')):continue
                target=(p.parent/url.split('#')[0]).resolve()
                links.append({'source':rel,'target':url,'exists':target.exists()})
                if not target.exists():findings.append({'file':rel,'issue':'unresolved relative link','target':url})
    if p.suffix=='.docx':
        with zipfile.ZipFile(p) as z:
            for n in z.namelist():
                if n.startswith('/') or '..' in Path(n).parts or re.search(r'(?:vbaProject|activeX|embeddings/|customXml/|comments\.xml)',n,re.I):findings.append({'file':rel,'issue':'active or unexpected DOCX package part'})
                if n.endswith('.rels') and b'TargetMode="External"' in z.read(n):findings.append({'file':rel,'issue':'external document link'})
            if any(n.startswith('docProps/') for n in z.namelist()):findings.append({'file':rel,'issue':'document properties'})
    if p.suffix=='.pdf':
        from pypdf import PdfReader
        reader=PdfReader(p)
        if reader.metadata or '/Metadata' in reader.trailer['/Root']:findings.append({'file':rel,'issue':'PDF metadata'})
        active=[]; seen=set()
        def visit(obj):
            try:obj=obj.get_object()
            except AttributeError:pass
            identity=id(obj)
            if identity in seen:return
            seen.add(identity)
            if isinstance(obj,dict):
                for key,value in obj.items():
                    if key in ('/JavaScript','/JS','/OpenAction','/AA','/Launch','/EmbeddedFiles','/RichMedia','/XFA'):active.append(str(key))
                    if key not in ('/Parent','/P'):visit(value)
            elif isinstance(obj,list):
                for child in obj:visit(child)
        visit(reader.trailer['/Root'])
        if active:findings.append({'file':rel,'issue':'active PDF content','keys':sorted(set(active))})
    if p.suffix=='.png':
        from PIL import Image
        if Image.open(p).info:findings.append({'file':rel,'issue':'PNG metadata'})
report={'schema_version':1,'scope':'Current case publication tree; source, text assets and ZIP/PDF/PNG internals. Read-only inventory; excludes this self-referential report and temporary generation files.','checks':['Secret signature and private-path scan','Relative Markdown link resolution','DOCX executable/embedded/external content and properties','PDF active-content graph and metadata','PNG ancillary metadata'],'malware_scan':'Structural active-content scan plus source read. Separate signature-based scanner outcome and database version are retained in proof/antivirus.log; this report does not substitute for that run.','inventory':inventory,'relative_links':links,'findings':findings,'status':'passed' if not findings else 'failed'}
write_json(destination,report)
print(('PASS' if not findings else 'FAIL')+f': publication scan; {len(inventory)} files; {len(findings)} findings')
if findings:
 print(json.dumps(findings,indent=2));sys.exit(1)
