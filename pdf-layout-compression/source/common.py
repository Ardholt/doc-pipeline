import collections, hashlib, json, math, subprocess, sys
from pathlib import Path
from pypdf import PdfReader, PdfWriter, Transformation
from pypdf.generic import RectangleObject, NameObject, NumberObject

def command(args, timeout=120):
    p=subprocess.run(args,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True,timeout=timeout)
    if p.returncode: raise ValueError(f'{Path(args[0]).name} failed ({p.returncode}): {p.stderr[-1200:]}')
    return p.stdout

def save(path,obj): path.write_text(json.dumps(obj,indent=2,ensure_ascii=False)+'\n')
def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()
def words(page): return (page.extract_text() or '').split()
def page_facts(reader):
    return [{'page':i+1,'media_box_pt':[round(float(v),4) for v in p.mediabox],
             'crop_box_pt':[round(float(v),4) for v in p.cropbox],'rotation':p.rotation,
             'words':len(words(p)),'images':len(p.images)} for i,p in enumerate(reader.pages)]
def load_input(inp):
    for name in ['input.pdf','repair.json']:
        if not (inp/name).is_file(): raise ValueError(f'missing input file: {name}')
    cfg=json.loads((inp/'repair.json').read_text())
    if not isinstance(cfg,dict): raise ValueError('repair.json: expected a JSON object')
    if type(cfg.get('schema_version')) is not int or cfg.get('schema_version')!=1: raise ValueError('repair.json: schema_version must be 1')
    for k in ('target_width_mm','target_height_mm','margin_mm','image_dpi'):
        if type(cfg.get(k)) not in (int,float) or not math.isfinite(cfg[k]): raise ValueError(f'repair.json: {k} must be a finite number')
    if cfg['target_width_mm']!=210 or cfg['target_height_mm']!=297: raise ValueError('only portrait A4 (210 x 297 mm) is supported')
    if not 8<=cfg['margin_mm']<=20: raise ValueError('margin_mm must be 8–20')
    if not 150<=cfg['image_dpi']<=200: raise ValueError('image_dpi must be 150–200')
    try: r=PdfReader(inp/'input.pdf',strict=True)
    except Exception as e: raise ValueError('malformed input.pdf: '+type(e).__name__) from e
    if r.is_encrypted: raise ValueError('encrypted input.pdf is not supported')
    catalog=r.trailer['/Root']
    if any(k in catalog for k in ('/AcroForm','/OpenAction','/AA','/OCProperties')) or catalog.get('/Names'):
        raise ValueError('interactive content, named destinations, attachments and layers require separate review before repair')
    if not r.pages: raise ValueError('input.pdf has no pages')
    for i,p in enumerate(r.pages):
        if p.get('/Annots') or p.get('/AA'): raise ValueError(f'page {i+1}: annotations/actions require separate review; nothing processed')
        if not words(p): raise ValueError(f'page {i+1}: searchable digital text is required')
        if min(float(p.mediabox.width),float(p.mediabox.height))<=0: raise ValueError(f'page {i+1}: invalid MediaBox')
    return cfg,r

def normalize(reader,cfg,dest):
    writer=PdfWriter(); transforms=[]
    W,H=210*72/25.4,297*72/25.4; margin=cfg['margin_mm']*72/25.4
    for i,p in enumerate(reader.pages):
        directions=collections.Counter()
        def visit(text,cm,tm,font,size):
            if text.strip():
                a=tm[0]*cm[0]+tm[1]*cm[2]; b=tm[0]*cm[1]+tm[1]*cm[3]
                angle=math.degrees(math.atan2(b,a))%360
                quarter=round(angle/90)*90%360
                if abs((angle-quarter+180)%360-180)>2: raise ValueError(f'page {i+1}: oblique text needs manual review')
                directions[quarter]+=len(text.strip())
        p.extract_text(visitor_text=visit)
        if not directions: raise ValueError(f'page {i+1}: cannot determine text orientation')
        direction=directions.most_common(1)[0][0]
        # PDF /Rotate is clockwise; the dominant physical baseline supplies it.
        p[NameObject('/Rotate')]=NumberObject(direction)
        p.cropbox=RectangleObject(p.mediabox)
        for key in ('/TrimBox','/BleedBox','/ArtBox'): p.pop(key,None)
        p.transfer_rotation_to_content()
        x,y=float(p.mediabox.left),float(p.mediabox.bottom)
        w,h=float(p.mediabox.width),float(p.mediabox.height)
        scale=min((W-2*margin)/w,(H-2*margin)/h)
        tx=(W-w*scale)/2-x*scale; ty=(H-h*scale)/2-y*scale
        p.add_transformation(Transformation((scale,0,0,scale,tx,ty)))
        p.mediabox=RectangleObject((0,0,W,H)); p.cropbox=RectangleObject((0,0,W,H))
        p[NameObject('/Rotate')]=NumberObject(0)
        writer.add_page(p)
        transforms.append({'page':i+1,'physical_baseline_degrees':direction,'scale':round(scale,8),
                           'matrix':[scale,0,0,scale,tx,ty],'method':'restore MediaBox; orient dominant text; fit full media into safe area'})
    writer._info=None
    with dest.open('wb') as f: writer.write(f)
    return transforms

def versions():
    import pypdf, PIL, reportlab
    return {'python':sys.version.split()[0],'pypdf':pypdf.__version__,'pillow':PIL.__version__,
            'reportlab':reportlab.Version,'ghostscript':command(['gs','--version']).strip(),
            'qpdf':command(['qpdf','--version']).splitlines()[0],
            'poppler':subprocess.run(['pdftoppm','-v'],capture_output=True,text=True).stderr.splitlines()[0],
            'chromium':command(['chromium','--version']).strip()}
