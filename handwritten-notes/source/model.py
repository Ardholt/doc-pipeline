"""Validate the public transcription contract before opening a converter."""
import json
from pathlib import Path
from PIL import Image

def load(root):
    try:
        pages=json.loads((root/'pages.json').read_text())
        transcript=json.loads((root/'transcript.json').read_text())
    except (OSError,ValueError) as e:
        raise ValueError('pages.json and transcript.json must be readable UTF-8 JSON') from e
    validate(root,pages,transcript)
    return pages,transcript

def validate(root,pages,transcript):
    for name,obj in [('pages.json',pages),('transcript.json',transcript)]:
        if not isinstance(obj,dict) or type(obj.get('schema_version')) is not int or obj['schema_version']!=1 or not isinstance(obj.get('pages'),list) or not obj['pages']:
            raise ValueError(name+': expected schema_version 1 and nonempty pages array')
    ids=[]
    for p in pages['pages']:
        if not isinstance(p,dict) or not isinstance(p.get('id'),str) or not p['id'].strip() or not isinstance(p.get('file'),str):
            raise ValueError('pages.json: each page needs string id and file')
        if p['id'] in ids: raise ValueError('pages.json: duplicate page id '+p['id'])
        ids.append(p['id']); path=root/p['file']
        if path.is_symlink() or not path.resolve().is_relative_to(root.resolve()) or path.suffix.lower() not in ('.png','.jpg','.jpeg'):
            raise ValueError('pages.json: image must be a local PNG/JPEG inside input')
        try:
            with Image.open(path) as im:
                if im.format not in ('PNG','JPEG'): raise ValueError('image content must be PNG/JPEG')
                im.verify()
        except (OSError,ValueError) as e: raise ValueError('pages.json: unreadable image '+p['file']) from e
    tids=[]
    for p in transcript['pages']:
        if not isinstance(p,dict) or not isinstance(p.get('id'),str) or p['id'] in tids:
            raise ValueError('transcript.json: missing or duplicate page id')
        tids.append(p['id'])
        if not isinstance(p.get('blocks'),list) or not p['blocks'] or not isinstance(p.get('uncertainties'),list):
            raise ValueError('transcript.json: blocks must be nonempty; uncertainties must be an array')
        blocks={}
        for b in p['blocks']:
            if not isinstance(b,dict) or not isinstance(b.get('id'),str) or not b['id'].strip() or b['id'] in blocks:
                raise ValueError('transcript.json: missing or duplicate block id')
            if b.get('kind') not in ('heading','paragraph','bullet') or not isinstance(b.get('text'),str) or not b['text'].strip() or any(ord(c)<32 and c not in '\n\t' for c in b['text']):
                raise ValueError('transcript.json: invalid block kind or text')
            blocks[b['id']]=b
        marked={k:b['text'].count('[unclear]') for k,b in blocks.items()}
        listed={k:0 for k in blocks}
        for u in p['uncertainties']:
            if not isinstance(u,dict) or u.get('block_id') not in blocks or u.get('token')!='[unclear]' or not isinstance(u.get('reason'),str) or not u['reason'].strip():
                raise ValueError('transcript.json: uncertainty needs an existing block, literal [unclear] and a reason')
            listed[u['block_id']]+=1
        if marked!=listed: raise ValueError('transcript.json: every [unclear] occurrence needs one uncertainty entry')
    if set(ids)!=set(tids) or len(ids)!=len(tids): raise ValueError('transcript.json: every source page must occur exactly once')

def ordered(pages,transcript):
    byid={p['id']:p for p in transcript['pages']}
    return [byid[p['id']] for p in pages['pages']]

def text(pages,transcript):
    return '\n\n'.join('\n'.join(b['text'] for b in p['blocks']) for p in ordered(pages,transcript))+'\n'

def mapping(pages,transcript):
    result=[]; index=0
    for src,p in zip(pages['pages'],ordered(pages,transcript)):
        rows=[]
        for b in p['blocks']:
            rows.append({'block_id':b['id'],'kind':b['kind'],'text':b['text'],'docx_paragraph_index':index})
            index+=1
        result.append({'page_id':p['id'],'source_file':src['file'],'blocks':rows})
    return {'schema_version':1,'pages':result,'crossed_out_policy':'Omit struck-out words; record each omission in a reviewed decision record before the transcript is formatted.'}

def uncertainty(pages,transcript):
    return {'schema_version':1,'uncertainties':[dict(page_id=p['id'],**u) for p in ordered(pages,transcript) for u in p['uncertainties']]}
