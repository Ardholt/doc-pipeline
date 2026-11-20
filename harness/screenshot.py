"""Offline README previews using a local GitHub-style frame and the Pages layout."""
import base64, hashlib, html, json, re, shutil, subprocess, sys, tempfile
from pathlib import Path
import markdown
from PIL import Image
case,out=map(Path,sys.argv[1:3]); here=Path(__file__).resolve().parent
out.mkdir(parents=True,exist_ok=True)
md=(case/'README.md').read_text(); body=markdown.markdown(md,extensions=['tables','fenced_code'])
def embed(match):
    source=match.group(1)
    if source.startswith('https://'): return 'src="data:image/svg+xml;base64,'+base64.b64encode(b'<svg xmlns="http://www.w3.org/2000/svg" width="148" height="20"><rect width="148" height="20" fill="#555"/><text x="6" y="14" fill="white" font-size="11">CI status requires network</text></svg>').decode()+'"'
    p=case/source
    return 'src="data:image/png;base64,'+base64.b64encode(p.read_bytes()).decode()+'"'
body=re.sub(r'src="([^"]+)"',embed,body)
slug=json.loads((out.parent/'report.json').read_text()).get('case',case.name)
font_css='body,.markdown-body{font-family:DejaVu Sans,sans-serif}.md h1,.md td:not(:first-child){font-family:DejaVu Serif,serif}code,pre,.meta{font-family:DejaVu Sans Mono,monospace}'
css=(here/'vendor/github-markdown.css').read_text()+(here/'vendor/github-frame.css').read_text()+font_css
head='<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
frame=f'''<div class="gh-h"><b style="font-size:25px">◉</b><div class="nav"><span>Product ▾</span><span>Solutions ▾</span><span>Resources ▾</span><span>Pricing</span></div><div class="sp"></div><span class="in">Sign in</span><span class="up">Sign up</span></div>
<div class="gh-r"><div class="own">Ardholt / <b>doc-pipeline</b></div><div class="tabs"><span class="on">Code</span><span>Issues</span><span class="x">Pull requests</span><span class="x">Actions</span></div></div>
<div style="display:flex"><div class="tree"><b>Files</b><p class="btn">main ▾</p><div class="it">harness</div><div class="it on">{slug}</div><div class="it">README.md</div></div>
<div style="flex:1;min-width:0;padding:0 16px 40px"><div class="gh-m" style="display:flex;gap:16px;align-items:center;padding:16px 0 4px"><span style="font-size:16px">← Files</span><span class="btn" style="font-size:16px">main ▾</span></div>
<div class="crumb"><a>doc-pipeline</a> / <a>{slug}</a> / README.md</div>
<div class="gh-m meta" style="padding:16px 4px 0">{len(md.splitlines())} lines · {len(md.encode())/1024:.1f} KB</div><div class="box tb" style="border-bottom:0"><div class="seg"><span class="on">Preview</span><span>Code</span><span>Blame</span></div></div><div class="mdwrap"><article class="markdown-body">{body}</article></div></div></div>'''
gh='<!doctype html><html lang="en"><head>'+head+'<style>'+css+'</style></head><body>'+frame+'</body></html>'
layout=(here/'pages/_layouts/default.html').read_text()
layout=re.sub(r'{% assign hero[\s\S]*?{% endif %}','',layout)
layout=re.sub(r'{%[\s\S]*?%}','',layout)
layout=layout.replace("{{ '/' | relative_url }}",'../').replace('{{ site.title }}','Document pipelines').replace('{{ content }}',body)
layout=re.sub(r'{{[^}]*}}','',layout).replace('</head>','<style>'+(here/'pages/assets/site.css').read_text()+font_css+'</style></head>')
# Headless Chromium will not make its window narrower than 500 px, so each page is shown in an iframe of exactly the stated width:
# the page then lays out, and its media queries apply, at 390 or 1366 CSS pixels. The wrapper is a render source only and is not kept.
CHROME=['chromium','--headless','--no-sandbox','--disable-gpu','--disable-dev-shm-usage','--no-proxy-server','--hide-scrollbars','--force-device-scale-factor=1']
def wrapper(content,w,h,script=''):
    return f'<!doctype html><meta charset="utf-8"><body style="margin:0;background:#fff"><iframe id="v" srcdoc="{html.escape(content,quote=True)}" style="display:block;border:0;width:{w}px;height:{h}px"></iframe>{script}</body>'
