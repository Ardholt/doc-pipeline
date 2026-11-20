"""Offline scan extraction, literal review, editable delivery and measured proof."""
import json, os, shutil, sys, tempfile, time
from pathlib import Path
from pypdf import PdfReader
from common import sha,write_json,run,block_text,strip_pdf,docx_pages
from extract import parse_tsv,infer_blocks,review_rows,apply_review,restore_blocks
from document import build
from score import score
from figures import figures
from layout import audit

os.environ['OMP_THREAD_LIMIT']='1'
case=Path(__file__).resolve().parents[1]
inp,out=map(Path,sys.argv[1:3]); start=time.monotonic()

def runtime(status):
    write_json(out/'runtime.json',{'schema_version':1,'scope':'Container workload including OCR, conversion, metrics, renders and checks; excludes image setup, source authoring and visual inspection.','elapsed_seconds':round(time.monotonic()-start,3),'limits':{'cpus':2,'memory':'2g','workload_seconds':1080,'network':'none'},'status':status})

def main():
    out.mkdir(parents=True,exist_ok=True)
    if any(p.is_symlink() for p in out.rglob('*')):raise ValueError('Output directory must not contain symlinks')
    runtime('running')
    for n in ('report.json','checks.json','claims.json'):
        p=out/n
        if p.exists():p.unlink()
    scan=inp/'scan.pdf'
    if not scan.is_file():raise ValueError('Missing required input: scan.pdf')
    reader=PdfReader(scan)
    if reader.is_encrypted:raise ValueError('scan.pdf must be unencrypted')
    count=len(reader.pages)
    if not 1<=count<=500:raise ValueError('scan.pdf must contain 1 to 500 pages')
    for i,p in enumerate(reader.pages,1):
        if (p.extract_text() or '').strip():raise ValueError(f'scan.pdf page {i} has a text layer; this pipeline requires page images without hidden text')
        resources=p.get('/Resources',{})
        if hasattr(resources,'get_object'):resources=resources.get_object()
        if '/XObject' not in resources:raise ValueError(f'scan.pdf page {i} has no image resources')
    reviews=review_rows(inp/'review.csv',count)
    input_hashes={p.name:sha(p) for p in (scan,inp/'review.csv') if p.is_file()}
    rawdir=out/'raw'; rawdir.mkdir(exist_ok=True)
    for old in rawdir.glob('page-*'):
        if old.is_file():old.unlink()
    pages=[]; events=[]; uncertainties=[]
    with tempfile.TemporaryDirectory(prefix='retype-') as temp:
        work=Path(temp)
        def extract_page(p):
            prefix=work/f'page-{p:03d}'
            run(['pdftoppm','-f',p,'-singlefile','-r','200','-png',scan,prefix],timeout=45)
            tsv=run(['tesseract',prefix.with_suffix('.png'),'stdout','-l','eng','--psm','6','tsv'],timeout=45)
            prefix.with_suffix('.png').unlink()
            (rawdir/f'page-{p:03d}.tsv').write_text(tsv)
            lines,confidence=parse_tsv(tsv); raw_blocks=infer_blocks(lines); raw_text=block_text(raw_blocks)
            (rawdir/f'page-{p:03d}.txt').write_text(raw_text+'\n')
            final,log=apply_review(raw_text,reviews,p); blocks=restore_blocks(final,raw_blocks)
            low=[{'token':w['text'],'confidence':w['confidence'],'box_px':[w['left'],w['top'],w['width'],w['height']]} for line in lines for w in line['words'] if w['confidence']<85]
            page={'id':f'page-{p:03d}','page':p,'source':'scan.pdf','source_page':p,'docx_bookmark':f'source_page_{p:03d}','raw_text':raw_text,'final_text':final,'blocks':blocks,'mean_ocr_confidence':round(sum(confidence)/len(confidence),3),'low_confidence':low}
            return page,log
        from concurrent.futures import ThreadPoolExecutor
        with ThreadPoolExecutor(max_workers=2) as pool:
            for page,log in pool.map(extract_page,range(1,count+1)):
                pages.append(page); events.extend(log)
                p=page['page']
                if page['low_confidence']:uncertainties.append({'page':p,'low_confidence_words':len(page['low_confidence'])})
                if p%10==0 or p==count:print(f'OCR: {p}/{count} pages',flush=True)
        events.sort(key=lambda event:event['row'])
        write_json(out/'pages.json',{'schema_version':1,'pages':pages})
        write_json(out/'corrections.json',{'schema_version':1,'review_supplied':(inp/'review.csv').exists(),'applied_rows':len(events),'events':events,'uncertainties':uncertainties,'note':'Confidence below 85 is a review cue, not a probability of correctness. No automatic spelling correction. No human page-by-page proofreading is included in this command.'})
        build(pages,out/'retyped.docx')
        # Only now can the independent scorer read the reference. It never edits OCR or DOCX.
        accuracy=score(scan,out,case); write_json(out/'accuracy.json',{'schema_version':1,**accuracy})
        correction_report=json.loads((out/'corrections.json').read_text())
        correction_report['independent_reference_disagreements']=[{'page':p['page'],'character_edits':p['docx']['character_edits'],'word_edits':p['docx']['word_edits'],'tables_exact':p['tables_exact']} for p in accuracy.get('pages',[]) if p['docx']['character_edits']]
        write_json(out/'corrections.json',correction_report)
        lodir=work/'lo'; lodir.mkdir()
        lo_log=run(['libreoffice',f"-env:UserInstallation={os.environ['LO_PROFILE_URI']}",'--headless','--convert-to','pdf','--outdir',lodir,out/'retyped.docx'],timeout=180)
        if not (lodir/'retyped.pdf').is_file():raise ValueError('LibreOffice did not produce the expected PDF: '+lo_log[-300:])
        (out/'conversion.log').write_text(lo_log.replace(str(out),'<output>').replace(str(lodir),'<temporary>'))
        strip_pdf(lodir/'retyped.pdf',out/'preview.pdf')
        # Renders and extracted text below use the cleaned PDF.
        write_json(out/'layout.json',audit(out/'preview.pdf'))
        figures(scan,out,work)
        tools={'python':sys.version.split()[0],'text_metric':'source/common.py SHA-256 '+sha(case/'source/common.py'),'tesseract':run(['tesseract','--version']).splitlines()[0],'ocr_language':'eng','libreoffice':run(['libreoffice','--version']).strip(),'poppler':__import__('subprocess').run(['pdftoppm','-v'],capture_output=True,text=True).stderr.splitlines()[0],'pypdf':__import__('pypdf').__version__,'python-docx':__import__('docx').__version__,'Pillow':__import__('PIL').__version__,'chromium':run(['chromium','--version']).strip()}
        shutil.copy('/opt/packages.tsv',out/'packages.tsv')
        actual_docx=docx_pages(out/'retyped.docx')
        counts={'input_pages':count,'mapped_pages':len(pages),'docx_source_bookmarks':len(actual_docx),'preview_pages':len(PdfReader(out/'preview.pdf').pages),'tables':sum(b['kind']=='table' for p in actual_docx for b in p['blocks']),'review_rows':len(events),'low_confidence_words':sum(len(p['low_confidence']) for p in pages)}
        report={'schema_version':1,'case':'retype-150-pages','input_hashes':input_hashes,'output_hashes':{},'transformations':[{'operation':'Rasterize scan','tool':'Poppler','dpi':200},{'operation':'English OCR','tool':'Tesseract','psm':6,'answer_source':'page pixels only'},{'operation':'Reconstruct lines, paragraphs, uppercase headings and aligned table rows','rule':'TSV geometry; source/extract.py'},{'operation':'Apply optional literal review','applied_rows':len(events),'order':'CSV file order, exactly one match per row on named page'},{'operation':'Build editable DOCX and source-page bookmarks; remove package properties'},{'operation':'Export cleaned DOCX with LibreOffice; remove PDF Info/XMP; render cleaned PDF'}],'counts':counts,'checks':[],'tools':tools,'uncertainties':['Clear English print only. No handwriting, complex tables or multicolumn reading-order guarantee.','Source-page bookmarks preserve mapping; reflow can change output pagination.','Microsoft Word was not run. LibreOffice headless export is the compatibility evidence.','OCR confidence is not measured accuracy. Public accuracy is limited to this hash-matched authored corpus.'],'human_steps':([{'step':'Literal review.csv corrections; public corpus review scope is documented in source/review-record.md','rows':len(events),'time_measured':False}] if events else []),'accuracy':{k:v for k,v in accuracy.items() if k!='pages'}}
        write_json(out/'report.json',report)
        staging=work/'site'; staging.mkdir(); shutil.copy(case/'README.md',staging/'README.md'); shutil.copytree(out/'media',staging/'media')
        run(['python','/harness/screenshot.py',staging,out/'page-previews'],timeout=240)
        claims={'schema_version':1,'claims':[{'claim':'Source scan page count','evidence':[{'path':'output/report.json','pointer':'/counts/input_pages'},{'path':'source/corpus-manifest.json','pointer':'/page_count'}]},{'claim':'Editable, page-mapped text and tables','evidence':[{'path':'output/retyped.docx','part':'word/document.xml'},{'path':'output/pages.json','pointer':'/pages'}]},{'claim':'Measured raw, reviewed and delivered-text accuracy','evidence':[{'path':'output/accuracy.json','pointer':'/method'},{'path':'output/accuracy.json','pointer':'/raw'},{'path':'output/accuracy.json','pointer':'/reviewed'},{'path':'output/accuracy.json','pointer':'/docx'}],'calculation':'100 * (1 - sum(page edit distances) / sum(reference page denominators))'},{'claim':'Figure crops from actual source and LibreOffice output','evidence':[{'path':'output/media/figure-map.json','pointer':'/hero'}]},{'claim':'Offline case-page screenshots at narrow and wide widths','evidence':[{'path':'output/page-previews/screenshots.json','pointer':'/screenshots'}]},{'claim':'Microsoft Word not tested','evidence':[{'path':'output/report.json','pointer':'/uncertainties/2'}]}]}
        if not accuracy.get('available'):
            claims['claims'][0]['evidence']=claims['claims'][0]['evidence'][:1]
            claims['claims'][2]={'claim':'No independent reference for this replacement scan; no measured accuracy is asserted','evidence':[{'path':'output/accuracy.json','pointer':'/available'},{'path':'output/accuracy.json','pointer':'/reason'}]}
        if accuracy.get('available'):
            for phase in ('raw','reviewed','docx'):
                for key,value in accuracy[phase].items():
                    claims['claims'].append({'claim':f'{phase} {key}: {value}','evidence':[{'path':'output/accuracy.json','pointer':f'/{phase}/{key}'}],'calculation':'Percentages on the case page round this measured field to three decimal places.' if 'percent' in key else 'Measured from the normalized independent reference and extraction/delivered text.'})
        if accuracy.get('available'):claims['claims'].append({'claim':'Limited visual review of selected pages; no full proofreading pass','evidence':[{'path':'source/review-record.md','lines':'3-5'},{'path':'input/review.csv','lines':'1-13'},{'path':'output/corrections.json','pointer':'/events'}]})
        if accuracy.get('available'):
            claims['claims'].extend([
                {'claim':'Delivered DOCX: 203 of 750 record and item codes are wrong','evidence':[{'path':'proof/code-errors.json','pointer':'/delivered_docx/codes'},{'path':'proof/code-errors.json','pointer':'/delivered_docx/wrong'}],'calculation':'203 / 750 = 27.07%; a code is wrong when its source page, as retyped, does not contain it as a whole word (tests/code_errors.py).'},
                {'claim':'The wrong codes are on 115 of the 150 pages','evidence':[{'path':'proof/code-errors.json','pointer':'/delivered_docx/pages_with_a_wrong_code'}]},
                {'claim':'95 of the 150 tables differ from the reference in at least one cell','evidence':[{'path':'output/accuracy.json','pointer':'/tables_exact_pages'},{'path':'output/accuracy.json','pointer':'/pages'}],'calculation':'150 tables, 55 exact (tables_exact_pages), so 150 - 55 = 95 differ.'},
                {'claim':'83 of the 450 distinct record and item codes cannot be found by exact search in the searchable PDF','evidence':[{'path':'proof/code-errors.json','pointer':'/searchable_pdf'}],'calculation':'Whole-word search of the text of output/preview.pdf for each distinct reference code (tests/code_errors.py).'}])
        write_json(out/'claims.json',claims)
        report['output_hashes']={str(p.relative_to(out)):sha(p) for p in sorted(out.rglob('*')) if p.is_file() and p.name not in ('report.json','runtime.json','checks.json')}
        write_json(out/'report.json',report)
        sys.path.insert(0,str(case/'tests')); from check import validate
        checks=validate(inp,out,case)
        report['checks']=checks; write_json(out/'checks.json',{'schema_version':1,'checks':checks}); write_json(out/'report.json',report)
        if input_hashes!={n:sha(inp/n) for n in input_hashes}:raise ValueError('Input hashes changed during run')
        runtime('passed'); print('PASS: OCR, editable document, source mapping, accuracy and output checks',flush=True)
try:main()
except Exception as exc:
    
    if out.is_dir() and not any(p.is_symlink() for p in out.rglob('*')):runtime('failed')
    print(f'FAIL: {type(exc).__name__}: {exc}',file=sys.stderr); sys.exit(1)
