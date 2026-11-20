#!/usr/bin/env python3
import importlib.metadata, json, os, shutil, subprocess, sys, time
from pathlib import Path
from PIL import Image
from book import build, inspect, dump, digest, run
from browser import exercise
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'tests'))
from check import negative
from contracts import contracts

start=time.monotonic(); inp,out=map(Path,sys.argv[1:3]); out.mkdir(exist_ok=True,parents=True)
try:
    mapping=build(inp,out)
    mapping=inspect(inp,out/'book.epub')
    proc=subprocess.run(['java','-jar','/usr/share/java/epubcheck.jar',str(out/'book.epub')],capture_output=True,text=True,timeout=180)
    log=(proc.stdout+proc.stderr).replace(str(out/'book.epub'),'book.epub')
    (out/'epubcheck.log').write_text(log)
    if proc.returncode or 'WARNING' in log: raise ValueError('EPUBCheck error or warning; see epubcheck.log')
    print('PASS: EPUBCheck; no errors or warnings',flush=True)
    audit=exercise(out/'book.epub',mapping,out)
    dump(out/'negative-tests.json',{'schema_version':1,'tests':negative(inp,out/'book.epub'),'input_contracts':contracts()})
    print(f'PASS: {len(audit["runs"])} browser tap-and-return journeys at narrow/wide widths and enlarged text',flush=True)
    # The proof image is cropped actual EPUB content, never re-typeset prose.
    first=Image.open(out/'passage-detail.png').convert('RGB')
    note=Image.open(out/'note-detail.png').convert('RGB')
    # Keep the opening sentence and complete first note with its return destinations.
    first=first.crop((0,0,first.width,min(first.height,30)))
    hero=Image.new('RGB',(max(first.width,note.width),first.height+note.height+10),'#fffdf8')
    hero.paste(first,(0,0));hero.paste(note,(0,first.height+10));hero.save(out/'hero.png')
    shutil.copy('/opt/packages.tsv',out/'packages.tsv')
    shutil.copy('/usr/share/doc/fonts-dejavu-core/copyright',out/'font-license.txt')
    (out/'pip-freeze.txt').write_text(run(['pip','freeze']))
    (out/'font-selection.txt').write_text(run(['fc-match','DejaVu Serif'])+run(['fc-match','DejaVu Sans'])+run(['fc-match','DejaVu Sans Mono']))
    tools={'python':sys.version.split()[0],'pandoc':run(['pandoc','--version']).splitlines()[0],'epubcheck':next(line for line in subprocess.run(['java','-jar','/usr/share/java/epubcheck.jar','--version'],capture_output=True,text=True,timeout=30).stdout.splitlines() if line.startswith('EPUBCheck v')),'chromium':run(['chromium','--version']).strip(),'reader':'Custom iframe browser reader 1.0','playwright':importlib.metadata.version('playwright'),'lxml':importlib.metadata.version('lxml'),'Pillow':importlib.metadata.version('Pillow')}
    counts={'unique_notes':len(mapping['notes']),'references':len(mapping['references']),'repeated_references':len(mapping['references'])-len(mapping['notes']),'browser_journeys':len(audit['runs']),'viewport_widths_css_px':[390,1366],'text_percent':[100,150],'epubcheck_errors':0,'epubcheck_warnings':0}
    report={'schema_version':1,'case':'kindle-tappable-footnotes','input_hashes':{f:digest(inp/f) for f in ['manuscript.md','book.json']},'output_hashes':{f:digest(out/f) for f in ['book.epub','source-map.json','epubcheck.log','browser-audit.json','negative-tests.json','hero.png']},'transformations':[{'operation':'parse Pandoc Markdown AST','parameters':{'normalization':mapping['normalization']}},{'operation':'deduplicate identical notes and allocate unique reference IDs','parameters':{'return_policy':'one labelled backlink per reference'}},{'operation':'package reflowable EPUB 3','parameters':{'spine':['chapter.xhtml','notes.xhtml'],'metadata':'title, language, identifier and fixed required modified timestamp only','archive_timestamp':'2026-01-01T00:00:00Z'}},{'operation':'validate and render delivered EPUB','parameters':{'browser':'Chromium','reader':'custom iframe reader','widths':[390,1366],'text_percent':[100,150]}}],'counts':counts,'checks':[{'name':'EPUBCheck','passed':True,'observation':'No errors or warnings; epubcheck.log'},{'name':'source conservation','passed':True,'observation':'All body and note text compared against parsed input under documented whitespace normalization; source-map.json'},{'name':'forward and return links','passed':True,'observation':'Every reference checked structurally and clicked in the browser at every width/text setting; browser-audit.json'},{'name':'damage detection','passed':True,'observation':'Broken forward, wrong return, lost body and lost note text rejected; negative-tests.json'}],'tools':tools,'uncertainties':['No Kindle device, Kindle Previewer, native note popup or KDP acceptance test was available.','Browser reader is a custom iframe reader using extracted EPUB XHTML; it is not a Kindle emulator.','Case-page screenshots are offline local renders, not published GitHub or Pages captures.'],'human_steps':['Original manuscript authored for this case.','Rendered reader and case-page screenshots reviewed after the run; review recorded separately in proof/visual-review.json.']}
    dump(out/'report.json',report)
    dump(out/'claims.json',{'schema_version':1,'claims':[
        {'claim':'Reflowable EPUB with tested tap-and-return navigation','kind':'machine','evidence':[{'path':'output/book.epub','members':['EPUB/package.opf','EPUB/chapter.xhtml','EPUB/notes.xhtml']},{'path':'output/browser-audit.json','pointer':'/runs'}]},
        {'claim':f'{counts["references"]} references to {counts["unique_notes"]} notes','kind':'machine','evidence':[{'path':'output/report.json','pointer':'/counts'},{'path':'output/source-map.json','pointer':'/references'}]},
        {'claim':f'{counts["browser_journeys"]} completed browser journeys','kind':'machine','evidence':[{'path':'output/browser-audit.json','pointer':'/runs'}],'calculation':'reference count × 2 viewport widths × 2 text sizes'},
        {'claim':'390 and 1366 CSS pixel widths, 100% and 150% text','kind':'machine','evidence':[{'path':'output/browser-audit.json','pointer':'/runs'}]},
        {'claim':'No EPUBCheck errors or warnings','kind':'machine','evidence':[{'path':'output/epubcheck.log','line':2},{'path':'output/report.json','pointer':'/tools/epubcheck'}]},
        {'claim':'Body, Unicode, lists and notes preserved under documented normalization','kind':'machine','evidence':[{'path':'output/source-map.json','pointer':''},{'path':'output/report.json','pointer':'/checks/1'}]},
        {'claim':'Damaged links and text are rejected','kind':'machine','evidence':[{'path':'output/negative-tests.json','pointer':'/tests'}]},
        {'claim':'Hero and reader images show delivered EPUB content; numbers in the figures identify notes and return passages','kind':'render','evidence':[{'path':'output/hero.png','frame':'complete image: passage and first note crops'},{'path':'output/browser-audit.json','pointer':'/runs'},{'path':'output/source-map.json','pointer':'/references'}]},
        {'claim':'Visual readability review is separate from automated link checks','kind':'visual review','evidence':[{'path':'proof/visual-review.json','pointer':'/images'}]},
        {'claim':'Kindle device, Previewer, native popup and KDP acceptance not tested','kind':'untested compatibility','evidence':[{'path':'output/report.json','pointer':'/uncertainties/0'}]}
    ]})
    dump(out/'runtime.json',{'schema_version':1,'scope':'EPUB generation, validation, browser checks and proof image; excludes container setup, manuscript authoring, page screenshots and visual review','elapsed_seconds':round(time.monotonic()-start,3),'limits':{'cpus':2,'memory':'2g','workload_timeout_seconds':1080,'network':'none'},'status':'PASS'})
    # Page proof uses the shared screenshot step and the final tracked case image.
    subprocess.run(['python','/harness/screenshot.py','/case',str(out/'page-previews')],check=True,timeout=300,env=dict(os.environ,FONTCONFIG_FILE='/case/source/fonts.conf'))
    print('PASS: source text and note text preserved; four damaged-file checks rejected',flush=True)
except Exception as e:
    print('FAIL: '+str(e),file=sys.stderr); sys.exit(1)
