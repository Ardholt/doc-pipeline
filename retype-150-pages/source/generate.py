"""Render the independently authored reference into image-only typed pages."""
import io, json, random, sys, textwrap
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.utils import ImageReader
from common import sha, write_json, block_text, strip_pdf

reference,out=map(Path,sys.argv[1:3]); out.mkdir(parents=True,exist_ok=True)
pages=json.loads(reference.read_text())['pages']
font_path=Path(__file__).with_name('DejaVuSansMono.ttf')
dpi=200; scale=dpi/72; width,height=1654,2339
font=ImageFont.truetype(str(font_path),round(11.5*scale))
heading=ImageFont.truetype(str(font_path),round(12*scale))
rng=random.Random(271828)
tmp=out/'unstripped.pdf'; canvas=Canvas(str(tmp),pagesize=(595.28,841.89),pageCompression=1,invariant=1)
manifest=[]
for page in pages:
    im=Image.new('L',(width,height),248); d=ImageDraw.Draw(im)
    for _ in range(10000):
        x=rng.randrange(width); y=rng.randrange(height); d.point((x,y),fill=rng.randrange(227,253))
    for x in range(18):d.line((x,0,x,height),fill=229+x)
    y=145; lines=[]
    for block in page['blocks']:
        if block['kind']=='table':
            for row in block['rows']:
                lines.append((''.join(s.ljust(16) for s in row).rstrip(),False,y)); y+=42
        else:
            for line in textwrap.wrap(block['text'],width=73,break_long_words=False,break_on_hyphens=False):
                lines.append((line,block['kind']=='heading',y)); y+=42
        y+=25
    if y>height-110:raise ValueError(f"Text does not fit source page {page['page']}")
    for line,is_heading,y in lines:
        d.text((135+rng.choice([-1,0,0,1]),y),line,font=heading if is_heading else font,fill=rng.randrange(28,48))
    angle=rng.uniform(-0.22,0.22)
    im=im.rotate(angle,resample=Image.Resampling.BICUBIC,fillcolor=248)
    buf=io.BytesIO(); im.save(buf,format='JPEG',quality=88,subsampling=0,optimize=True)
    data=buf.getvalue(); import hashlib
    canvas.drawImage(ImageReader(io.BytesIO(data)),0,0,width=595.28,height=841.89); canvas.showPage()
    manifest.append({'page':page['page'],'id':page['id'],'image_sha256':hashlib.sha256(data).hexdigest(),'text_sha256':hashlib.sha256(block_text(page['blocks']).encode()).hexdigest(),'width_px':width,'height_px':height,'skew_degrees':round(angle,6)})
    if page['page'] in (1,75,150):im.convert('RGB').save(out/f"source-{page['page']:03d}.png")
canvas.save(); strip_pdf(tmp,out/'scan.pdf'); tmp.unlink()
write_json(out/'corpus-manifest.json',{'schema_version':1,'page_count':len(pages),'scan_sha256':sha(out/'scan.pdf'),'reference_sha256':sha(reference),'font_sha256':sha(font_path),'recipe':'source/generate.py','raster_dpi':dpi,'seed':271828,'degradation':'Paper tone, sparse grain, left-edge shading, per-line ink density and position variation, small page skew, JPEG quality 88. No hidden text.','pages':manifest})
print(f'PASS: generated {len(pages)} image-only pages')
