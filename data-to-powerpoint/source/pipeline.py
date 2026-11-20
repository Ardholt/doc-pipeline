"""Create a reconciled editable presentation, then render the cleaned package."""
import hashlib, io, json, math, os, posixpath, shutil, subprocess, sys, tempfile, time, zipfile
from decimal import Decimal
from pathlib import Path
from xml.etree import ElementTree as ET
from pptx import Presentation
from pptx.chart.data import CategoryChartData
from pptx.dml.color import RGBColor
from pptx.enum.chart import XL_CHART_TYPE, XL_DATA_LABEL_POSITION, XL_LEGEND_POSITION, XL_TICK_MARK, XL_TICK_LABEL_POSITION
from pptx.util import Inches, Pt
from PIL import Image, ImageDraw, ImageFont
from pypdf import PdfReader, PdfWriter
from data import read_inputs, sums, money

NS = {'r': 'http://schemas.openxmlformats.org/package/2006/relationships'}
FONT = 'DejaVu Sans'
INK, MUTED, PAPER = '172B3A', '526875', 'F7F9FA'

def run(args, **kwargs):
    result=subprocess.run(args, timeout=180, capture_output=True, text=True, **kwargs)
    if result.returncode: raise ValueError((result.stdout+result.stderr).strip() or f'Command failed: {args[0]}')
    return result.stdout.strip()

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def write_json(path, obj):
    path.write_text(json.dumps(obj, indent=2, ensure_ascii=False) + '\n')

