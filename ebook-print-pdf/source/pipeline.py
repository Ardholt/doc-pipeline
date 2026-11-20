"""Produce the interior and inspect the cleaned, rendered delivery."""
import base64, html, json, os, shutil, subprocess, sys, time, traceback
os.environ['SOURCE_DATE_EPOCH']='0'
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
from pypdf import PdfReader, PdfWriter
from pypdf.generic import RectangleObject
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from weasyprint import HTML
import weasyprint, pypdf, reportlab, PIL
from layout import load_input, make_html
from inspect_pdf import inspect, sha, extract


def dump(path,value):
    path.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n')


def clean_pdf(src,dst,cfg):
    writer=PdfWriter(clone_from=str(src))
    writer.metadata=None
    if '/Metadata' in writer._root_object: del writer._root_object['/Metadata']
    s=72/25.4; b=cfg['bleed_mm']*s; w=cfg['trim_width_mm']*s; h=cfg['trim_height_mm']*s
    if dst.name=='interior.pdf' and len(writer.pages)%2:
        writer.add_blank_page(width=w+2*b,height=h+2*b)
    for page in writer.pages:
        page.trimbox=RectangleObject([b,b,b+w,b+h])
        page.cropbox=RectangleObject(page.mediabox)
        page.bleedbox=RectangleObject(page.mediabox)
    with dst.open('wb') as f: writer.write(f)


def render_pdf(pdf,folder,dpi=96):
    folder.mkdir(parents=True,exist_ok=True)
    for old in folder.glob('page-*.png'): old.unlink()
    subprocess.run(['pdftoppm','-r',str(dpi),'-png',str(pdf),str(folder/'page')],check=True,timeout=180)
    for p in folder.glob('*.png'):
        im=Image.open(p).convert('RGB'); im.save(p)
    return sorted(folder.glob('*.png'))


