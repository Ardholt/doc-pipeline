"""Render proof from the delivered scan and cleaned LibreOffice PDF."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
from common import run,write_json

def figures(scan,out,work):
    media=out/'media'; media.mkdir(exist_ok=True)
    for pattern in ('contact-*.png','detail-*.png'):
        for old in media.glob(pattern):old.unlink()
    run(['pdftoppm','-f','1','-singlefile','-r','144','-png',scan,work/'scan'])
    run(['pdftoppm','-f','1','-singlefile','-r','144','-png',out/'preview.pdf',work/'preview'])
    scan_im=Image.open(work/'scan.png').convert('RGB'); final_im=Image.open(work/'preview.png').convert('RGB')
    scan_im.save(media/'scan-page-001.png'); final_im.save(media/'document-page-001.png')
    # Matching table totals remain readable at a phone's content width.
    before_box=(750,628,940,730); after_box=(820,495,1074,633)
    before=scan_im.crop(before_box); after=final_im.crop(after_box)
    target=330
    before=before.resize((target,round(before.height*target/before.width)))
    after=after.resize((target,round(after.height*target/after.width)))
    hero=Image.new('RGB',(720,250),'#f4f1e9'); d=ImageDraw.Draw(hero)
    font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',23)
    d.text((20,10),'SCANNED PAGE',font=font,fill='#3e4c50'); d.text((370,10),'EDITABLE DOCUMENT',font=font,fill='#183c42')
    hero.paste(before,(20,58)); hero.paste(after,(370,58)); hero.save(media/'hero.png')
    write_json(media/'figure-map.json',{'schema_version':1,'hero':{'left':{'source':'input/scan.pdf','page':1,'render_dpi':144,'crop_px':before_box},'right':{'source':'output/preview.pdf','page':1,'application':'LibreOffice headless PDF export, after DOCX metadata stripping','render_dpi':144,'crop_px':after_box},'operation':'Crops resized preserving aspect ratio; labels added above. No replacement document text.'}})
    # Every output page is represented, with larger inspection frames retained.
    import json
    from pypdf import PdfReader
    count=len(PdfReader(out/'preview.pdf').pages)
    sheets=[]
    for start in range(1,count+1,30):
        sheet=Image.new('RGB',(1200,1740),'#e8e8e8'); draw=ImageDraw.Draw(sheet)
        label_font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',12)
        for k,p in enumerate(range(start,min(start+30,count+1))):
            prefix=work/f'contact-{p}'
            run(['pdftoppm','-f',p,'-singlefile','-scale-to','270','-png',out/'preview.pdf',prefix],timeout=30)
            page=Image.open(prefix.with_suffix('.png')).convert('RGB'); page.thumbnail((190,260))
            x=(k%6)*200; y=(k//6)*348
            sheet.paste(page,(x+5,y+25)); draw.text((x+8,y+5),str(p),fill='black',font=label_font)
            prefix.with_suffix('.png').unlink()
        name=f'contact-{start:03d}.png'; sheet.save(media/name); sheets.append(name)
    for p in sorted(set([1,min(31,count),min(75,count),min(121,count),count])):
        prefix=work/f'detail-{p:03d}'
        run(['pdftoppm','-f',p,'-singlefile','-r','110','-png',out/'preview.pdf',prefix])
        Image.open(prefix.with_suffix('.png')).convert('RGB').save(media/f'detail-{p:03d}.png')
    write_json(media/'contact-sheets.json',{'schema_version':1,'output_pages':count,'sheets':sheets,'columns':6,'pages_per_sheet':30,'detail_pages':sorted(set([1,min(31,count),min(75,count),min(121,count),count]))})