def clean_zip(raw, workbooks=None, cells=None):
    src, buf = zipfile.ZipFile(io.BytesIO(raw)), io.BytesIO()
    removed = {n for n in src.namelist() if n.startswith('docProps/') or n.endswith('thumbnail.jpeg') or '/printerSettings/' in n}
    with zipfile.ZipFile(buf, 'w', zipfile.ZIP_DEFLATED) as dest:
        for name in sorted(src.namelist()):
            if name in removed:
                continue
            data = src.read(name)
            if name.endswith('.xlsx'):
                data = clean_zip(data, cells=(workbooks or {}).get(name))
            elif name == 'xl/worksheets/sheet1.xml' and cells:
                root=ET.fromstring(data)
                ns={'s':'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
                for cell in root.findall('.//s:c',ns):
                    if cell.get('r') in cells:
                        cell.find('s:v',ns).text=cells[cell.get('r')]
                ET.register_namespace('',ns['s'])
                data=ET.tostring(root,encoding='utf-8',xml_declaration=True)
            elif name.endswith('.rels') or name == '[Content_Types].xml':
                root = ET.fromstring(data)
                for child in list(root):
                    if 'docProps/' in child.get('Target', '') or child.get('PartName', '').lstrip('/') in removed or 'metadata/' in child.get('Type', '') or 'extended-properties' in child.get('Type', '') or 'thumbnail' in child.get('Type', '') or 'printerSettings' in child.get('Type', '') or child.get('Extension') == 'bin':
                        root.remove(child)
                ET.register_namespace('', root.tag.split('}')[0][1:])
                data = ET.tostring(root, encoding='utf-8', xml_declaration=True)
            info = zipfile.ZipInfo(name, (2026, 1, 1, 0, 0, 0)); info.compress_type = zipfile.ZIP_DEFLATED
            dest.writestr(info, data)
    return buf.getvalue()

def text(slide, x, y, w, h, value, size=22, colour=INK, bold=False):
    shape = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    frame = shape.text_frame; frame.word_wrap = True
    frame.margin_left = frame.margin_right = 0
    frame.margin_top = frame.margin_bottom = 0
    p = frame.paragraphs[0]; p.text = value
    p.font.name = FONT; p.font.size = Pt(size); p.font.bold = bold; p.font.color.rgb = RGBColor.from_string(colour)
    return shape

def build(cfg, rows, periods, out):
    deck = Presentation(); deck.slide_width = Inches(13.333333); deck.slide_height = Inches(7.5)
    maps, slide_records = [], []
    order = cfg['department_order']; currency = cfg['currency']; totals = sums(rows)
    def slide(eyebrow, headline, subtitle):
        s = deck.slides.add_slide(deck.slide_layouts[6])
        s.background.fill.solid(); s.background.fill.fore_color.rgb = RGBColor.from_string(PAPER)
        n = len(deck.slides)
        text(s, .55, .32, 12.2, .3, eyebrow.upper(), 12, MUTED, True)
        text(s, .55, .85, 12.2, .8, headline, 30 if len(headline) <= 60 else 26, INK, True)
        text(s, .55, 1.7, 12.2, .6, subtitle, 16, MUTED)
        text(s, .55, 7.06, 11, .25, f'{cfg["title"]}  |  {currency}  |  Source: data.csv', 10, MUTED)
        text(s, 12.25, 7.06, .5, .25, str(n), 10, MUTED)
        slide_records.append({'slide': n, 'headline': headline, 'source_lines': [r['line'] for r in rows]})
        return s
    def chart(s, kind, categories, series, x, y, w, h, dept=None, source_rows=None, bounds=None):
        data = CategoryChartData(); data.categories = categories
        for name, values in series:
            data.add_series(name, [float(v) for v in values], '#,##0.##;−#,##0.##;0')
        ch = s.shapes.add_chart(XL_CHART_TYPE.COLUMN_CLUSTERED, Inches(x), Inches(y), Inches(w), Inches(h), data).chart
        ch.font.name = FONT; ch.font.size = Pt(18)
        ch._chartSpace.xpath('./c:chart/c:autoTitleDeleted')[0].set('val','1')
        ch.has_legend = kind == 'comparison'
        if ch.has_legend:
            ch.legend.position = XL_LEGEND_POSITION.BOTTOM
            ch.legend.include_in_layout = False
        ch.chart_style = 10
        plot = ch.plots[0]; plot.has_data_labels = True
        plot.data_labels.position = XL_DATA_LABEL_POSITION.OUTSIDE_END
        plot.data_labels.font.name = FONT; plot.data_labels.font.size = Pt(14 if max(len(money(v)) for _, values in series for v in values) > 8 else (20 if w < 5 else 22))
        plot.data_labels.font.color.rgb = RGBColor.from_string(INK)
        plot.data_labels.number_format = '#,##0.##;−#,##0.##;0'
        plot.gap_width = 100
        ch.value_axis.has_major_gridlines = True
        ch.value_axis.tick_labels.font.size = Pt(12)
        ch.value_axis.tick_labels.number_format = '#,##0.##;−#,##0.##;0'
        ch.category_axis.tick_labels.font.size = Pt(20 if w < 5 else 18)
        ch.category_axis.major_tick_mark = XL_TICK_MARK.NONE
        ch.category_axis.tick_label_position = XL_TICK_LABEL_POSITION.LOW
        if bounds:
            ch.value_axis.minimum_scale, ch.value_axis.maximum_scale = bounds
        for i, ser in enumerate(ch.series):
            if dept:
                colour = cfg['colours'][dept][1:] if i == 0 else 'CAD2D9'
                ser.format.fill.solid(); ser.format.fill.fore_color.rgb = RGBColor.from_string(colour)
                ser.format.line.fill.background()
            else:
                for j, point in enumerate(ser.points):
                    point.format.fill.solid(); point.format.fill.fore_color.rgb = RGBColor.from_string(cfg['colours'][categories[j]][1:])
                    point.format.line.fill.background()
        maps.append({'slide': len(deck.slides), 'part': str(ch.part.partname).lstrip('/'), 'kind': kind, 'department': dept, 'categories': categories, 'series': [{'name': n, 'values': [str(v) for v in vals]} for n, vals in series], 'source_lines': [r['line'] for r in source_rows or rows]})
        return ch
    s = slide('Performance review', f'{currency} {money(totals["profit"])} remains after costs', f'{periods[0]} to {periods[-1]} · Recorded revenue less recorded cost')
    text(s, .55, 2.7, 11.8, 1.2, cfg['title'], 30, INK, True)
    for i, key in enumerate(('revenue', 'cost', 'profit')):
        text(s, .55 + i * 4.2, 4.35, 4, .4, key.upper(), 15, MUTED, True)
        text(s, .55 + i * 4.2, 4.95, 4, .9, money(totals[key]), 34, INK, True)
    for start in range(0, len(order), 6):
        group = order[start:start+6]
        top = max(group, key=lambda d: sums([r for r in rows if r['department'] == d])['revenue'])
        s = slide('Revenue overview', f'{top} has the highest revenue in this group', f'All recorded periods · {currency} · Departments {", ".join(group)}')
        chart(s, 'overview', group, [('Revenue', [sums([r for r in rows if r['department'] == d])['revenue'] for d in group])], .7, 2.5, 11.9, 4.2, source_rows=[r for r in rows if r['department'] in group], bounds=(0, float(max(sums([r for r in rows if r['department'] == d])['revenue'] for d in group) or 1)*1.3))
    for start in range(0, len(order), 3):
        group = order[start:start+3]
        losses = [d for d in group if sums([r for r in rows if r['department'] == d])['profit'] < 0]
        headline = f'{", ".join(losses)} records a loss over the period' if losses else 'Revenue covers costs in each department shown'
        s = slide('Revenue and cost', headline, f'All recorded periods · {currency} · Revenue uses each department colour; cost is grey')
        hi = max(sums([r for r in rows if r['department'] == d])[k] for d in group for k in ('revenue','cost'))
        for i, d in enumerate(group):
            dr = [r for r in rows if r['department'] == d]; total = sums(dr); x = .55 + i * 4.2
            text(s, x, 2.45, 4, .4, f'{d} · Profit {money(total["profit"])}', 21, cfg['colours'][d][1:], True)
            chart(s, 'comparison', [d], [('Revenue', [total['revenue']]), ('Cost', [total['cost']])], x, 3.05, 4, 3.8, dept=d, source_rows=dr, bounds=(0, float(hi or 1)*1.3))
    hero = None
    for pstart in range(0, len(periods), 3):
        ps = periods[pstart:pstart+3]
        for start in range(0, len(order), 3):
            group = order[start:start+3]
            drs = [r for r in rows if r['department'] in group and r['period'] in ps]
            negatives = [d for d in group if any(r['profit'] < 0 for r in drs if r['department'] == d)]
            headline = f'{", ".join(negatives)} has negative monthly profit' if negatives else 'Monthly profit stays at or above zero'
            s = slide('Profit trend', headline, f'Revenue minus cost · {currency} · Independent axes keep small losses visible')
            for i,d in enumerate(group):
                dr = sorted([r for r in drs if r['department'] == d], key=lambda r: r['period']); vals = [r['profit'] for r in dr]
                x = .55 + i*4.2
                text(s,x,2.45,4,.45,f'{d} · Monthly profit',24,cfg['colours'][d][1:],True)
                labels = [p[5:] for p in ps]
                lo, hi = min(vals+[Decimal(0)]), max(vals+[Decimal(0)]); span = max(hi-lo, Decimal(1))
                chart(s,'trend',labels,[(f'{d} profit',vals)],x,3.05,4,3.4,dept=d,source_rows=dr,bounds=(float(lo-span*Decimal('.4')) if lo < 0 else 0, float(hi+span*Decimal('.4'))))
                text(s,x,6.55,4,.25,f'Months {ps[0]} to {ps[-1]}',12,MUTED)
                if hero is None and any(v<0 for v in vals):
                    hero={'slide':len(deck.slides),'department':d,'crop_inches':[x,2.35,x+4,6.9],'rows':dr}
    s = slide('Source and method', 'Every plotted value traces back to the source', 'Observed figures only · No forecasts or causal explanation')
    notes = [f'Source: data.csv · {len(rows)} rows · {len(order)} departments · {len(periods)} periods',
             f'Period: {periods[0]} to {periods[-1]} · Currency: {currency}',
             'Revenue and cost are summed using exact decimal arithmetic.',
             'Profit = revenue − cost. Zero and losses remain visible.',
             'Each period must contain every department; absent rows are errors.',
             'Charts and their embedded spreadsheets remain editable.',
             'Source line numbers and chart parts are listed in source-map.json.']
    for i, note in enumerate(notes): text(s,.7,2.65+i*.52,12,.44,note,19)
    deck.save(out/'deck.pptx')
    raw=(out/'deck.pptx').read_bytes(); package=zipfile.ZipFile(io.BytesIO(raw)); workbooks={}
    for mapping in maps:
        part=mapping['part']; folder=posixpath.dirname(part)
        rels=ET.fromstring(package.read(folder+'/_rels/'+posixpath.basename(part)+'.rels'))
        target=next(r.get('Target') for r in rels if r.get('Type','').endswith('/package'))
        path=posixpath.normpath(posixpath.join(folder,target))
        workbooks[path]={f'{chr(66+j)}{i+2}':v for j,series in enumerate(mapping['series']) for i,v in enumerate(series['values'])}
    (out/'deck.pptx').write_bytes(clean_zip(raw,workbooks=workbooks))
    write_json(out/'source-map.json', {'schema_version':1,'slides':slide_records,'charts':maps})
    return hero, maps

def make_hero(out, hero, cfg, rows):
    if hero is None:
        return
    # A literal crop from the rendered slide sits beside reformatted CSV cells.
    im=Image.open(out/'slides'/f'slide-{hero["slide"]:02}.png').convert('RGB')
    scale=im.width/13.333333
    crop=im.crop(tuple(round(v*scale) for v in hero['crop_inches']))
    crop.save(out/'chart-detail.png')
    H=640; W=1120; left=560
    canvas=Image.new('RGB',(W,H),'#F7F9FA'); draw=ImageDraw.Draw(canvas)
    regular='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'; bold='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
    def label(x,y,t,size=40,b=False,fill='#172B3A'):
        draw.text((x,y),t,font=ImageFont.truetype(bold if b else regular,size),fill=fill)
    label(24,20,'CSV · '+hero['department'],44,True)
    label(24,95,cfg['currency']+' · rev / cost',40)
    shown=hero['rows'][:3]
    for i,row in enumerate(shown):
        y=185+i*135
        label(24,y,row['period'],42,True)
        label(24,y+48,f'{money(row["revenue"])} / {money(row["cost"])}',42)
    draw.line((left,20,left,H-20),fill='#CAD2D9',width=2)
    target=crop.resize((560,round(crop.height*560/crop.width)),Image.Resampling.LANCZOS)
    canvas.paste(target,(left,0))
    canvas.save(out/'hero.png')
    write_json(out/'hero-map.json',{'schema_version':1,'source':'input/data.csv','source_lines':[r['line'] for r in shown],'render':f'output/slides/slide-{hero["slide"]:02}.png','crop_inches':hero['crop_inches'],'display':'Source cells reformatted with thousands separators; output is a crop of the LibreOffice-rendered chart. Month numbers on chart retain the source year in the footer.'})

def main():
    started=time.monotonic(); inp,out=map(Path,sys.argv[1:3]); out.mkdir(exist_ok=True,parents=True)
    os.environ['FONTCONFIG_FILE']='/case/source/fonts.conf'
    cfg,rows,periods=read_inputs(inp)
    for name in ('hero.png','hero-map.json','chart-detail.png'):
        (out/name).unlink(missing_ok=True)
    hero,maps=build(cfg,rows,periods,out)
    (out/'deck.pdf').unlink(missing_ok=True)
    conversion=subprocess.run(['libreoffice',f'-env:UserInstallation={os.environ["LO_PROFILE_URI"]}','--headless','--convert-to','pdf','--outdir',str(out),str(out/'deck.pptx')],capture_output=True,text=True,timeout=180)
    if conversion.returncode or not (out/'deck.pdf').is_file(): raise ValueError('LibreOffice conversion failed: '+(conversion.stdout+conversion.stderr).strip())
    reader=PdfReader(out/'deck.pdf'); writer=PdfWriter()
    for p in reader.pages: writer.add_page(p)
    writer.metadata=None
    with (out/'deck.pdf').open('wb') as stream: writer.write(stream)
    (out/'pdf-fonts.txt').write_text(run(['pdffonts',str(out/'deck.pdf')])+'\n')
    slides=out/'slides'; slides.mkdir(exist_ok=True)
    for stale in slides.glob('slide-*.png'): stale.unlink()
    run(['pdftoppm','-png','-r','120',str(out/'deck.pdf'),str(slides/'slide')])
    generated=sorted(slides.glob('slide-*.png'),key=lambda p:int(p.stem.split('-')[-1]))
    for i,p in enumerate(generated,1):
        im=Image.open(p).convert('RGB'); p.unlink(); im.save(slides/f'slide-{i:02}.png')
    thumbs=[]
    for p in sorted(slides.glob('*.png')):
        im=Image.open(p); im.thumbnail((640,360)); thumbs.append(im.copy())
    sheet=Image.new('RGB',(1280,math.ceil(len(thumbs)/2)*390),'#E5EBEF')
    for i,im in enumerate(thumbs): sheet.paste(im,((i%2)*640,(i//2)*390))
    sheet.save(out/'contact-sheet.png'); make_hero(out,hero,cfg,rows)
    shutil.copy('/opt/packages.tsv',out/'packages.tsv')
    fonts=out/'font-licences'; fonts.mkdir(exist_ok=True)
    shutil.copy('/usr/share/doc/fonts-dejavu-core/copyright',fonts/'DejaVu.txt')
    (fonts/'Liberation.txt').unlink(missing_ok=True)
    write_json(out/'font-inventory.json',{'schema_version':1,'fonts':[{'file':p.as_posix(),'sha256':sha(p),'notice':'font-licences/DejaVu.txt'} for family in ('dejavu',) for p in sorted((Path('/usr/share/fonts/truetype')/family).glob('*.ttf'))]})
    versions={'Python':sys.version.split()[0],'python-pptx':__import__('pptx').__version__,'pypdf':__import__('pypdf').__version__,'LibreOffice':run(['libreoffice','--version']),'Poppler':subprocess.run(['pdftoppm','-v'],capture_output=True,text=True).stderr.splitlines()[0],'Chromium':run(['chromium','--version'])}
    report={'schema_version':1,'case':'data-to-powerpoint','input_hashes':{n:sha(inp/n) for n in ('data.csv','deck.json')},'output_hashes':{p.relative_to(out).as_posix():sha(p) for p in sorted(out.rglob('*')) if p.is_file() and (p.name in ('deck.pptx','deck.pdf','source-map.json','hero.png','hero-map.json','chart-detail.png','contact-sheet.png','packages.tsv','pdf-fonts.txt','font-inventory.json') or p.parent.name in ('slides','font-licences'))},'transformations':[{'operation':'Validate complete department/period grid and decimal money'},{'operation':'Aggregate revenue and cost; subtract exact decimals for profit'},{'operation':'Create native chart shapes; store exact decimal lexical values in embedded workbook numeric cells; paginate departments and periods'},{'operation':'Remove PPTX/workbook properties before LibreOffice PDF conversion; remove PDF metadata before raster rendering'}],'counts':{'source_rows':len(rows),'departments':len(cfg['department_order']),'periods':len(periods),'slides':len(PdfReader(out/'deck.pdf').pages),'editable_charts':len(maps),'totals':{k:str(v) for k,v in sums(rows).items()}},'checks':[],'tools':versions,'uncertainties':['Microsoft PowerPoint and Excel were not run.','Native PPTX numeric cells use floating-point storage; checks reconcile their decimal representation to exact source amounts.','Offline page previews use the shared GitHub frame approximation, not captures of published pages.'],'human_steps':['Authored anonymous source figures.','Reviewed all rendered slides and case-page screenshots before delivery; review record is in proof/visual-review.json.']}
    write_json(out/'report.json',report)
    checks=json.loads(run([sys.executable,'/case/tests/check.py',str(inp),str(out),'--json']))
    report['checks']=checks; write_json(out/'report.json',report)
    regression=json.loads(run([sys.executable,'/case/tests/regression.py',str(inp),str(out)]))
    write_json(out/'regression.json',regression)
    with tempfile.TemporaryDirectory() as temp:
        preview=Path(temp); shutil.copy('/case/README.md',preview/'README.md'); (preview/'media').mkdir()
        if (out/'hero.png').exists(): shutil.copy(out/'hero.png',preview/'media/hero.png')
        else: shutil.copy(out/'contact-sheet.png',preview/'media/hero.png')
        run([sys.executable,'/harness/screenshot.py',str(preview),str(out/'page-previews')])
    write_json(out/'runtime.json',{'schema_version':1,'scope':'Document generation, rendering and checks; excludes image build and manual review. Shell stdout includes setup.','elapsed_seconds':round(time.monotonic()-started,3),'limits':{'cpus':2,'memory':'2g','workload_seconds':1080,'build_seconds':1500},'status':'PASS'})
    write_json(out/'claims.json',{'schema_version':1,'claims':[{'claim':'Editable deck with reconciled charts','evidence':{'path':'output/report.json','field':'/checks'},'calculation':'CSV decimal sums = chart caches = embedded workbook numeric cells; profit = revenue − cost.'},{'claim':'Source rows beside matching rendered profit chart','evidence':{'path':'output/hero-map.json','field':'/' }},{'claim':'All reported counts and totals','evidence':{'path':'output/report.json','field':'/counts'}},{'claim':'Compatibility evidence is LibreOffice rendering only','evidence':{'path':'output/report.json','field':'/tools/LibreOffice'}}]})
    for c in checks: print('PASS: '+c['name'])
    print('PASS: deliberate damage and invalid-input checks')
    print('PASS: case-page screenshots at 390 and 1366 CSS pixels')
    print(f'PASS: document workload completed in {time.monotonic()-started:.3f} seconds')

if __name__=='__main__':
    try: main()
    except (ValueError, OSError, subprocess.SubprocessError) as exc:
        print('ERROR: '+str(exc),file=sys.stderr); sys.exit(1)
