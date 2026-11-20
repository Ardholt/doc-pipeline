"""Offline document workload using the shared harness evidence contract."""
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path
from forms import clean_docx, inspect_docx, load_inputs, make_blank, sha, write_json

SOURCE = Path(__file__).resolve().parent
CASE = SOURCE.parent
sys.path.insert(0, str(CASE / 'tests'))
from check import check_all


def command(args, timeout=180):
    try:
        return subprocess.check_output(args, text=True, stderr=subprocess.STDOUT, timeout=timeout).strip()
    except subprocess.CalledProcessError as exc:
        raise RuntimeError('Command failed: ' + Path(args[0]).name + '\n' + exc.output) from exc


def clean_pdf(path):
    from pypdf import PdfReader, PdfWriter
    reader = PdfReader(path); writer = PdfWriter()
    for page in reader.pages: writer.add_page(page)
    writer.metadata = None
    with path.open('wb') as f: writer.write(f)


def make_preview(out, fid):
    from PIL import Image, ImageChops
    # First-screen image: the whole filled form page as rendered by Poppler, cut below its last content so
    # the empty lower part of the sheet is not shown. Nothing is redrawn.
    image = Image.open(out / (fid + '-filled.png')).convert('RGB')
    ink = ImageChops.invert(image.convert('L')).point(lambda v: 255 if v > 24 else 0).getbbox() or (0, 0, image.width, image.height)
    bottom = min(image.height, ink[3] + 60)
    image.crop((0, 0, image.width, bottom)).save(out / 'hero.png')
    write_json(out / 'preview-map.json', {'schema_version': 1, 'source': fid + '-filled.png', 'source_pdf': fid + '-filled.pdf', 'crop_pixels': [0, 0, image.width, bottom], 'crop': 'full page width, from the top edge to 60 px below the last content; the empty lower part of the sheet is left out'})


