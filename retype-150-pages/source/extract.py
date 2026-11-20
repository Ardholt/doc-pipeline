"""OCR and structure inference. Reads page pixels only; no reference access."""
import csv, io, statistics
from common import block_text


def parse_tsv(tsv):
    lines={}; confidences=[]
    for row in csv.DictReader(io.StringIO(tsv),delimiter='\t',quoting=csv.QUOTE_NONE):
        if row['level']!='5' or not row['text'].strip():continue
        word={k:int(row[k]) for k in ('left','top','width','height')}
        word['text']=row['text']; word['confidence']=float(row['conf'])
        key=tuple(row[k] for k in ('page_num','block_num','par_num','line_num'))
        lines.setdefault(key,[]).append(word); confidences.append(word['confidence'])
    result=[]
    for words in lines.values():
        words.sort(key=lambda w:w['left'])
        char=statistics.median(w['width']/max(1,len(w['text'])) for w in words)
        groups=[]; text=''; right=None
        for w in words:
            if right is not None and w['left']-right>char*3.5:
                groups.append(text); text=''
            text+=(' ' if text else '')+w['text']; right=w['left']+w['width']
        groups.append(text)
        result.append({'top':min(w['top'] for w in words),'bottom':max(w['top']+w['height'] for w in words),'groups':groups,'words':words})
    result.sort(key=lambda r:(r['top'],r['words'][0]['left']))
    return result,confidences


def infer_blocks(lines):
    if not lines:raise ValueError('No readable words on scan page')
    gaps=[b['top']-a['top'] for a,b in zip(lines,lines[1:]) if b['top']>a['top']]
    baseline=statistics.median(gaps) if gaps else 40
    body_height=statistics.median(max(w['height'] for w in line['words']) for line in lines)
    blocks=[]; pending=[]
    def flush():
        if pending:blocks.append({'kind':'paragraph','text':' '.join(pending)}); pending.clear()
    i=0; previous=None
    while i<len(lines):
        row=lines[i]; groups=row['groups']
        if len(groups)>=2:
            end=i+1
            while end<len(lines) and len(lines[end]['groups'])==len(groups) and lines[end]['top']-lines[end-1]['top']<baseline*1.7:end+=1
            if end-i>=2:
                flush(); blocks.append({'kind':'table','rows':[l['groups'] for l in lines[i:end]]}); previous=lines[end-1]; i=end; continue
        text=' '.join(groups)
        letters=[c for c in text if c.isalpha()]
        mostly_upper=bool(letters) and sum(c.isupper() for c in letters)/len(letters)>=0.85
        larger_type=max(w['height'] for w in row['words'])>body_height*1.15
        gap_after=i+1<len(lines) and lines[i+1]['top']-row['top']>baseline*1.25
        if len(text)<100 and (mostly_upper or (larger_type and gap_after)):
            flush(); blocks.append({'kind':'heading','text':text})
        else:
            if previous and row['top']-previous['top']>baseline*1.35:flush()
            pending.append(text)
        previous=row; i+=1
    flush(); return blocks


def review_rows(path,count):
    if not path.exists():return []
    if not path.is_file():raise ValueError('review.csv must be a regular file')
    with path.open(newline='',encoding='utf-8-sig') as f:
        reader=csv.DictReader(f)
        if reader.fieldnames!=['page','find','replace','reason']:raise ValueError('review.csv requires page,find,replace,reason columns in that order')
        rows=[]
        for n,r in enumerate(reader,2):
            if None in r or any(v is None for v in r.values()):raise ValueError(f'review.csv row {n}: invalid column count')
            try:p=int(r['page'])
            except ValueError:raise ValueError(f'review.csv row {n}: page must be an integer')
            if not 1<=p<=count:raise ValueError(f'review.csv row {n}: page outside scan')
            if not r['find'] or not r['reason'].strip():raise ValueError(f'review.csv row {n}: find and reason must be nonempty')
            rows.append({**r,'page':p,'row':n})
        return rows


def apply_review(text,rows,page):
    events=[]
    for row in rows:
        if row['page']!=page:continue
        found=0; start=0
        while True:
            position=text.find(row['find'],start)
            if position<0:break
            found+=1; start=position+1
        if found!=1:raise ValueError(f"review.csv row {row['row']}, page {page}: expected one literal match, found {found}")
        before=text; text=text.replace(row['find'],row['replace'],1)
        events.append({**row,'matches':found})
    return text,events


def restore_blocks(text,original):
    """Parse reviewed structure, retaining original styles when boundaries survive."""
    chunks=text.split('\n\n')
    result=[]
    for i,chunk in enumerate(chunks):
        if not chunk.strip():continue
        if '\t' in chunk:
            rows=[r.split('\t') for r in chunk.split('\n')]
            if len({len(r) for r in rows})!=1:raise ValueError('Review produced a nonrectangular table')
            result.append({'kind':'table','rows':rows})
        else:
            kind=original[i]['kind'] if len(chunks)==len(original) and original[i]['kind']!='table' else ('heading' if chunk.isupper() and len(chunk)<100 else 'paragraph')
            result.append({'kind':kind,'text':chunk})
    return result
