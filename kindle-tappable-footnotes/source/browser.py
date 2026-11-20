"""Drive native anchor navigation in a custom Chromium EPUB browser reader."""
import json, shutil, tempfile, zipfile
from pathlib import Path
from PIL import Image
from playwright.sync_api import sync_playwright
from book import dump

def exercise(epub,mapping,out=None):
    rows=[]
    with tempfile.TemporaryDirectory() as td:
        root=Path(td)
        with zipfile.ZipFile(epub) as z: z.extractall(root)
        shutil.copyfile(Path(__file__).parent/'reader.html',root/'reader.html')
        with sync_playwright() as p:
            browser=p.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox','--disable-dev-shm-usage','--allow-file-access-from-files'])
            version=browser.version
            for width in [390,1366]:
                for scale in [100,150]:
                    page=browser.new_page(viewport={'width':width,'height':844},device_scale_factor=1)
                    page.goto((root/'reader.html').as_uri())
                    page.locator('#size').select_option(str(scale))
                    frame=page.frames[1]
                    frame.wait_for_selector('#ref-1')
                    frame.wait_for_function('document.documentElement.style.fontSize === "'+str(scale)+'%"')
                    def reflow():
                        return frame.evaluate('''() => ({width:innerWidth, scroll:document.documentElement.scrollWidth, font:getComputedStyle(document.body).fontSize, clipped:[...document.querySelectorAll('p,li,h1,h2,aside')].filter(e=>e.scrollHeight>e.clientHeight+1 && ['hidden','clip'].includes(getComputedStyle(e).overflowY)).length})''')
                    before=reflow(); assert before['scroll']<=before['width'] and before['clipped']==0,'body does not reflow'
                    # Exercise the shipped navigation document, then resume reading.
                    page.get_by_text('Contents',exact=True).click()
                    frame.wait_for_selector('#toc'); frame.locator('nav a').first.click(); frame.wait_for_selector('#ref-1')
                    for r in mapping['references']:
                        a=frame.locator('#'+r['reference_id']); a.scroll_into_view_if_needed()
                        if out and width==390 and scale==100 and r['reference_id']=='ref-1':
                            page.screenshot(path=str(out/'reader-passage.png'))
                            a.locator('..').screenshot(path=str(out/'passage-detail.png'))
                        a.click()
                        frame.wait_for_url('**/notes.xhtml#'+r['note_id'])
                        target=frame.locator('#'+r['note_id']); assert target.is_visible(),'note not visible'
                        assert frame.evaluate('location.hash')=='#'+r['note_id'],'wrong note opened'
                        assert target.locator('.note-text').inner_text().split()==next(n['text'] for n in mapping['notes'] if n['id']==r['note_id']).split(),'rendered note text differs'
                        note_layout=reflow(); assert note_layout['scroll']<=note_layout['width'] and note_layout['clipped']==0,'note does not reflow'
                        if out and r['reference_id']=='ref-1':
                            page.screenshot(path=str(out/f'reader-note-{width}-{scale}.png'))
                            if width==390 and scale==100: target.screenshot(path=str(out/'note-detail.png'))
                        back=target.locator('a[href="'+r['return']+'"]'); back.click()
                        frame.wait_for_url('**/chapter.xhtml#'+r['reference_id'])
                        returned=frame.locator('#'+r['reference_id'])
                        assert returned.is_visible(),'return marker not visible'
                        rect=returned.bounding_box(); assert rect and rect['y']>=0 and rect['y']<844,'return is outside the viewport'
                        assert float(reflow()['font'].removesuffix('px'))==16*scale/100,'enlarged text was lost'
                        rows.append(dict(r,width=width,text_percent=scale,forward_passed=True,return_passed=True,no_horizontal_scroll=True,no_clipping=True))
                    if out: page.screenshot(path=str(out/f'reader-return-{width}-{scale}.png'))
                    page.close()
            browser.close()
    result={'schema_version':1,'reader':'Custom iframe browser reader 1.0; unmodified XHTML and CSS extracted from delivered EPUB; native anchor navigation, no popup emulation','chromium':version,'runs':rows}
    if out:
        dump(out/'browser-audit.json',result)
        # Re-encode screenshots without ancillary metadata.
        for f in out.glob('*.png'):
            im=Image.open(f).convert('RGB'); im.save(f)
    return result
