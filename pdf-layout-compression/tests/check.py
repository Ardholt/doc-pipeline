"""Inspect actual existing PDFs; never accepts a converter success flag as evidence."""
import json, sys, tempfile, xml.etree.ElementTree as ET
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'source'))
from common import *
from PIL import Image, ImageChops, ImageStat

def inspect(inp,out,normalized=None):
    cfg,original=load_input(inp)
    fixed=PdfReader(out/'fixed.pdf',strict=True)
    checks=[]
    def check(name,passed,observation):
        checks.append({'name':name,'passed':bool(passed),'observation':observation})
        if not passed: raise ValueError(name+': '+str(observation))
    check('page_count',len(original.pages)==len(fixed.pages),{'before':len(original.pages),'after':len(fixed.pages)})
    mapped=[]
    for i,(a,b) in enumerate(zip(original.pages,fixed.pages)):
        aw,bw=words(a),words(b)
        check(f'page_{i+1}_text',aw==bw,{'input_words':len(aw),'output_words':len(bw),'comparison':'exact words in page reading order; whitespace normalized'})
        check(f'page_{i+1}_images',len(a.images)==len(b.images),{'before':len(a.images),'after':len(b.images)})
        mapped.append({'page':i+1,'words':aw})
        check(f'page_{i+1}_geometry',all(abs(float(v)-t)<.02 for v,t in zip(b.mediabox,(0,0,210*72/25.4,297*72/25.4))) and list(b.cropbox)==list(b.mediabox) and b.rotation==0,{'media_box_pt':list(map(float,b.mediabox)),'rotation':b.rotation})
    check('metadata',not fixed.metadata and not fixed.xmp_metadata and not fixed.attachments,{'info':bool(fixed.metadata),'xmp':bool(fixed.xmp_metadata),'attachments':len(fixed.attachments)})
    command(['qpdf','--check',str(out/'fixed.pdf')])
    check('qpdf_structure',True,'qpdf --check exited 0')
    with tempfile.TemporaryDirectory() as td:
        tmp=Path(td)
        command(['pdftotext','-bbox',str(out/'fixed.pdf'),str(tmp/'bbox.html')])
        root=ET.parse(tmp/'bbox.html').getroot(); ns={'h':'http://www.w3.org/1999/xhtml'}
        margin=cfg['margin_mm']*72/25.4
        boxes=root.findall('.//h:word',ns)
        bounds=all(float(w.attrib['xMin'])>=margin-.1 and float(w.attrib['yMin'])>=margin-.1 and float(w.attrib['xMax'])<=210*72/25.4-margin+.1 and float(w.attrib['yMax'])<=297*72/25.4-margin+.1 for w in boxes)
        smallest=min(float(w.attrib['yMax'])-float(w.attrib['yMin']) for w in boxes)
        check('text_within_safe_area',bool(boxes) and bounds,{'words_measured':len(boxes),'margin_mm':cfg['margin_mm'],'minimum_word_box_height_pt':round(smallest,3)})
        check('minimum_text_size',smallest>=7,{'minimum_word_box_height_pt':round(smallest,3),'minimum_allowed_pt':7})
        image_list=command(['pdfimages','-list',str(out/'fixed.pdf')]); images=[]
        for line in image_list.splitlines()[2:]:
            parts=line.split()
            if len(parts)>=14: images.append({'page':int(parts[0]),'type':parts[2],'width':int(parts[3]),'height':int(parts[4]),'x_ppi':int(parts[12]),'y_ppi':int(parts[13])})
        check('image_resolution',all(min(i['x_ppi'],i['y_ppi'])>=cfg['image_dpi']-2 for i in images),images)
        fonts=command(['pdffonts',str(out/'fixed.pdf')])
        check('embedded_fonts',all('yes' in line for line in fonts.splitlines()[2:]) and len(fonts.splitlines())>2,fonts.splitlines())
        if normalized is None:
            normalized=tmp/'normalized.pdf'; normalize(original,cfg,normalized)
        command(['pdftoppm','-r','90','-png',str(normalized),str(tmp/'ref')])
        command(['pdftoppm','-r','90','-png',str(out/'fixed.pdf'),str(tmp/'got')])
        visual=[]
        for ref,got in zip(sorted(tmp.glob('ref-*.png')),sorted(tmp.glob('got-*.png'))):
            a,b=Image.open(ref).convert('RGB'),Image.open(got).convert('RGB')
            err=sum(ImageStat.Stat(ImageChops.difference(a,b)).mean)/3
            visual.append(round(err,5))
        check('visual_conservation',len(visual)==len(fixed.pages) and max(visual)<3,{'mean_absolute_rgb_error_per_page':visual,'maximum_allowed':3,'scale':'0–255; Poppler at 90 dpi against restored uncompressed source'})
    ib=(inp/'input.pdf').stat().st_size; ob=(out/'fixed.pdf').stat().st_size
    check('smaller_file',ob<ib,{'input_bytes':ib,'output_bytes':ob})
    return {'input_bytes':ib,'output_bytes':ob,'output_to_input_ratio':round(ob/ib,8),
            'reduction_percent':round((1-ob/ib)*100,2),'pages':len(fixed.pages),
            'words':sum(len(words(p)) for p in fixed.pages),'images':images,'source_output_map':mapped,'checks':checks}

if __name__=='__main__':
    try:
        inp,out=map(Path,sys.argv[1:3]); facts=inspect(inp,out)
        report=json.loads((out/'report.json').read_text())
        assert report['input_hashes']=={p.name:sha(p) for p in sorted(inp.iterdir()) if p.is_file()},'reported input hash mismatch'
        assert report['output_hashes']['fixed.pdf']==sha(out/'fixed.pdf'),'reported output hash mismatch'
        assert report['counts']=={k:v for k,v in facts.items() if k!='checks'},'reported facts differ'
        print('PASS: existing output independently inspected; report and hashes match')
    except Exception as e:
        print('FAIL: '+str(e),file=sys.stderr); sys.exit(1)