# Added to a separate copy of the wrapper, never to the screenshot: measures sideways overflow of the README content inside the frame.
MEASURE='''<script>addEventListener('load',()=>{const f=document.getElementById('v'),d=f.contentDocument,root=d.documentElement,scope=d.querySelector('article.markdown-body,main.md'),edge=e=>e.getBoundingClientRect().right;let right=0,who='';
for(const e of scope.querySelectorAll('*')){if(e.closest('pre')||!e.getClientRects().length)continue;if(edge(e)>right){right=edge(e);who=e.tagName.toLowerCase()}}
const bad=[...scope.querySelectorAll('table')].filter(t=>t.scrollWidth>t.clientWidth+1||edge(t)>root.clientWidth+1).map(t=>{const c=[...t.querySelectorAll('th,td')].sort((a,b)=>b.getBoundingClientRect().width-a.getBoundingClientRect().width).slice(0,12).map(c=>({text:c.textContent.trim().slice(0,60),width:Math.round(c.getBoundingClientRect().width)}));return {table_width:Math.round(t.getBoundingClientRect().width),scroll_width:t.scrollWidth,client_width:t.clientWidth,widest_cells:c}});
const m=document.createElement('pre');m.id='dp-measure';m.textContent=JSON.stringify({viewport_width:root.clientWidth,document_scroll_width:root.scrollWidth,content_right_edge:Math.round(right*10)/10,widest_element:who,tables_wider_than_view:bad});document.body.appendChild(m)})</script>'''
def measure(content,w,h,probe):
    probe.write_text(wrapper(content,w,h,MEASURE))
    proc=subprocess.run(CHROME+[f'--window-size={max(w,500)},{h}','--virtual-time-budget=1500','--dump-dom',probe.as_uri()],capture_output=True,timeout=60,text=True)
    found=re.search(r'<pre id="dp-measure">(.*?)</pre>',proc.stdout,re.S)
    if proc.returncode or not found: raise ValueError('Chromium overflow measurement failed')
    m=json.loads(html.unescape(found.group(1)))
    if m['viewport_width']!=w: raise ValueError(f'Frame laid out at {m["viewport_width"]} px, not {w} px')
    m['horizontal_overflow']=m['document_scroll_width']>m['viewport_width'] or m['content_right_edge']>m['viewport_width']+0.5 or bool(m['tables_wider_than_view'])
    return m
records=[]
work=Path(tempfile.mkdtemp(prefix='dp-render-'))  # the local frame and Pages-layout pages are only render sources; neither is kept in the output
for kind,content in [('github',gh),('pages',layout)]:
    for w,h in [(390,844),(1366,768)]:
        path=work/f'{kind}-{w}.html'; path.write_text(wrapper(content,w,h))
        shot=out/f'{kind}-{w}.png'
        proc=subprocess.run(CHROME+[f'--window-size={max(w,500)},{h}','--run-all-compositor-stages-before-draw','--virtual-time-budget=1500',f'--screenshot={shot}',path.as_uri()],capture_output=True,timeout=60)
        if proc.returncode or not shot.is_file(): raise ValueError('Chromium screenshot failed')
        im=Image.open(shot).convert('RGB').crop((0,0,w,h)); im.save(shot)
        records.append({'file':shot.name,'css_width':w,'css_height':h,'device_scale_factor':1,'measured':measure(content,w,h,work/f'{kind}-{w}-measure.html')})
shutil.rmtree(work)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
(out/'screenshots.json').write_text(json.dumps({'schema_version':1,'renderer':subprocess.check_output(['chromium','--version'],text=True).strip(),'screenshots':records,'measured_files':{'README.md':sha(case/'README.md'),'site.css':sha(here/'pages/assets/site.css')},'surface':'offline local render in a local GitHub-style frame, not a live github.com capture','badge':'offline placeholder says CI status requires network; no passing CI claim'},indent=2)+'\n')
wide=[r['file'] for r in records if r['measured']['horizontal_overflow']]
if wide: raise ValueError('Horizontal overflow in the rendered README at: '+', '.join(wide)+' (see screenshots.json)')
print('PASS: case-page screenshots at 390 and 1366 CSS pixels, no horizontal overflow')
