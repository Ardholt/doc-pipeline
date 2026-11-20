"""Verify that the editable stroke artwork produces the delivered source raster."""
import hashlib,json,subprocess,sys,tempfile
from pathlib import Path
from PIL import Image,ImageChops
svg,png,result=map(Path,sys.argv[1:4])
with tempfile.TemporaryDirectory() as tmp:
    shot=Path(tmp)/'strokes.png'
    subprocess.run(['chromium','--headless','--no-sandbox','--disable-gpu','--disable-dev-shm-usage','--hide-scrollbars','--force-device-scale-factor=1','--window-size=1000,420',f'--screenshot={shot}',svg.resolve().as_uri()],capture_output=True,check=True,timeout=60)
    expected=Image.open(png).convert('RGB');actual=Image.open(shot).convert('RGB')
    assert expected.size==actual.size and ImageChops.difference(expected,actual).getbbox() is None,'Stroke/raster mismatch'
obj={'schema_version':1,'status':'PASS','source':'source/pen-strokes.svg','source_sha256':hashlib.sha256(svg.read_bytes()).hexdigest(),'raster':'input/page-01.png','raster_sha256':hashlib.sha256(png.read_bytes()).hexdigest(),'observation':'Editable SVG and original PNG rendered to identical RGB pixels. No text elements or font resources in SVG.','renderer':subprocess.check_output(['chromium','--version'],text=True).strip()}
assert '<text' not in svg.read_text() and 'font' not in svg.read_text(),'Type resource in stroke source'
result.write_text(json.dumps(obj,indent=2)+'\n');print('PASS: original raster matches editable stroke source pixel for pixel')
