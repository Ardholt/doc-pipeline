"""Create replacement PNG/JPEG inputs from legible parts of our stroke page."""
import json,sys
from pathlib import Path
from PIL import Image
src,dst=map(Path,sys.argv[1:3]);dst.mkdir(parents=True,exist_ok=True)
im=Image.open(src/'page-01.png').convert('RGB')
im.crop((0,0,1000,270)).save(dst/'stock.jpg',quality=95)
im.crop((0,0,1000,145)).save(dst/'heading.png')
pages={'schema_version':1,'pages':[{'id':'stock-page','file':'stock.jpg'},{'id':'heading-page','file':'heading.png'}]}
tr={'schema_version':1,'pages':[{'id':'heading-page','blocks':[{'id':'title','kind':'heading','text':'Shelf check'}],'uncertainties':[]},{'id':'stock-page','blocks':[{'id':'title','kind':'heading','text':'Shelf check'},{'id':'stock','kind':'paragraph','text':'Keep 12 boxes.'}],'uncertainties':[]}]}
for name,obj in [('pages.json',pages),('transcript.json',tr)]:
    (dst/name).write_text(json.dumps(obj,indent=2)+'\n')
