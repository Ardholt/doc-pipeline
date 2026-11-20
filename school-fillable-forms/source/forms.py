"""Validate the public schema and create metadata-free DOCX content controls."""
import hashlib
import json
import re
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET

W = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
W14 = 'http://schemas.microsoft.com/office/word/2010/wordml'
NS = {'w': W, 'w14': W14}
ET.register_namespace('w', W)
ET.register_namespace('w14', W14)

def need(ok, message):
    if not ok:
        raise ValueError(message)

def load_inputs(directory):
    directory = Path(directory)
    try:
        spec = json.loads((directory / 'forms.json').read_text(encoding='utf-8'))
        values = json.loads((directory / 'values.json').read_text(encoding='utf-8'))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise ValueError('forms.json and values.json must be readable UTF-8 JSON: ' + str(exc).split(':')[0]) from exc
    validate(spec, values)
    return spec, values

def safe_text(value, limit, context, empty=False):
    need(isinstance(value, str), context + ': expected a string')
    need((empty or bool(value.strip())) and len(value) <= limit, context + ': empty or too long')
    need(not any(ord(c) < 32 and c != '\n' for c in value), context + ': unsupported control character')
    need(not any(0xD800 <= ord(c) <= 0xDFFF for c in value), context + ': unsupported Unicode surrogate')

def identifier(value, context):
    need(isinstance(value, str) and re.fullmatch(r'[a-z][a-z0-9-]{0,39}', value), context + ': use lowercase ASCII IDs, at most 40 characters')

def validate(spec, values):
    need(isinstance(spec, dict) and type(spec.get('schema_version')) is int and spec['schema_version'] == 1, 'forms.json: schema_version must be 1')
    forms = spec.get('forms')
    need(isinstance(forms, list) and 1 <= len(forms) <= 20, 'forms.json: expected 1 to 20 forms')
    need(isinstance(values, dict), 'values.json: expected an object keyed by form ID')
    form_ids = set()
    for form in forms:
        need(isinstance(form, dict), 'form: expected an object')
        fid = form.get('id'); identifier(fid, 'form ID')
        need(fid not in form_ids, 'duplicate form ID: ' + fid); form_ids.add(fid)
        safe_text(form.get('title'), 55, fid + ' title')
        safe_text(form.get('instructions'), 180, fid + ' instructions')
        need('\n' not in form['title'] and '\n' not in form['instructions'], fid + ': title and instructions must be single paragraphs')
        fields = form.get('fields')
        need(isinstance(fields, list) and 1 <= len(fields) <= 6, fid + ': expected 1 to 6 fields')
        need(fid in values and isinstance(values[fid], dict), fid + ': values object is missing')
        field_ids = set()
        for field in fields:
            need(isinstance(field, dict), fid + ': field must be an object')
            key = field.get('id'); identifier(key, fid + ' field ID')
            need(key not in field_ids, fid + ': duplicate field ID ' + key); field_ids.add(key)
            safe_text(field.get('label'), 60, fid + '/' + key + ' label')
            need('\n' not in field['label'], fid + '/' + key + ': label must be one line')
            need(type(field.get('required')) is bool, fid + '/' + key + ': required must be boolean')
            need(field.get('type') in ('text', 'checkbox'), fid + '/' + key + ': unsupported field type')
            need(key in values[fid] or not field['required'], fid + '/' + key + ': required value is missing')
            value = values[fid].get(key, '' if field['type'] == 'text' else False)
            if field['type'] == 'text':
                maximum = field.get('max_chars')
                need(type(maximum) is int and 1 <= maximum <= 160, fid + '/' + key + ': max_chars must be an integer from 1 to 160')
                safe_text(value, maximum, fid + '/' + key, empty=not field['required'])
                need(value.count('\n') <= 3, fid + '/' + key + ': at most four explicit lines')
            else:
                need('max_chars' not in field, fid + '/' + key + ': checkbox must omit max_chars')
                need(type(value) is bool, fid + '/' + key + ': expected a boolean')
        need(set(values[fid]) <= field_ids, fid + ': unknown field in values.json')
    need(set(values) == form_ids, 'values.json: unknown form ID')