def make_media(out,inspection,cfg):
    pages=render_pdf(out/'interior.pdf',out/'pages')
    render_pdf(out/'before.pdf',out/'before-pages')
    label=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',16)
    thumbs=[]
    for number,p in enumerate(pages,1):
        im=Image.open(p).convert('RGB'); im.thumbnail((170,255))
        tile=Image.new('RGB',(190,285),'#e9e6df'); tile.paste(im,((190-im.width)//2,8))
        ImageDraw.Draw(tile).text((12,263),str(number),font=label,fill='#242424'); thumbs.append(tile)
    rows=(len(thumbs)+5)//6
    sheet=Image.new('RGB',(1140,rows*285),'#e9e6df')
    for n,tile in enumerate(thumbs): sheet.paste(tile,((n%6)*190,(n//6)*285))
    sheet.save(out/'contact-sheet.png')
    chosen={1,len(pages),inspection['last_text_page']}|{c['start_page'] for c in inspection['chapters']}
    # Locate the retained figure caption in actual extracted output.
    for n,lines in enumerate(extract(out/'interior.pdf'),1):
        if any('observation page:' in l['text'] for l in lines): chosen.add(n)
    details=out/'details'; details.mkdir(exist_ok=True)
    for old in details.glob('page-*.png'): old.unlink()
    for number in sorted(chosen):
        subprocess.run(['pdftoppm','-f',str(number),'-l',str(number),'-r','144','-singlefile','-png',str(out/'interior.pdf'),str(details/f'page-{number:02}')],check=True,timeout=60)
        p=details/f'page-{number:02}.png'; Image.open(p).convert('RGB').save(p)
    # The first-screen image is one finished interior page, rendered from the PDF; nothing is redrawn over it.
    first=inspection['chapters'][0]['start_page']
    after=Image.open(details/f'page-{first:02}.png')
    subprocess.run(['pdftoppm','-f','1','-l','1','-r','144','-singlefile','-png',str(out/'before.pdf'),str(out/'before-detail')],check=True,timeout=60)
    before=Image.open(out/'before-detail.png').convert('RGB'); before.save(out/'before-detail.png')
    figure_page=next(n for n,lines in enumerate(extract(out/'interior.pdf'),1) if any('observation page:' in l['text'] for l in lines))
    shutil.copyfile(details/f'page-{figure_page:02}.png',out/'hero.png')
    pair=Image.new('RGB',(1200,930),'#e9e6df')
    for xx,im in [(20,before),(620,after)]:
        im=im.copy();im.thumbnail((560,880));pair.paste(im,(xx,25))
    pair.save(out/'page-pair.png')
    dump(out/'render-map.json',{'schema_version':1,'renderer':'pdftoppm','dpi':96,'detail_dpi':144,'detail_pages':sorted(chosen),'hero':{'page':figure_page,'source':f'details/page-{figure_page:02}.png','kind':'one finished interior page, unedited; the raw-Markdown first page and the first chapter opening side by side are in page-pair.png'},'contact_sheet':'all interior pages in file order'})


def run(root,out):
    start=time.monotonic(); out.mkdir(parents=True,exist_ok=True)
    cfg,ast=load_input(root)
    hashes={str(p.relative_to(root)):sha(p) for p in sorted(root.rglob('*')) if p.is_file()}
    doc,renderer=make_html(cfg,ast,root)
    for src in renderer.assets:
        doc=doc.replace((root/src).resolve().as_uri(),'data:image/svg+xml;base64,'+base64.b64encode((root/src).read_bytes()).decode())
    htmlpath=out/'layout.html';htmlpath.write_text(doc)
    rendered=HTML(string=doc,base_url=str(root)).render()
    opening_pages=[]
    chapter_ids={h['id'] for h in renderer.headings if h['level']==1}
    for number,page in enumerate(rendered.pages,1):
        if chapter_ids.intersection(page.anchors): opening_pages.append(number)
    suppression=''.join('@page :nth('+str(n)+') {@top-center {content:none}}' for n in opening_pages)
    doc=doc.replace('</style>',suppression+'</style>');htmlpath.write_text(doc)
    HTML(string=doc,base_url=str(root)).write_pdf(out/'interior-raw.pdf')
    clean_pdf(out/'interior-raw.pdf',out/'interior.pdf',cfg);(out/'interior-raw.pdf').unlink()
    # A plain source view, without typesetting, provides the before document.
    import textwrap
    pdfmetrics.registerFont(TTFont('SourceMono','/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf'))
    s=72/25.4; width=(cfg['trim_width_mm']+2*cfg['bleed_mm'])*s; height=(cfg['trim_height_mm']+2*cfg['bleed_mm'])*s
    margin=(cfg['margin_mm']+cfg['bleed_mm'])*s
    c=canvas.Canvas(str(out/'before-raw.pdf'),pagesize=(width,height),invariant=1)
    c.setFont('SourceMono',9); y=height-margin-9
    cols=int((width-2*margin)/(9*.602))
    for line in (root/'manuscript.md').read_text().splitlines():
        for part in textwrap.wrap(line,width=cols,replace_whitespace=False,drop_whitespace=False) or ['']:
            if y<margin+12: c.showPage();c.setFont('SourceMono',9);y=height-margin-9
            c.drawString(margin,y,part);y-=13
    c.save();clean_pdf(out/'before-raw.pdf',out/'before.pdf',cfg);(out/'before-raw.pdf').unlink()
    inspection=inspect(root,out)
    versions={'Python':sys.version.split()[0],'Pandoc':subprocess.check_output(['pandoc','--version'],text=True).splitlines()[0],
              'WeasyPrint':weasyprint.__version__,'pypdf':pypdf.__version__,'ReportLab':reportlab.Version,'Pillow':PIL.__version__,
              'Poppler':subprocess.run(['pdftoppm','-v'],capture_output=True,text=True).stderr.splitlines()[0],
              'qpdf':subprocess.check_output(['qpdf','--version'],text=True).splitlines()[0],
              'Chromium':subprocess.check_output(['chromium','--version'],text=True).strip()}
    dump(out/'source-map.json',{'schema_version':1,'blocks':inspection['source_map'],'footnotes':inspection['footnote_map'],'chapters':inspection['chapters']})
    dump(out/'geometry.json',{'schema_version':1,'print_settings':cfg,'pages':inspection['boxes'],'fonts':inspection['fonts'],'image_resolution':inspection['image_resolution']})
    shutil.copy('/opt/packages.tsv',out/'packages.tsv')
    notice=Path('/usr/share/doc/fonts-dejavu-core/copyright').read_text().split('Files: *\n',1)[1].split('\nFiles: debian/',1)[0]
    notice=notice.split(' For further information, contact:',1)[0].rstrip()+'\n'
    (out/'fonts-dejavu.txt').write_text('DejaVu font copyright and permission notice. Source: fonts-dejavu-core 2.37-6.\nPackaging metadata and the optional contact sentence are omitted.\n\n'+notice)
    make_media(out,inspection,cfg)
    (out/'extracted-text.txt').write_text('\n\f\n'.join('\n'.join(line['text'] for line in page) for page in extract(out/'interior.pdf'))+'\n')
    if not any(not c['passed'] for c in inspection['checks']):
        subprocess.run([sys.executable,'/case/tests/validation.py',str(root),str(out),str(out/'validation.json')],check=True,timeout=180)
    report={'schema_version':1,'case':'ebook-print-pdf','input_hashes':hashes,
            'output_hashes':{p.name:sha(p) for p in sorted(out.iterdir()) if p.is_file() and p.name not in ('report.json','runtime.json')},
            'transformations':[{'operation':'Pandoc Markdown parse','format':'markdown; raw HTML and unsupported blocks rejected'},
                               {'operation':'paged typesetting','settings':cfg,'running_heads':'book title on verso; chapter title on recto; suppressed on front matter, blank and chapter-opening pages','chapter_openings':'recto','footnotes':'page-bottom floats'},
                               {'operation':'deterministic embedded-font timestamps','source_date_epoch':0},
                               {'operation':'PDF cleaning','removed':['Info','XMP'],'boxes':'MediaBox = trim + twice bleed; TrimBox inset by bleed','even_page_count':'append a blank final verso when necessary'},
                               {'operation':'render cleaned PDFs','renderer':'Poppler','all_pages_dpi':96,'detail_pages_dpi':144}],
            'counts':inspection['counts'],'checks':inspection['checks'],'tools':versions,
            'uncertainties':['No printer upload, PDF/X certification, physical proof or cover was tested.','No Microsoft Word, LibreOffice, Kindle device or Kindle Previewer was run.','Visual review applies to the shipped manuscript; replacement manuscripts require fresh page review.'],
            'human_steps':['Original manuscript and SVG authored for this delivery.','See proof/visual-review.json for the recorded inspection of rendered pages.']}
    dump(out/'report.json',report)
    failures=[c['name'] for c in inspection['checks'] if not c['passed']]
    if failures: raise ValueError('PDF checks failed: '+', '.join(failures))
    subprocess.run([sys.executable,'/case/tests/check.py',str(root),str(out)],check=True,timeout=120)
    subprocess.run([sys.executable,'/harness/screenshot.py','/case',str(out/'page-previews')],check=True,timeout=300)
    dump(out/'runtime.json',{'schema_version':1,'scope':'Document conversion, independent checks, PDF renders and offline page screenshots; excludes image build and authoring/review','elapsed_seconds':round(time.monotonic()-start,3),'limits':{'cpus':2,'memory_gb':2,'network':'none','workload_seconds':1080},'status':'PASS'})
    print(f'PASS: interior {inspection["counts"]["pages"]} pages; {inspection["counts"]["chapters"]} chapters; source text, boxes, fonts and notes checked')

if __name__=='__main__':
    try: run(Path(sys.argv[1]),Path(sys.argv[2]))
    except Exception as e:
        print('ERROR: '+str(e),file=sys.stderr)
        sys.exit(1)