def main(indir, out):
    started = time.monotonic(); out.mkdir(parents=True, exist_ok=True)
    runtime = {'schema_version': 1, 'scope': 'offline workload and checks; excludes image build and manual review', 'limits': {'cpus': 2, 'memory_gib': 2, 'workload_timeout_seconds': 1080}, 'status': 'failed'}
    try:
        if any(p.is_symlink() for p in out.rglob('*')):
            raise ValueError('output directory must not contain symbolic links')
        spec, values = load_inputs(indir)
        input_hashes = {name: sha(indir / name) for name in ('forms.json', 'values.json')}
        records = []
        with tempfile.TemporaryDirectory(prefix='forms-') as temp:
            temp = Path(temp)
            for form in spec['forms']:
                fid = form['id']
                blank = out / (fid + '-blank.docx'); filled = out / (fid + '-filled.docx')
                make_blank(form, blank)
                job = {'action': 'fill', 'blank': str(blank), 'filled': str(filled), 'fields': form['fields'], 'values': values[fid], 'record': str(temp / 'entered.json')}
                write_json(temp / 'job.json', job)
                command(['/usr/bin/python3', str(SOURCE / 'office.py'), str(temp / 'job.json')])
                entered = json.loads((temp / 'entered.json').read_text())
                clean_docx(blank); clean_docx(filled)
                job.update(action='inspect', record=str(temp / 'reopened.json'), blank_pdf=str(out / (fid + '-blank.pdf')), filled_pdf=str(out / (fid + '-filled.pdf')))
                write_json(temp / 'job.json', job)
                command(['/usr/bin/python3', str(SOURCE / 'office.py'), str(temp / 'job.json')])
                reopened = json.loads((temp / 'reopened.json').read_text())
                for mode in ('blank', 'filled'): clean_pdf(out / (fid + '-' + mode + '.pdf'))
                records.append({'form': fid, 'entry': entered, 'reopen_after_metadata_removal': reopened, 'ooxml_before': inspect_docx(blank), 'ooxml_after': inspect_docx(filled)})
        write_json(out / 'roundtrip.json', {'schema_version': 1, 'forms': records})
        measurements = check_all(indir, out, hashes=False)
        command([sys.executable, str(CASE / 'tests/selftest.py'), '--output', str(out)])
        command([sys.executable, str(CASE / 'tests/rendered_negative.py'), str(indir), str(out)])
        for form in spec['forms']:
            for mode in ('blank', 'filled'):
                prefix = out / (form['id'] + '-' + mode)
                command(['pdftoppm', '-png', '-scale-to', '1200', '-singlefile', str(prefix) + '.pdf', str(prefix)])
                from PIL import Image
                Image.open(str(prefix) + '.png').convert('RGB').save(str(prefix) + '.png')
        make_preview(out, spec['forms'][0]['id'])
        shutil.copyfile('/opt/packages.tsv', out / 'packages.tsv')
        fonts = out / 'font-licenses'; fonts.mkdir(exist_ok=True)
        for name in ('fonts-dejavu-core', 'fonts-liberation'):
            shutil.copyfile('/usr/share/doc/' + name + '/copyright', fonts / (name + '.txt'))
        tools = {'LibreOffice': command(['libreoffice', '--version']), 'Python': command([sys.executable, '--version']), 'Poppler': command(['pdftoppm', '-v']), 'Chromium': command(['chromium', '--version'])}
        import pypdf, PIL
        tools.update(pypdf=pypdf.__version__, Pillow=PIL.__version__)
        report = {'schema_version': 1, 'case': 'school-fillable-forms', 'input_hashes': input_hashes, 'output_hashes': {}, 'transformations': [{'operation': 'generate OOXML rich-text and checkbox controls', 'font': 'DejaVu Sans', 'fixed_text_row_twips': 1400, 'fixed_checkbox_row_twips': 620}, {'operation': 'normalize blank through LibreOffice DOCX export; enter values using UNO cursors and checkbox Checked; save DOCX; close'}, {'operation': 'remove DOCX properties; reopen in LibreOffice; inspect and export PDF'}, {'operation': 'remove PDF Info/XMP; rasterize sanitized PDFs with Poppler'}], 'counts': {'forms': len(measurements), 'controls': sum(m['controls'] for m in measurements), 'text_controls': sum(f['type'] == 'text' for form in spec['forms'] for f in form['fields']), 'checkbox_controls': sum(f['type'] == 'checkbox' for form in spec['forms'] for f in form['fields'])}, 'measurements': measurements, 'layout_tolerance_pt': 0.5, 'checks': [{'name': 'existing-output inspection', 'passed': True, 'observation': measurements}, {'name': 'negative tests', 'passed': True, 'observation': 'See selftest.json and rendered-negative.json for rejected schemas, damaged controls, values, links and PDF pages'}], 'tools': tools, 'uncertainties': ['Microsoft Word was not run. DOCX filling and round-trip were exercised in LibreOffice only.', 'The templates are not locked forms. Manual editing can exceed field space; the pipeline rejects values outside supported bounds.', 'Control IDs are mapped by source order and adjacent labels read through UNO; Writer may drop alias/tag metadata and add XML container wrappers. Raw wrapper counts are retained in roundtrip.json.'], 'human_steps': []}
        produced = [out / (form['id'] + '-' + mode + ext) for form in spec['forms'] for mode in ('blank', 'filled') for ext in ('.docx', '.pdf', '.png')]
        produced += [out / name for name in ('hero.png', 'preview-map.json', 'roundtrip.json', 'selftest.json', 'rendered-negative.json', 'packages.tsv')]
        produced += sorted(fonts.glob('*.txt'))
        report['output_hashes'] = {str(path.relative_to(out)): sha(path) for path in produced}
        write_json(out / 'report.json', report)
        # Resolve the current run's proof image, even with a separate output mount.
        preview_case = out / 'page-source'; preview_case.mkdir(exist_ok=True)
        (preview_case / 'media').mkdir(exist_ok=True)
        shutil.copyfile(out / 'hero.png', preview_case / 'media/hero.png')
        shutil.copyfile(CASE / 'README.md', preview_case / 'README.md')
        command([sys.executable, '/harness/screenshot.py', str(preview_case), str(out / 'page-previews')], timeout=300)
        shutil.rmtree(preview_case)
        report['output_hashes'].update({str(path.relative_to(out)): sha(path) for path in sorted((out / 'page-previews').iterdir()) if path.is_file()})
        write_json(out / 'report.json', report)
        write_json(out / 'claims.json', {'schema_version': 1, 'paths_relative_to': 'case directory', 'claims': [
            {'claim': str(report['counts']['forms']) + ' forms and ' + str(report['counts']['controls']) + ' leaf fields' , 'evidence': [{'path': 'output/report.json', 'pointer': '/counts'}, {'path': 'output/roundtrip.json', 'pointer': '/forms'}], 'calculation': 'Sum of inspected leaf controls across the forms; XML container wrappers recorded separately'},
            {'claim': 'Fields survive a LibreOffice save, close and reopen', 'evidence': [{'path': 'output/roundtrip.json', 'pointer': '/forms'}, {'path': 'output/report.json', 'pointer': '/tools/LibreOffice'}]},
            {'claim': 'Fixed-height rows and label positions within half a point', 'evidence': [{'path': 'output/report.json', 'pointer': '/transformations/0'}, {'path': 'output/report.json', 'pointer': '/measurements'}, {'path': 'output/report.json', 'pointer': '/layout_tolerance_pt'}, {'path': 'output/report.json', 'pointer': '/tools/Poppler'}], 'calculation': 'Maximum absolute x/y difference of matching PDF label word boxes; threshold 0.5 pt'},
            {'claim': 'First-screen image is the first form\'s filled page rendered from its PDF, cut below the last content; see the crop record', 'evidence': [{'path': 'output/preview-map.json', 'pointer': ''}, {'path': 'output/hero.png', 'frame': 'complete image: filled form page, top to just below the last content'}]},
            {'claim': 'Microsoft Word was not available or tested; LibreOffice was run', 'evidence': [{'path': 'output/report.json', 'pointer': '/uncertainties/0'}, {'path': 'output/report.json', 'pointer': '/tools/LibreOffice'}]},
            {'claim': 'Invalid inputs and damaged saved values, links and pages are rejected', 'evidence': [{'path': 'output/selftest.json', 'pointer': '/checks'}, {'path': 'output/rendered-negative.json', 'pointer': '/checks'}]},
            {'claim': 'Document workload runs offline, with separate read-only input and writable output', 'evidence': [{'path': '../harness/run-container.sh', 'lines': 'Docker run network and bind-mount arguments'}, {'path': 'run.sh', 'lines': 'shared runner invocation'}]},
            {'claim': 'Fields are editable and are not locked; pipeline enforces documented input limits', 'evidence': [{'path': 'source/forms.py', 'symbols': ['validate', 'make_blank']}, {'path': 'INPUT.md', 'section': 'Supported boundaries'}]},
            {'claim': 'Page screenshots are offline renders at phone and desktop sizes', 'evidence': [{'path': 'output/page-previews/screenshots.json', 'pointer': '/screenshots'}, {'path': 'output/page-previews/screenshots.json', 'pointer': '/surface'}]}
        ]})
        check_all(indir, out)
        runtime['status'] = 'passed'
        print('PASS: LibreOffice field entry, DOCX save/reopen, PDF layout and negative tests')
    finally:
        runtime['elapsed_seconds'] = round(time.monotonic() - started, 3)
        write_json(out / 'runtime.json', runtime)
        if runtime['status'] != 'passed':
            write_json(out / 'report.json', {'schema_version': 1, 'case': 'school-fillable-forms', 'status': 'failed', 'input_hashes': {}, 'output_hashes': {}, 'transformations': [], 'counts': {}, 'checks': [{'name': 'complete workload', 'passed': False, 'observation': 'Workload did not finish; see stderr and runtime.json. Existing artifacts are not a successful delivery.'}], 'tools': {'Python': sys.version.split()[0]}, 'uncertainties': ['Incomplete run; no compatibility or layout result.'], 'human_steps': []})


if __name__ == '__main__':
    try: main(Path(sys.argv[1]), Path(sys.argv[2]))
    except Exception as exc:
        print('FAIL: ' + str(exc), file=sys.stderr); sys.exit(1)
