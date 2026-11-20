"""Inspect existing files independently of conversion; a mismatch is a failure."""
import json
import re
import subprocess
import sys
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'source'))
from forms import NS, W, inspect_docx, load_inputs, need, sha, value_for


def normalize(value): return ' '.join(value.split())


def check_docx(path, form, values=None):
    actual = inspect_docx(path)
    need(len(actual['controls']) == len(form['fields']), path.name + ': control count changed')
    for position, (field, control) in enumerate(zip(form['fields'], actual['controls'])):
        need(control['type'] == field['type'], path.name + ': control type changed')
        need(field['label'] in actual['text'], path.name + ': field label is missing')
        need(control['label'] in (None, field['label']), path.name + ': control alias changed')
        need(control['id'] in (None, field['id']), path.name + ': control tag changed')
        if values is not None:
            expected = value_for(field, values)
            found = control['checked'] if field['type'] == 'checkbox' else control['text']
            need(found == expected, path.name + ': value mismatch for ' + field['id'])
        elif field['type'] == 'checkbox':
            need(control['checked'] is False, path.name + ': blank checkbox is selected')
        else: need(control['text'] == 'Select here to type', path.name + ': blank text was changed')
    need(form['title'] in actual['text'] and form['instructions'] in actual['text'], path.name + ': heading or instructions changed')
    need(len(actual['rows']) == len(form['fields']), path.name + ': layout row count changed')
    for field, row in zip(form['fields'], actual['rows']):
        need(row.get('{' + W + '}hRule') == 'exact', path.name + ': fixed row height lost')
        need(int(row['{' + W + '}val']) == (1400 if field['type'] == 'text' else 620), path.name + ': row height changed')
    with zipfile.ZipFile(path) as z:
        need(not any(n.startswith(('docProps/', 'word/embeddings/', 'word/activeX/')) or any(s in n.lower() for s in ('vbaproject', 'comments', 'customxml', 'thumbnail')) for n in z.namelist()), path.name + ': unwanted metadata or embedded content')
        for name in z.namelist():
            if name.endswith('.rels'):
                for rel in ET.fromstring(z.read(name)):
                    need(rel.get('TargetMode') != 'External', path.name + ': external relationship')
            if name.endswith('.xml'):
                root = ET.fromstring(z.read(name))
                for tag in ('vanish', 'webHidden', 'del', 'ins'):
                    need(root.find('.//w:' + tag, NS) is None, path.name + ': hidden text or revisions')
    return actual


def pdf_words(path):
    from pypdf import PdfReader
    pdf = PdfReader(path)
    need(len(pdf.pages) == 1, path.name + ': expected one page')
    need(not pdf.metadata, path.name + ': PDF Info metadata remains')
    need('/Metadata' not in pdf.trailer['/Root'], path.name + ': XMP metadata remains')
    need(not pdf.attachments, path.name + ': attachments found')
    need(not pdf.pages[0].get('/Annots'), path.name + ': annotations found')
    need(abs(float(pdf.pages[0].mediabox.width) - 595.3) < 1 and abs(float(pdf.pages[0].mediabox.height) - 841.9) < 1, path.name + ': page geometry changed')
    output = subprocess.check_output(['pdftotext', '-bbox', str(path), '-'], text=True, timeout=30)
    root = ET.fromstring(output)
    words = [{'text': n.text or '', **{k: float(n.get(k)) for k in ('xMin', 'xMax', 'yMin', 'yMax')}} for n in root.iter() if n.tag.endswith('}word')]
    for word in words:
        need(45 <= word['xMin'] < word['xMax'] <= 552 and 40 <= word['yMin'] < word['yMax'] <= 802, path.name + ': text outside safe area')
    fonts = subprocess.check_output(['pdffonts', str(path)], text=True, timeout=30).splitlines()[2:]
    need(bool(fonts), path.name + ': no fonts found')
    for font in fonts:
        columns = font.split()
        need(len(columns) >= 8 and columns[-5] == 'yes', path.name + ': unembedded font')
    return pdf, words


def locate(words, phrase):
    tokens = phrase.split()
    for i in range(len(words) - len(tokens) + 1):
        if [w['text'] for w in words[i:i + len(tokens)]] == tokens: return words[i:i + len(tokens)]
    raise ValueError('Rendered text missing: ' + phrase)


def check_all(indir, outdir, hashes=True):
    spec, values = load_inputs(indir); out = Path(outdir); measured = []
    for form in spec['forms']:
        fid = form['id']; views = {}
        for mode in ('blank', 'filled'):
            docx = out / (fid + '-' + mode + '.docx')
            check_docx(docx, form, values[fid] if mode == 'filled' else None)
            pdf, words = pdf_words(out / (fid + '-' + mode + '.pdf'))
            views[mode] = words
            text = normalize(pdf.pages[0].extract_text())
            need(normalize(form['title']) in text and normalize(form['instructions']) in text, fid + ': PDF lost title or instructions')
            for field in form['fields']:
                label = locate(words, field['label'])
                if mode == 'filled' and field['type'] == 'text':
                    value = value_for(field, values[fid])
                    need(normalize(value) in text, fid + ': PDF lost field value')
                    for line in value.split('\n'):
                        if not line: continue
                        found = locate(words, line)
                        need(all(label[-1]['yMax'] <= w['yMin'] and w['yMax'] <= label[-1]['yMax'] + 78 for w in found), fid + ': value exceeds its fixed text area')
        drift = 0
        for field in form['fields']:
            a = locate(views['blank'], field['label'])[0]; b = locate(views['filled'], field['label'])[0]
            drift = max(drift, abs(a['yMin'] - b['yMin']), abs(a['xMin'] - b['xMin']))
        need(drift <= 0.5, fid + ': surrounding labels moved by more than 0.5 pt')
        measured.append({'form': fid, 'blank_pages': 1, 'filled_pages': 1, 'controls': len(form['fields']), 'label_position_drift_pt': round(drift, 4)})
    if hashes:
        report = json.loads((out / 'report.json').read_text())
        for name, digest in report['input_hashes'].items(): need(sha(Path(indir) / name) == digest, 'input hash changed: ' + name)
        for name, digest in report['output_hashes'].items(): need(sha(out / name) == digest, 'output hash changed: ' + name)
        need(report['counts']['forms'] == len(measured), 'report form count differs')
        need(report['measurements'] == measured, 'report measurements differ')
    return measured


if __name__ == '__main__':
    try:
        result = check_all(sys.argv[1], sys.argv[2])
        print('PASS: existing DOCX controls, values, labels, fixed rows, PDF content, geometry, fonts, metadata and hashes')
    except Exception as exc:
        print('FAIL: ' + str(exc), file=sys.stderr); sys.exit(1)
