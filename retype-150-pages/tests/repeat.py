"""Compare two independent runs, including paths containing spaces."""
import json,sys,zipfile
from pathlib import Path
sys.path.insert(0,'/case/source')
from common import sha,write_json,docx_pages,normalized
from pypdf import PdfReader
first,second,dest=map(Path,sys.argv[1:4])
a=json.loads((first/'report.json').read_text()); b=json.loads((second/'report.json').read_text())
keys=['schema_version','case','input_hashes','transformations','counts','checks','tools','uncertainties','human_steps','accuracy']
checks={
 'docx_text_and_structure':docx_pages(first/'retyped.docx')==docx_pages(second/'retyped.docx'),
 'pdf_text':normalized(' '.join(p.extract_text() or '' for p in PdfReader(first/'preview.pdf').pages))==normalized(' '.join(p.extract_text() or '' for p in PdfReader(second/'preview.pdf').pages)),
 'page_map':(first/'pages.json').read_bytes()==(second/'pages.json').read_bytes(),
 'report_facts':all(a[k]==b[k] for k in keys),
 'accuracy':(first/'accuracy.json').read_bytes()==(second/'accuracy.json').read_bytes(),
}
checks['docx_bytes_equal']=sha(first/'retyped.docx')==sha(second/'retyped.docx')
checks['pdf_bytes_equal']=sha(first/'preview.pdf')==sha(second/'preview.pdf')
write_json(dest,{'schema_version':1,'scope':'Two complete independent runs over the full corpus. Second run uses input and output paths containing spaces. Timestamps and archive ordering may differ; measured report facts and document content must agree.','checks':checks,'input_hashes':a['input_hashes'],'first_output_hashes':{n:sha(first/n) for n in ('retyped.docx','preview.pdf','pages.json')},'second_output_hashes':{n:sha(second/n) for n in ('retyped.docx','preview.pdf','pages.json')}})
if not all(checks[k] for k in ('docx_text_and_structure','pdf_text','page_map','report_facts','accuracy')):raise SystemExit('FAIL: repeatability')
print('PASS: repeatability of the full corpus; document content and report facts agree')
