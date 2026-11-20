#!/usr/bin/env python3
"""Inspect delivered bytes and prove damaged links/text are rejected."""
import json, sys, tempfile, zipfile
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'source'))
from book import inspect, digest, run
from browser import exercise

def negative(inp,epub):
    outcomes=[]
    for name,entry,old,new in [
        ('broken forward','EPUB/chapter.xhtml',b'notes.xhtml#note-1',b'notes.xhtml#absent'),
        ('wrong return','EPUB/notes.xhtml',b'chapter.xhtml#ref-1"',b'chapter.xhtml#ref-2"'),
        ('lost body text','EPUB/chapter.xhtml',b'notebook',b'notebok'),
        ('lost note text','EPUB/notes.xhtml',b'observation',b'observatio')]:
        with tempfile.TemporaryDirectory() as td:
            target=Path(td)/'damaged.epub'
            with zipfile.ZipFile(epub) as src,zipfile.ZipFile(target,'w') as dst:
                for info in src.infolist():
                    data=src.read(info.filename)
                    if info.filename==entry:
                        assert old in data,'mutation target missing'; data=data.replace(old,new,1)
                    dst.writestr(info,data)
            try: inspect(inp,target)
            except AssertionError as e: outcomes.append({'damage':name,'rejected':True,'diagnostic':str(e)})
            else: raise AssertionError('damaged EPUB was accepted: '+name)
    return outcomes

def check(inp,out,browser=True):
    mapping=inspect(inp,out/'book.epub')
    validation=run(['java','-jar','/usr/share/java/epubcheck.jar',str(out/'book.epub')])
    assert 'WARNING' not in validation,'EPUBCheck warning'
    assert json.loads((out/'source-map.json').read_text())==mapping,'source map mismatch'
    if (out/'report.json').exists():
        report=json.loads((out/'report.json').read_text())
        assert report['counts']['references']==len(mapping['references']),'reported reference count differs'
        assert report['counts']['unique_notes']==len(mapping['notes']),'reported note count differs'
        assert report['counts']['browser_journeys']==4*len(mapping['references']),'reported browser count differs'
        for name,sha in report['input_hashes'].items(): assert digest(inp/name)==sha,'input hash mismatch: '+name
        for name,sha in report['output_hashes'].items(): assert digest(out/name)==sha,'output hash mismatch: '+name
    damaged=negative(inp,out/'book.epub')
    if browser: exercise(out/'book.epub',mapping)
    print('PASS: EPUB structure, source text, every forward/return link and damaged-file rejection')
    return damaged
if __name__=='__main__':
    try: check(Path(sys.argv[1]),Path(sys.argv[2]))
    except Exception as e: print('FAIL: '+str(e),file=sys.stderr); sys.exit(1)
