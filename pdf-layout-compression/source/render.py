from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
from pypdf import PdfReader
from common import command, save

def render_evidence(inp,out,norm):
    previews=out/'previews'; previews.mkdir(exist_ok=True)
    for pattern in ('before-*.png','after-*.png','comparison-*.png','detail-*.png','image-detail-*.png','all-pages.png','hero.png'):
        for old in previews.glob(pattern): old.unlink()
    command(['pdftoppm','-r','120','-cropbox','-png',str(inp/'input.pdf'),str(previews/'before')])
    command(['pdftoppm','-r','120','-png',str(out/'fixed.pdf'),str(previews/'after')])
    font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',22)
    sheets=[]
    for i,(a,b) in enumerate(zip(sorted(previews.glob('before-*.png')),sorted(previews.glob('after-*.png')))):
        panel=Image.new('RGB',(1040,780),'#e9edf0'); d=ImageDraw.Draw(panel)
        d.text((24,12),f'BEFORE / sheet {i+1}',font=font,fill='#243b49'); d.text((544,12),f'AFTER / sheet {i+1}',font=font,fill='#243b49')
        for path,x in [(a,20),(b,540)]:
            im=Image.open(path).convert('RGB'); im.thumbnail((480,710)); panel.paste(im,(x,55))
        panel.save(previews/f'comparison-{i+1}.png'); sheets.append(panel)
    contact=Image.new('RGB',(1040,780*len(sheets)),'white')
    for i,im in enumerate(sheets): contact.paste(im,(0,780*i))
    contact.save(previews/'all-pages.png')
    # Align the actual cropped input render to the repaired page's scale and position.
    p=PdfReader(inp/'input.pdf').pages[0]
    scale=min((595.27559-2*28.34646)/float(p.mediabox.width),(841.88976-2*28.34646)/float(p.mediabox.height))
    cfg=__import__('json').loads((inp/'repair.json').read_text()); margin=cfg['margin_mm']*72/25.4
    scale=min((595.27559-2*margin)/float(p.mediabox.width),(841.88976-2*margin)/float(p.mediabox.height))
    after=Image.open(sorted(previews.glob('after-*.png'))[0]).convert('RGB')
    visible=Image.open(sorted(previews.glob('before-*.png'))[0]).convert('RGB')
    frame=Image.new('RGB',after.size,'white')
    x=(595.27559-float(p.mediabox.width)*scale)/2+float(p.cropbox.left)*scale
    y=(841.88976-float(p.mediabox.height)*scale)/2+(float(p.mediabox.top)-float(p.cropbox.top))*scale
    visible=visible.resize((round(visible.width*scale),round(visible.height*scale)),Image.Resampling.LANCZOS)
    frame.paste(visible,(round(x*120/72),round(y*120/72)))
    box=(70,255,365,330)
    hero=Image.new('RGB',(614,119),'#e9edf0'); d=ImageDraw.Draw(hero)
    f=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',18)
    d.text((8,7),'BEFORE / cut off',font=f,fill='#243b49'); d.text((316,7),'AFTER / restored',font=f,fill='#243b49')
    hero.paste(frame.crop(box),(8,36)); hero.paste(after.crop(box),(316,36)); hero.save(previews/'hero.png')
    # Full-resolution detail crops retain caption, fine linework and small-print text.
    for i,p in enumerate(sorted(previews.glob('after-*.png'))):
        im=Image.open(p); im.crop((100,420,900,820)).save(previews/f'image-detail-{i+1}.png'); im.crop((65,880,min(im.width,920),im.height-70)).save(previews/f'detail-{i+1}.png')
    save(previews/'frames.json',{'schema_version':1,'renderer':'pdftoppm','dpi':120,
        'hero':{'source':'input/input.pdf page 1 rendered with CropBox; output/fixed.pdf page 1',
                'crop_pixels_at_120_dpi':list(box),'before_rescale':scale,'same_reading_scale':True},
        'comparison_note':'Whole-page comparisons fit each page in its panel; hero alone uses equal reading scale.'})
