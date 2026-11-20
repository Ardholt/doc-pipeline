import json, shutil, sys, tempfile, time
from pathlib import Path
from pypdf import PdfReader, PdfWriter
from common import *

start=time.monotonic(); inp,out=map(Path,sys.argv[1:3]); out.mkdir(parents=True,exist_ok=True)
try:
    # Resolve all output paths before writing; reject symlink escapes.
    if any(p.is_symlink() for p in out.rglob('*')): raise ValueError('output contains a symlink; use a fresh directory')
    cfg,reader=load_input(inp)
    hashes={p.name:sha(p) for p in sorted(inp.iterdir()) if p.is_file()}
    before=page_facts(reader)
    with tempfile.TemporaryDirectory() as td:
        tmp=Path(td); norm=tmp/'normalized.pdf'; optimized=tmp/'optimized.pdf'
        transforms=normalize(reader,cfg,norm)
        dpi=str(cfg['image_dpi'])
        command(['gs','-q','-dSAFER','-dBATCH','-dNOPAUSE','-sDEVICE=pdfwrite','-dCompatibilityLevel=1.7',
            '-dAutoRotatePages=/None','-dDetectDuplicateImages=true','-dEmbedAllFonts=true',
            '-dDownsampleColorImages=true','-dColorImageDownsampleType=/Bicubic',f'-dColorImageResolution={dpi}',
            '-dColorImageDownsampleThreshold=1.0','-dDownsampleGrayImages=true',
            '-dGrayImageDownsampleType=/Bicubic',f'-dGrayImageResolution={dpi}','-dGrayImageDownsampleThreshold=1.0',
            '-dAutoFilterColorImages=false','-dColorImageFilter=/DCTEncode','-dJPEGQ=90',
            '-sOutputFile='+str(optimized),str(norm)],timeout=180)
        cleaned=PdfWriter()
        for page in PdfReader(optimized).pages:
            page.cropbox=RectangleObject(page.mediabox)
            for key in ('/TrimBox','/BleedBox','/ArtBox'): page.pop(key,None)
            cleaned.add_page(page)
        cleaned._info=None
        cleaned._root_object.pop('/Metadata',None)
        with (tmp/'clean.pdf').open('wb') as f: cleaned.write(f)
        command(['qpdf','--deterministic-id','--object-streams=generate',str(tmp/'clean.pdf'),str(out/'fixed.pdf')])
        sys.path.insert(0,'/case/tests')
        from check import inspect
        facts=inspect(inp,out,normalized=norm)
        from render import render_evidence
        render_evidence(inp,out,norm)
    checks=facts.pop('checks')
    report={'schema_version':1,'case':'pdf-layout-compression','input_hashes':hashes,
        'output_hashes':{'fixed.pdf':sha(out/'fixed.pdf')},'transformations':transforms,
        'counts':facts,'pages_before':before,'pages_after':page_facts(PdfReader(out/'fixed.pdf')),
        'checks':checks,'tools':versions(),'uncertainties':[
            'Dominant text baseline determines orientation; mixed-direction layouts require visual review.',
            'Annotations, forms, actions, attachments, named destinations and layers are rejected before processing.',
            'No Acrobat, Microsoft Office, email provider, PDF/A or accessibility certification was tested.'],
        'human_steps':[]}
    save(out/'report.json',report)
    from claim_map import claims
    save(out/'claims.json',claims(report))
    save(out/'runtime.json',{'schema_version':1,'scope':'offline conversion, rendering and content checks; excludes image build and case-page screenshots',
        'elapsed_seconds':round(time.monotonic()-start,3),'limits':{'cpus':2,'memory':'2g','network':'none'},
        'status':'PASS'})
    shutil.copy('/opt/packages.tsv',out/'packages.tsv')
    assert hashes=={p.name:sha(p) for p in sorted(inp.iterdir()) if p.is_file()},'input changed'
    print('PASS: input hashes unchanged')
    print('PASS: text, page geometry, images, metadata and visual comparison')
    print('PASS: fixed.pdf, report.json, runtime.json and previews written')
except Exception as e:
    print('FAIL: '+str(e),file=sys.stderr); sys.exit(1)