def value_for(field, values):
    return values.get(field['id'], '' if field['type'] == 'text' else False)

def el(name, attrs=None, parent=None):
    prefix, local = name.split(':')
    node = ET.Element('{' + NS[prefix] + '}' + local)
    for key, value in (attrs or {}).items():
        p, k = key.split(':'); node.set('{' + NS[p] + '}' + k, str(value))
    if parent is not None: parent.append(node)
    return node

def run(parent, text, bold=False, size=22, colour='183B45'):
    r = el('w:r', parent=parent); pr = el('w:rPr', parent=r)
    el('w:rFonts', {'w:ascii': 'DejaVu Sans', 'w:hAnsi': 'DejaVu Sans', 'w:cs': 'DejaVu Sans'}, pr)
    el('w:sz', {'w:val': size}, pr); el('w:color', {'w:val': colour}, pr)
    if bold: el('w:b', parent=pr)
    for i, line in enumerate(text.split('\n')):
        if i: el('w:br', parent=r)
        t = el('w:t', parent=r); t.set('{http://www.w3.org/XML/1998/namespace}space', 'preserve'); t.text = line
    return r

def paragraph(parent, text=None, bold=False, size=22, before=0, after=100):
    p = el('w:p', parent=parent); pr = el('w:pPr', parent=p)
    el('w:spacing', {'w:before': before, 'w:after': after, 'w:line': max(280, size * 12), 'w:lineRule': 'exact'}, pr)
    if text is not None: run(p, text, bold, size)
    return p

def xml(node):
    return ET.tostring(node, encoding='utf-8', xml_declaration=True)

def make_blank(form, target):
    doc = el('w:document'); body = el('w:body', parent=doc)
    paragraph(body, 'SCHOOL OFFICE  /  ' + form['id'].upper(), size=18, after=180)
    paragraph(body, form['title'], bold=True, size=36, after=220)
    paragraph(body, form['instructions'], size=20, after=220)
    for index, field in enumerate(form['fields'], 1):
        label = field['label'] + (' *' if field['required'] else '')
        paragraph(body, label, bold=True, before=140, after=100)
        table = el('w:tbl', parent=body); pr = el('w:tblPr', parent=table)
        el('w:tblW', {'w:w': 9638, 'w:type': 'dxa'}, pr)
        el('w:tblLayout', {'w:type': 'fixed'}, pr)
        margins = el('w:tblCellMar', parent=pr)
        for edge in ('top', 'left', 'bottom', 'right'):
            el('w:' + edge, {'w:w': 160, 'w:type': 'dxa'}, margins)
        borders = el('w:tblBorders', parent=pr)
        for edge in ('top', 'left', 'bottom', 'right'):
            el('w:' + edge, {'w:val': 'single', 'w:sz': 6, 'w:color': '9BB8C0'}, borders)
        grid = el('w:tblGrid', parent=table); el('w:gridCol', {'w:w': 9638}, grid)
        row = el('w:tr', parent=table); rp = el('w:trPr', parent=row)
        el('w:cantSplit', parent=rp)
        el('w:trHeight', {'w:val': 1400 if field['type'] == 'text' else 620, 'w:hRule': 'exact'}, rp)
        cell = el('w:tc', parent=row); cp = el('w:tcPr', parent=cell)
        el('w:tcW', {'w:w': 9638, 'w:type': 'dxa'}, cp)
        el('w:shd', {'w:fill': 'EFF5F6', 'w:val': 'clear'}, cp)
        p = paragraph(cell, after=0)
        sdt = el('w:sdt', parent=p); props = el('w:sdtPr', parent=sdt)
        el('w:id', {'w:val': index}, props)
        el('w:alias', {'w:val': field['label']}, props)
        el('w:tag', {'w:val': field['id']}, props)
        content = el('w:sdtContent', parent=sdt)
        if field['type'] == 'checkbox':
            cb = el('w14:checkbox', parent=props)
            el('w14:checked', {'w14:val': 0}, cb)
            el('w14:checkedState', {'w14:val': '2612', 'w14:font': 'DejaVu Sans'}, cb)
            el('w14:uncheckedState', {'w14:val': '2610', 'w14:font': 'DejaVu Sans'}, cb)
            run(content, '☐', size=28)
        else:
            el('w:showingPlcHdr', parent=props)
            run(content, 'Select here to type', colour='526B72')
    paragraph(body, 'Save the completed DOCX. Use the PDF for viewing or printing.', size=18, before=240)
    sect = el('w:sectPr', parent=body)
    el('w:pgSz', {'w:w': 11906, 'w:h': 16838}, sect)
    el('w:pgMar', {'w:top': 1000, 'w:right': 1134, 'w:bottom': 1000, 'w:left': 1134, 'w:header': 0, 'w:footer': 0, 'w:gutter': 0}, sect)
    parts = {
        '[Content_Types].xml': b'<?xml version="1.0" encoding="UTF-8"?><Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="xml" ContentType="application/xml"/><Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/></Types>',
        '_rels/.rels': b'<?xml version="1.0" encoding="UTF-8"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/></Relationships>',
        'word/document.xml': xml(doc),
    }
    write_zip(target, parts)

