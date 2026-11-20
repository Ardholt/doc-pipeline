"""Measure text extents in the cleaned PDF, independently of DOCX settings."""
from xml.etree import ElementTree as ET
from common import run

def audit(path):
    root=ET.fromstring(run(['pdftotext','-bbox',path,'-'],timeout=120))
    pages=[]
    for index,page in enumerate(root.findall('.//{*}page'),1):
        words=page.findall('.//{*}word')
        if not words:raise ValueError(f'PDF page {index} has no searchable words')
        width=float(page.get('width')); height=float(page.get('height'))
        extents=[min(float(w.get('xMin')) for w in words),min(float(w.get('yMin')) for w in words),max(float(w.get('xMax')) for w in words),max(float(w.get('yMax')) for w in words)]
        safe=extents[0]>=14 and extents[1]>=14 and extents[2]<=width-14 and extents[3]<=height-14
        if not safe:raise ValueError(f'PDF page {index} text enters the outer 14-point edge band')
        pages.append({'page':index,'width_pt':width,'height_pt':height,'text_bounds_pt':extents,'words':len(words),'inside_edge_band':safe})
    return {'schema_version':1,'method':'Poppler pdftotext -bbox on the cleaned PDF. All extracted word boxes must stay at least 14 points inside the page. This measures bounds; visual review checks appearance.','pages':pages}
