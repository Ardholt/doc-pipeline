"""Fail when the stored page measurements show horizontal overflow, or no longer describe the README and CSS in the tree.

usage: preview_check.py CASE_DIR OUTPUT_DIR
Reads OUTPUT_DIR/page-previews/screenshots.json (written by screenshot.py, which measures the rendered README at 390 and
1366 CSS pixels in the Pages layout and in the local GitHub-style frame). Without that file nothing is checked and a note says so.
"""
import hashlib, json, sys
from pathlib import Path
case, out = Path(sys.argv[1]), Path(sys.argv[2])
record = out / 'page-previews' / 'screenshots.json'
if not record.is_file():
    print('NOTE: no page-previews/screenshots.json in this output; page overflow was not checked'); sys.exit(0)
data = json.loads(record.read_text())
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
problems = []
shots = data.get('screenshots', [])
if sorted((s['file'], s['css_width']) for s in shots) != [('github-1366.png', 1366), ('github-390.png', 390), ('pages-1366.png', 1366), ('pages-390.png', 390)]:
    problems.append('page-previews must hold github and pages renders at 390 and 1366')
for s in shots:
    m = s.get('measured')
    if not m: problems.append(f"{s['file']}: no overflow measurement recorded"); continue
    if m['viewport_width'] != s['css_width']: problems.append(f"{s['file']}: laid out at {m['viewport_width']} px, not {s['css_width']} px")
    if m['horizontal_overflow'] or m['document_scroll_width'] > m['viewport_width'] or m['content_right_edge'] > m['viewport_width'] + 0.5 or m['tables_wider_than_view']:
        problems.append(f"{s['file']}: horizontal overflow (page {m['document_scroll_width']} px, content edge {m['content_right_edge']} px, view {m['viewport_width']} px)")
files = data.get('measured_files', {})
if files.get('README.md') != sha(case / 'README.md'): problems.append('README.md changed since the page measurements were taken')
css = Path(__file__).resolve().parent / 'pages/assets/site.css'
if files.get('site.css') != sha(css): problems.append('harness/pages/assets/site.css changed since the page measurements were taken')
if problems:
    print('FAIL: ' + '; '.join(problems)); sys.exit(1)
print(f'PASS: README measured at 390 and 1366 CSS pixels in both page views, no horizontal overflow ({len(shots)} renders)')
