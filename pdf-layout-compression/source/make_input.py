"""Regenerate the authored input; never used to infer replacement PDF content."""
import json, math, sys
from pathlib import Path
from io import BytesIO
from PIL import Image
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.utils import ImageReader
from pypdf import PdfReader, PdfWriter
from pypdf.generic import DecodedStreamObject, NameObject, RectangleObject

root=Path(__file__).resolve().parent
out=Path(sys.argv[1]); out.mkdir(parents=True, exist_ok=True)
content=json.loads((root/'content.json').read_text())
pdfmetrics.registerFont(TTFont('Body','/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'))
pdfmetrics.registerFont(TTFont('Bold','/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'))
buf=BytesIO(); c=canvas.Canvas(buf, pagesize=(595.27559,841.88976), invariant=1)
for n,p in enumerate(content['pages']):
    w,h=(640,900) if n==2 else (595.27559,841.88976)
    c.setPageSize((w,h))
    c.setStrokeColorRGB(.12,.28,.34); c.setLineWidth(.6); c.rect(18,18,w-36,h-36)
    c.setFillColorRGB(.10,.23,.29); c.setFont('Bold',25); c.drawString(36,h-64,p['title'])
    c.setFont('Body',12); c.drawString(36,h-91,p['subtitle'])
    c.setFont('Body',13)
    for i,line in enumerate(p['lines']): c.drawString(36,h-138-i*25,line)
    iw,ih=2100,1500
    data=bytearray(iw*ih*3)
    for y in range(ih):
        v=y/ih
        for x in range(iw):
            u=x/iw
            z=.5+.23*math.sin(u*13+v*7+n)+.16*math.cos(v*21-u*5)+.10*math.sin(33*(u*u+v*v))
            band=.5+.5*math.sin(z*80)
            t=max(0,min(1,z))
            k=(y*iw+x)*3
            data[k:k+3]=bytes((int(30+190*t),int(65+115*t+20*band),int(110+80*(1-t))))
    img=Image.frombytes('RGB',(iw,ih),bytes(data))
    c.drawImage(ImageReader(img),36,h-530,width=480,height=300)
    c.setFont('Body',11); c.drawString(36,h-550,p['caption'])
    c.setStrokeColorRGB(.13,.25,.30)
    for i in range(7):
        c.setLineWidth(.3+i*.08); c.line(36,h-590-i*8,275,h-590-i*8)
    c.line(345,h-650,345,h-585); c.line(345,h-585,339,h-596); c.line(345,h-585,351,h-596)
    c.setFont('Bold',11); c.drawString(359,h-595,'UP'); c.drawString(359,h-650,'BASE')
    c.setFont('Body',10); c.drawString(36,h-690,p['note'])
    c.setFont('Body',11); c.drawString(36,38,p['footer'])
    c.showPage()
c.save()
r=PdfReader(buf); writer=PdfWriter()
for n,p in enumerate(r.pages):
    # A valid but inefficient export: full-size, uncompressed image streams.
    for ref in p['/Resources']['/XObject'].values():
        obj=ref.get_object()
        if obj.get('/Subtype')=='/Image':
            raw=DecodedStreamObject(); raw.set_data(obj.get_data())
            for k,v in obj.items():
                if k not in ('/Length','/Filter','/DecodeParms'): raw[k]=v
            obj.clear(); obj.update(raw); obj._data=raw._data
    if n==0: p.cropbox=RectangleObject((110,60,565,740))
    if n==1: p.rotate(90)
    writer.add_page(p)
writer._info=None
with (out/'input.pdf').open('wb') as f: writer.write(f)
print('PASS: authored input generated')
