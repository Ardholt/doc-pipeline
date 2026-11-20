"""Replacement-input and diagnostic contract checks."""
import json,tempfile
from pathlib import Path
from book import build,inspect

def contracts():
    rows=[]
    with tempfile.TemporaryDirectory() as td:
        inp=Path(td)/'input with spaces';out=Path(td)/'output with spaces';inp.mkdir();out.mkdir()
        def settings():
            (inp/'book.json').write_text(json.dumps({'schema_version':1,'title':'Paper & light','language':'en-GB','identifier':'urn:book:paper-light'}))
        settings()
        (inp/'manuscript.md').write_text('# Paper & light\n\nCafé — a quiet pause.[^pause]\n\n- Keep **both** words.\n- Read again.[^pause]\n\n[^pause]: An unhurried interval.\n')
        build(inp,out); mapping=inspect(inp,out/'book.epub')
        assert len(mapping['references'])==2 and len(mapping['notes'])==1
        rows.append({'case':'replacement title, Unicode, list and shared note in paths with spaces','passed':True})
        for title,content in [('undefined note','# Heading\n\nText.[^absent]'),('unsupported raw content','# Heading\n\n<script>test</script>\n\nText.[^n]\n\n[^n]: Note.'),('empty manuscript','')]:
            (inp/'manuscript.md').write_text(content)
            try: build(inp,out)
            except ValueError as e: rows.append({'case':title,'passed':True,'diagnostic':str(e)})
            else: raise AssertionError(title+' accepted')
        (inp/'book.json').write_text('{"schema_version":true}')
        try: build(inp,out)
        except ValueError as e: rows.append({'case':'invalid schema version type','passed':True,'diagnostic':str(e)})
        else: raise AssertionError('boolean schema version accepted')
        settings()
        (inp/'manuscript.md').unlink()
        try: build(inp,out)
        except ValueError as e: rows.append({'case':'missing manuscript','passed':True,'diagnostic':str(e)})
        else: raise AssertionError('missing input accepted')
    return rows
