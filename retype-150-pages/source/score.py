"""Post-conversion comparison with the independent, hash-bound public reference."""
import json
from pathlib import Path
from common import sha,metric,aggregate,block_text,docx_pages


def score(scan,output,case):
    manifest_path=case/'source/corpus-manifest.json'
    ref_path=case/'source/reference.json'
    if not manifest_path.exists():return {'available':False,'reason':'No generated corpus manifest is installed; reference comparison is unavailable.'}
    manifest=json.loads(manifest_path.read_text())
    if sha(scan)!=manifest['scan_sha256']:return {'available':False,'reason':'Replacement scan has no independent reference in this case; no accuracy percentage is asserted.'}
    if sha(ref_path)!=manifest['reference_sha256']:raise ValueError('Independent reference hash differs from corpus manifest')
    reference=json.loads(ref_path.read_text())['pages']
    pages=json.loads((output/'pages.json').read_text())['pages']; doc=docx_pages(output/'retyped.docx')
    if not len(reference)==len(pages)==len(doc):raise ValueError('Page count differs between reference, mapping and DOCX')
    results=[]
    for ref,page,actual in zip(reference,pages,doc):
        if not ref['page']==page['page']==actual['page']:raise ValueError('Source page order differs')
        text=block_text(ref['blocks'])
        expected_tables=[b['rows'] for b in ref['blocks'] if b['kind']=='table']
        actual_tables=[b['rows'] for b in actual['blocks'] if b['kind']=='table']
        results.append({'page':ref['page'],'raw':metric(text,page['raw_text']),'reviewed':metric(text,page['final_text']),'docx':metric(text,actual['text']),'reference_tables':expected_tables,'docx_tables':actual_tables,'tables_exact':expected_tables==actual_tables,'structure_exact':[b['kind'] for b in ref['blocks']]==[b['kind'] for b in actual['blocks']]})
    return {'available':True,'reference':'source/reference.json','reference_sha256':sha(ref_path),'method':'Exact unit-cost Levenshtein distance independently per source page. Collapse every whitespace run to one ASCII space and trim. Preserve case, spelling, digits and punctuation. Words are whitespace-delimited tokens. Denominators are reference counts after normalization. Accuracy = 100 * (1 - edits / reference count); no clipping at zero. DOCX text is read from word/document.xml in paragraph/table order using source-page bookmarks.','raw':aggregate([p['raw'] for p in results]),'reviewed':aggregate([p['reviewed'] for p in results]),'docx':aggregate([p['docx'] for p in results]),'structure_exact_pages':sum(p['structure_exact'] for p in results),'tables_exact_pages':sum(p['tables_exact'] for p in results),'pages':results}
