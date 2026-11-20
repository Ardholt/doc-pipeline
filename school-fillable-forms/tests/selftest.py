"""Schema and damaged-document tests; stdlib only, no conversion required."""
import copy
import json
import sys
import tempfile
import zipfile
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'source'))
from forms import load_inputs, make_blank, validate, write_json, write_zip
from check import check_docx


def main():
    case = Path(__file__).resolve().parents[1]
    spec, values = load_inputs(case / 'input')
    checks = []
    def reject(name, action):
        try: action()
        except (ValueError, KeyError, FileNotFoundError):
            checks.append({'name': name, 'passed': True}); return
        raise AssertionError(name + ': damage was accepted')
    mutations = [
        ('unsupported schema', lambda s,v: s.update(schema_version=2)),
        ('boolean schema', lambda s,v: s.update(schema_version=True)),
        ('unknown field type', lambda s,v: s['forms'][0]['fields'][0].update(type='date')),
        ('duplicate form ID', lambda s,v: s['forms'].append(copy.deepcopy(s['forms'][0]))),
        ('duplicate field ID', lambda s,v: s['forms'][0]['fields'].append(copy.deepcopy(s['forms'][0]['fields'][0]))),
        ('path traversal ID', lambda s,v: s['forms'][0].update(id='../outside')),
        ('overlong text', lambda s,v: v['trip-permission'].update(activity='x'*81)),
        ('too many lines', lambda s,v: v['trip-permission'].update(arrangements='a\nb\nc\nd\ne')),
        ('wrong checkbox value', lambda s,v: v['trip-permission'].update(permission='yes')),
        ('missing required value', lambda s,v: v['trip-permission'].pop('activity')),
        ('unknown supplied field', lambda s,v: v['trip-permission'].update(extra='text')),
        ('unsupported maximum', lambda s,v: s['forms'][0]['fields'][0].update(max_chars=999)),
        ('checkbox maximum', lambda s,v: s['forms'][0]['fields'][2].update(max_chars=10)),
        ('control characters', lambda s,v: v['trip-permission'].update(activity='bad\x01value')),
    ]
    for name, change in mutations:
        s, v = copy.deepcopy(spec), copy.deepcopy(values); change(s,v)
        reject(name, lambda: validate(s,v))
    with tempfile.TemporaryDirectory(prefix='form-check-') as directory:
        root = Path(directory)
        reject('missing inputs', lambda: load_inputs(root))
        form = spec['forms'][0]; path = root / 'blank.docx'; make_blank(form, path)
        check_docx(path, form)
        first = path.read_bytes(); make_blank(form, path)
        assert first == path.read_bytes(), 'DOCX generation is not deterministic'
        checks.append({'name': 'deterministic DOCX generation and valid controls', 'passed': True})
        with zipfile.ZipFile(path) as z: parts = {n: z.read(n) for n in z.namelist()}
        original = parts['word/document.xml']
        for name, before, after in [
            ('damaged control', b'w:sdt>', b'w:removed>'),
            ('missing label', b'Travel arrangements', b'Travel deleted'),
            ('changed fixed row', b'w:val="1400"', b'w:val="100"'),
            ('selected blank checkbox', b'w14:val="0"', b'w14:val="1"'),
            ('changed blank value', b'Select here to type', b'Damaged value'),
        ]:
            altered = dict(parts); altered['word/document.xml'] = original.replace(before, after)
            write_zip(path, altered)
            reject(name, lambda: check_docx(path, form))
        altered = dict(parts)
        altered['_rels/.rels'] = altered['_rels/.rels'].replace(b'Target="word/document.xml"', b'Target="https://invalid.example.invalid/" TargetMode="External"')
        write_zip(path, altered)
        reject('external relationship', lambda: check_docx(path, form))
    result = {'schema_version': 1, 'scope': 'stdlib schema and OOXML checks; no LibreOffice or rendered PDF validation', 'checks': checks, 'passed': len(checks)}
    if '--output' in sys.argv:
        target = Path(sys.argv[sys.argv.index('--output') + 1]); target.mkdir(parents=True, exist_ok=True)
        write_json(target / 'selftest.json', result)
    print('PASS: ' + str(len(checks)) + ' schema, determinism and damaged-document checks')


if __name__ == '__main__': main()
