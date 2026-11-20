"""Ensure the existing-output checks reject damaged values, links and pages."""
import json
import sys
import tempfile
import zipfile
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'source'))
from forms import load_inputs, write_json, write_zip
from check import check_docx, pdf_words
from pypdf import PdfReader, PdfWriter


def main(indir, out):
    spec, values = load_inputs(indir); checks = []
    def rejected(name, action):
        try: action()
        except ValueError as exc:
            checks.append({'name': name, 'passed': True, 'diagnostic': str(exc)}); return
        raise ValueError('Damaged output accepted: ' + name)
    form = spec['forms'][0]; fid = form['id']
    with tempfile.TemporaryDirectory(prefix='damage-check-') as directory:
        temp = Path(directory)
        with zipfile.ZipFile(out / (fid + '-filled.docx')) as z: parts = {n:z.read(n) for n in z.namelist()}
        text_field = next(f for f in form['fields'] if f['type']=='text' and values[fid].get(f['id']))
        # Change an actual entered value in a copy, then inspect it against the independent JSON input.
        from xml.etree import ElementTree as ET
        from forms import NS, W, xml
        root = ET.fromstring(parts['word/document.xml'])
        for sdt in root.findall('.//w:sdt', NS):
            t=sdt.find('.//w:t',NS)
            if t is not None and t.text and t.text in values[fid][text_field['id']]:
                t.text='Changed answer'; break
        altered=dict(parts); altered['word/document.xml']=xml(root)
        path=temp/'changed-value.docx'; write_zip(path, altered)
        rejected('changed saved field value', lambda: check_docx(path, form, values[fid]))
        altered=dict(parts)
        root=ET.fromstring(altered['_rels/.rels'])
        ET.SubElement(root,'{http://schemas.openxmlformats.org/package/2006/relationships}Relationship',{'Id':'external','Type':'http://schemas.openxmlformats.org/officeDocument/2006/relationships/hyperlink','Target':'https://invalid.example.invalid/','TargetMode':'External'})
        altered['_rels/.rels']=xml(root); path=temp/'external-link.docx'; write_zip(path,altered)
        rejected('injected external document link', lambda: check_docx(path, form, values[fid]))
        reader=PdfReader(out/(fid+'-filled.pdf'))
        writer=PdfWriter(); writer.add_page(reader.pages[0]); writer.add_page(reader.pages[0]); writer.metadata=None
        path=temp/'extra-page.pdf'
        with path.open('wb') as stream: writer.write(stream)
        rejected('extra rendered page',lambda:pdf_words(path))
        writer=PdfWriter(); writer.add_blank_page(width=300,height=400); writer.metadata=None
        path=temp/'wrong-page.pdf'
        with path.open('wb') as stream: writer.write(stream)
        rejected('damaged page geometry',lambda:pdf_words(path))
    write_json(out/'rendered-negative.json',{'schema_version':1,'checks':checks,'passed':len(checks)})
    print('PASS: damaged saved value, external link and rendered pages rejected')


if __name__=='__main__': main(Path(sys.argv[1]),Path(sys.argv[2]))