def write_zip(target, parts):
    with zipfile.ZipFile(target, 'w', compression=zipfile.ZIP_DEFLATED) as z:
        for name, data in sorted(parts.items()):
            info = zipfile.ZipInfo(name, (2000, 1, 1, 0, 0, 0)); info.compress_type = zipfile.ZIP_DEFLATED
            z.writestr(info, data)

def clean_docx(path):
    with zipfile.ZipFile(path) as z: parts = {name: z.read(name) for name in z.namelist()}
    removed = {name for name in parts if name.startswith('docProps/')}
    for name in removed: del parts[name]
    for name in list(parts):
        if name.endswith('.rels') or name == '[Content_Types].xml':
            root = ET.fromstring(parts[name])
            for node in list(root):
                target = node.get('Target', '').lstrip('/')
                if target.startswith('docProps/') or node.get('PartName', '').lstrip('/') in removed:
                    root.remove(node)
            ET.register_namespace('', root.tag.split('}')[0][1:])
            parts[name] = xml(root)
    write_zip(path, parts)

def content_text(node):
    return ''.join(n.text or '' if n.tag == '{' + W + '}t' else '\n' for n in node.iter() if n.tag in ('{' + W + '}t', '{' + W + '}br'))

def inspect_docx(path):
    with zipfile.ZipFile(path) as z:
        root = ET.fromstring(z.read('word/document.xml'))
        records = []
        sdts = root.findall('.//w:sdt', NS)
        for sdt in sdts:
            # Writer exports legacy container wrappers around some leaf controls.
            # Count the actual leaf fields and retain the full XML node count too.
            if sdt.find('.//w:sdt', NS) is not None:
                continue
            props = sdt.find('w:sdtPr', NS)
            checkbox = props.find('w14:checkbox', NS)
            alias = props.find('w:alias', NS); tag = props.find('w:tag', NS)
            state = None if checkbox is None else checkbox.find('w14:checked', NS)
            records.append({'type': 'text' if checkbox is None else 'checkbox', 'label': None if alias is None else alias.get('{' + W + '}val'), 'id': None if tag is None else tag.get('{' + W + '}val'), 'text': content_text(sdt.find('w:sdtContent', NS)), 'checked': None if state is None else state.get('{' + W14 + '}val') in ('1', 'true')})
        return {'controls': records, 'xml_sdt_nodes': len(sdts), 'container_wrappers': len(sdts) - len(records), 'text': content_text(root), 'rows': [n.attrib for n in root.findall('.//w:trHeight', NS)], 'parts': z.namelist()}

def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def write_json(path, data):
    Path(path).write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
