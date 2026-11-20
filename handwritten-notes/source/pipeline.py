"""Assemble reviewed transcription; preserve and audit page/block structure."""
import hashlib,json,os,shutil,subprocess,sys,tempfile,time,zipfile
from pathlib import Path
from lxml import etree as ET
from docx import Document
from docx.shared import Pt,Mm
from PIL import Image,ImageDraw,ImageFont
from pypdf import PdfReader,PdfWriter
from model import load,ordered,text,mapping,uncertainty
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'tests'))
from check import inspect
from regression import run as rejection_checks

def call(args,**kw):return subprocess.run(args,check=True,timeout=180,capture_output=True,text=True,**kw)
def version(args):return call(args).stdout.strip()
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(out,name,obj):(out/name).write_text(json.dumps(obj,indent=2,ensure_ascii=False)+'\n')
def sanitize_docx(path):
    with zipfile.ZipFile(path) as z: files={n:z.read(n) for n in z.namelist() if not n.startswith('docProps/')}
    ns='{http://schemas.openxmlformats.org/package/2006/relationships}'
    tree=ET.fromstring(files['_rels/.rels'])
    for el in list(tree):
        if 'docProps/' in el.get('Target',''):tree.remove(el)
    files['_rels/.rels']=ET.tostring(tree,encoding='utf-8',xml_declaration=True)
    tree=ET.fromstring(files['[Content_Types].xml'])
    for el in list(tree):
        if el.get('PartName','').startswith('/docProps/'):tree.remove(el)
    files['[Content_Types].xml']=ET.tostring(tree,encoding='utf-8',xml_declaration=True)
    # Remove revision identifiers inherited from the document template.
    for name in list(files):
        if name.startswith('word/') and name.endswith('.xml'):
            root=ET.fromstring(files[name])
            for el in root.iter():
                for attr in list(el.attrib):
                    if attr.rsplit('}',1)[-1].startswith('rsid'):del el.attrib[attr]
                for child in list(el):
                    if child.tag.rsplit('}',1)[-1] in ('rsids','docId'):el.remove(child)
            files[name]=ET.tostring(root,encoding='utf-8',xml_declaration=True)
    with zipfile.ZipFile(path,'w',compression=zipfile.ZIP_DEFLATED) as z:
        for n,b in sorted(files.items()):
            info=zipfile.ZipInfo(n,date_time=(2020,1,1,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED;z.writestr(info,b)

def build(src,out):
    start=time.monotonic();pages,tr=load(src);out.mkdir(parents=True,exist_ok=True)
    input_hashes={p.relative_to(src).as_posix():digest(p) for p in sorted(src.rglob('*')) if p.is_file()}
    fontdir=Path(os.environ['HOME'])/'.local/share/fonts';fontdir.mkdir(parents=True,exist_ok=True)
    for font in (Path(__file__).parent/'fonts').glob('*.ttf'):shutil.copyfile(font,fontdir/font.name)
    call(['fc-cache','-f',str(fontdir)])
    doc=Document();sec=doc.sections[0];sec.page_width=Mm(210);sec.page_height=Mm(297)
    sec.top_margin=sec.bottom_margin=Mm(22);sec.left_margin=sec.right_margin=Mm(24)
    for name,size in [('Normal',14),('Heading 1',24),('List Bullet',14)]:
        st=doc.styles[name];st.font.name='Inter SemiBold' if name=='Heading 1' else 'Inter';st.font.size=Pt(size);st.paragraph_format.space_after=Pt(14)
        st.font.bold=False
        rfonts=st.element.rPr.rFonts
        for attr in list(rfonts.attrib):
            if attr.endswith('Theme'):del rfonts.attrib[attr]
    from docx.oxml import OxmlElement
    from docx.oxml.ns import qn
    for lvl in doc.part.numbering_part.element.iter(qn('w:lvl')):
        fmt=lvl.find(qn('w:numFmt'))
        if fmt is not None and fmt.get(qn('w:val'))=='bullet':
            lvl.find(qn('w:lvlText')).set(qn('w:val'),'•')
            rpr=lvl.find(qn('w:rPr'))
            if rpr is None:rpr=OxmlElement('w:rPr');lvl.append(rpr)
            fonts=rpr.find(qn('w:rFonts'))
            if fonts is None:fonts=OxmlElement('w:rFonts');rpr.append(fonts)
            for attr in ('ascii','hAnsi','cs','eastAsia'):fonts.set(qn('w:'+attr),'Inter')
    for pi,p in enumerate(ordered(pages,tr)):
        for bi,b in enumerate(p['blocks']):
            style={'heading':'Heading 1','paragraph':'Normal','bullet':'List Bullet'}[b['kind']]
            para=doc.add_paragraph(b['text'],style)
            if pi and bi==0:para.paragraph_format.page_break_before=True
    doc.save(out/'notes.docx');sanitize_docx(out/'notes.docx')
    (out/'notes.txt').write_text(text(pages,tr))
    write(out,'mapping.json',mapping(pages,tr));write(out,'uncertainties.json',uncertainty(pages,tr))
    with tempfile.TemporaryDirectory() as tmp:
        conversion=call(['libreoffice','-env:UserInstallation='+os.environ['LO_PROFILE_URI'],'--headless','--convert-to','pdf','--outdir',tmp,str(out/'notes.docx')])
        raw=Path(tmp)/'notes.pdf'
        if not raw.exists():raise ValueError('LibreOffice did not produce notes.pdf: '+conversion.stdout.strip()+' '+conversion.stderr.strip())
        reader=PdfReader(raw);writer=PdfWriter();writer.append_pages_from_reader(reader);writer._info=None
        writer.write(out/'preview.pdf')
    # Render the cleaned PDF, never the discarded pre-cleaning file.
    call(['pdftoppm','-scale-to','1500','-png','-singlefile',str(out/'preview.pdf'),str(out/'preview')])
    im=Image.open(out/'preview.png').convert('RGB');im.save(out/'preview.png')
    # A direct crop of source pen strokes and a direct crop of the rendered PDF.
    # The first source page is a full-source view for arbitrary replacement inputs.
    source=Image.open(src/pages['pages'][0]['file']).convert('RGB')
    if source.size==(1000,420) and pages['pages'][0]['file']=='page-01.png':
        source=source.crop((40,278,680,390))
    else:source.thumbnail((660,180))
    bbox=call(['pdftotext','-f','1','-l','1','-bbox',str(out/'preview.pdf'),'-']).stdout
    tree=ET.fromstring(bbox);ns={'x':'http://www.w3.org/1999/xhtml'};page=tree.find('.//x:page',ns);words=tree.findall('.//x:word',ns)
    # Find a literal uncertainty token in the actual rendered output, if present.
    anchor=next((w for w in words if '[unclear]' in (w.text or '')),words[-1])
    y0=float(anchor.get('yMin'));y1=float(anchor.get('yMax'))
    line=[w for w in words if abs(float(w.get('yMin'))-y0)<2]
    sx=im.width/float(page.get('width'));sy=im.height/float(page.get('height'))
    x0=min(float(w.get('xMin')) for w in line);x1=max(float(w.get('xMax')) for w in line)
    typed=im.crop((max(0,int((x0-8)*sx)),int((y0-7)*sy),int((x1+12)*sx),int((y1+7)*sy)))
    canvas=Image.new('RGB',(700,310),'#f5f3ee');draw=ImageDraw.Draw(canvas)
    font=ImageFont.truetype(str(Path(__file__).parent/'fonts/Inter-Regular.ttf'),22)
    draw.text((20,10),'Original pen strokes',font=font,fill='#344054')
    source.thumbnail((660,116));canvas.paste(source,(20,44))
    draw.line((20,172,680,172),fill='#c0c0c0',width=1)
    draw.text((20,183),'Typed notes · rendered PDF',font=font,fill='#344054')
    typed.thumbnail((650,80));
    if typed.width<600:typed=typed.resize((int(typed.width*min(600/typed.width,80/typed.height)),int(typed.height*min(600/typed.width,80/typed.height))))
    canvas.paste(typed,(20,218));canvas.save(out/'hero.png')
    shutil.copyfile('/opt/packages.tsv',out/'packages.tsv')
    (out/'pdf-fonts.txt').write_text(call(['pdffonts',str(out/'preview.pdf')]).stdout)
    tools={'python':sys.version.split()[0],'python-docx':__import__('docx').__version__,'pypdf':__import__('pypdf').__version__,'Pillow':__import__('PIL').__version__,'libreoffice':version(['libreoffice','--version']),'pdftoppm':call(['pdftoppm','-v']).stderr.splitlines()[0],'chromium':version(['chromium','--version']),'pdffonts':call(['pdffonts','-v']).stderr.splitlines()[0],'pdftotext':call(['pdftotext','-v']).stderr.splitlines()[0],'lxml':__import__('lxml').__version__,'fontconfig':call(['fc-cache','--version']).stderr.strip()}
    counts={'source_pages':len(pages['pages']),'blocks':sum(len(p['blocks']) for p in tr['pages']),'unclear_tokens':sum(b['text'].count('[unclear]') for p in tr['pages'] for b in p['blocks']),'pdf_pages':len(PdfReader(out/'preview.pdf').pages)}
    report={'schema_version':1,'case':'handwritten-notes','input_hashes':input_hashes,'output_hashes':{},'transformations':[{'operation':'Assemble supplied reviewed text in source page order','font':'Inter','body_pt':14},{'operation':'Preserve heading, paragraph and bullet styles; retain literal [unclear] markers'},{'operation':'Remove DOCX property parts; export in LibreOffice; remove PDF metadata; render cleaned PDF'},{'operation':'Check DOCX/TXT text literally; for PDF comparison collapse whitespace and remove the generated bullet glyph U+F0B7 or U+2022'}],'counts':counts,'checks':[],'tools':tools,'uncertainties':['The command validates the supplied transcript, not handwriting recognition or transcription accuracy.','Microsoft Word was not run.','Page screenshots are offline layout approximations, not captures of published pages.'],'human_steps':['The transcript is prepared and reviewed by reading the page before the command runs; the command cannot verify image reading.','For the shipped inputs, the original stroke authorship and unresolved-mark decision are retained in source/authorship.md. Manual review time was not measured.'],'crossed_out_policy':mapping(pages,tr)['crossed_out_policy'],'page_preview_scope':'Case README and original case proof; replacement-input runs retain the published hero. preview.png always shows the supplied transcript.'}
    write(out,'report.json',report)
    inspect(src,out);neg=rejection_checks(src,out)
    report['checks']=[{'name':'content_structure_metadata','passed':True,'observation':'Actual DOCX text/styles, TXT, PDF text, page/block map, uncertainty list and input hashes agree.'},{'name':'rejection_checks','passed':True,'observation':f'{neg} invalid-input/damaged-output cases rejected.'}]
    write(out,'report.json',report)
    with tempfile.TemporaryDirectory() as tmp:
        stage=Path(tmp);(stage/'media').mkdir();shutil.copyfile('/case/README.md',stage/'README.md')
        original_root=Path('/case/input')
        original_hashes={p.relative_to(original_root).as_posix():digest(p) for p in sorted(original_root.rglob('*')) if p.is_file()}
        page_hero=out/'hero.png' if input_hashes==original_hashes else Path('/case/media/hero.png')
        shutil.copyfile(page_hero,stage/'media/hero.png')
        call(['python','/harness/screenshot.py',str(stage),str(out/'page-previews')])
    report['output_hashes']={p.relative_to(out).as_posix():digest(p) for p in sorted(out.rglob('*')) if p.is_file() and p.name not in ('report.json','runtime.json')}
    write(out,'report.json',report)
    inspect(src,out)
    write(out,'runtime.json',{'schema_version':1,'scope':'Offline assembly, conversion, checks and page screenshots; excludes image/transcript preparation, manual review and Docker setup.','elapsed_seconds':round(time.monotonic()-start,3),'limits':{'cpus':2,'memory_gb':2,'workload_seconds':1080,'setup_seconds':1500},'status':'PASS'})
    print('PASS: transcript assembled; source mapping, literal uncertainty, formatting and PDF text verified')
    print('PASS: offline case screenshots at 390 and 1366 CSS pixels')
    print('PASS: elapsed %.3f seconds (workload only)'%(time.monotonic()-start))
if __name__=='__main__':
    try:build(*map(Path,sys.argv[1:3]))
    except Exception as e:print('FAIL: '+str(e),file=sys.stderr);sys.exit(1)
