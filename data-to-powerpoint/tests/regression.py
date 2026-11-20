"""Damage independent copies and require the output checker to reject them."""
import io, json, shutil, sys, tempfile, zipfile
from pathlib import Path
from xml.etree import ElementTree as ET
from check import inspect, NS, read_inputs, sums, money

def rewrite(raw, target, mutate):
    z=zipfile.ZipFile(io.BytesIO(raw)); buf=io.BytesIO()
    with zipfile.ZipFile(buf,'w',zipfile.ZIP_DEFLATED) as dst:
        for name in z.namelist(): dst.writestr(name,mutate(z.read(name)) if name==target else z.read(name))
    return buf.getvalue()

def run(inp,out):
    records=[]
    with tempfile.TemporaryDirectory() as temp:
        base=Path(temp); dest=base/'output'; shutil.copytree(out,dest)
        original=(dest/'deck.pptx').read_bytes()
        def reject(name,raw):
            (dest/'deck.pptx').write_bytes(raw)
            try: inspect(inp,dest,hashes=False)
            except (ValueError,KeyError) as exc: records.append({'test':name,'passed':True,'diagnostic':str(exc)})
            else: raise ValueError('corruption accepted: '+name)
            (dest/'deck.pptx').write_bytes(original)
        def cache(raw):
            root=ET.fromstring(raw); root.find('.//c:val/c:numRef/c:numCache/c:pt/c:v',NS).text='123.45'; return ET.tostring(root)
        reject('changed chart value',rewrite(original,'ppt/charts/chart1.xml',cache))
        z=zipfile.ZipFile(io.BytesIO(original)); embedded=next(n for n in z.namelist() if n.endswith('.xlsx'))
        def sheet(raw):
            root=ET.fromstring(raw)
            for c in root.findall('.//s:c',NS):
                if c.get('r')=='B2': c.find('s:v',NS).text='123.45'
            return ET.tostring(root)
        reject('changed embedded workbook value',rewrite(original,embedded,lambda raw:rewrite(raw,'xl/worksheets/sheet1.xml',sheet)))
        _,source_rows,_=read_inputs(inp)
        target=money(sums(source_rows)['revenue']).encode()
        reject('changed visible total',rewrite(original,'ppt/slides/slide1.xml',lambda raw:raw.replace(target,b'999,999,999,999')))
        source=base/'input';shutil.copytree(Path('/case/input'),source)
        csv=(source/'data.csv').read_text();cfg=(source/'deck.json').read_text()
        cases={'duplicate row':csv+csv.splitlines()[1]+'\n','missing money':csv.replace('12000.00','',1),'negative revenue':csv.replace('12000.00','-1.00',1),'excess precision':csv.replace('12000.00','1.001',1),'missing department-period': '\n'.join(csv.splitlines()[:-1])+'\n','invalid month':csv.replace('2026-01','2026-13',1)}
        for name,content in cases.items():
            (source/'data.csv').write_text(content)
            try: read_inputs(source)
            except ValueError as exc: records.append({'test':name,'passed':True,'diagnostic':str(exc)})
            else: raise ValueError('invalid input accepted: '+name)
        (source/'data.csv').write_text(csv)
        config=json.loads(cfg); config['department_order']=['A','B'];(source/'deck.json').write_text(json.dumps(config))
        try: read_inputs(source)
        except ValueError as exc: records.append({'test':'incomplete department order','passed':True,'diagnostic':str(exc)})
        else: raise ValueError('incomplete order accepted')
        (source/'deck.json').write_text(cfg)
        (source/'data.csv').write_text(csv.replace('12000.00','0.01',1))
        _,valid,_=read_inputs(source)
        if str(valid[0]['profit'])!='-7999.99': raise ValueError('decimal cents arithmetic failed')
        records.append({'test':'decimal cents and negative profit','passed':True,'diagnostic':'Exact decimal subtraction preserves cents and sign.'})
    return {'schema_version':1,'checks':records}

if __name__=='__main__':
    try:
        result=run(Path(sys.argv[1]),Path(sys.argv[2])); print(json.dumps(result,indent=2))
    except Exception as exc: print('FAIL: '+str(exc),file=sys.stderr);sys.exit(1)
