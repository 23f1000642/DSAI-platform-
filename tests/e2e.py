import asyncio
from playwright.async_api import async_playwright
OUT='/tmp/claude-0/'
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page(viewport={'width':1280,'height':900})
        errs=[]; pg.on('console', lambda m: errs.append(m.text) if m.type=='error' else None); pg.on('pageerror', lambda e: errs.append(str(e)))
        await pg.goto('http://localhost:8765/_local.html'); await pg.wait_for_selector('.subj')
        await pg.screenshot(path=OUT+'s1_home.png')
        await pg.click('[data-s="1"]'); await pg.wait_for_selector('#subs')
        await pg.check('#c1\\.2'); await pg.check('#c1\\.42')
        await pg.screenshot(path=OUT+'s2_subject.png')
        await pg.click('#prac'); await pg.wait_for_selector('#qimg img')
        await pg.screenshot(path=OUT+'s3a_desc.png', full_page=True)
        await pg.click('#next'); await pg.wait_for_selector('#qimg img'); await pg.click('#next'); await pg.wait_for_selector('.opt')
        await pg.click('.opt[data-o="A"]'); await pg.wait_for_selector('.verdict')
        await pg.click('#reveal'); await pg.wait_for_timeout(500)
        await pg.screenshot(path=OUT+'s3_practice.png', full_page=True)
        await pg.click('[data-s]') if False else None
        await pg.click('.crumbs button:nth-of-type(2)'); await pg.wait_for_selector('#subs')
        await pg.fill('#cnt','5'); await pg.dispatch_event('#cnt','change')
        await pg.click('#exam'); await pg.wait_for_selector('.exam #exImg img')
        for i in range(5):
            if await pg.query_selector('.exopts input[type=radio]'):
                await pg.check('.exopts input[type=radio] >> nth=1')
            elif await pg.query_selector('.exopts input[type=checkbox]'):
                await pg.check('.exopts input[type=checkbox] >> nth=0')
            else:
                await pg.fill('#exnat','3')
            await pg.click('#mark' if i==2 else '#save'); await pg.wait_for_timeout(150)
        await pg.screenshot(path=OUT+'s4_exam.png')
        await pg.click('#submit'); await pg.click('#yes'); await pg.wait_for_selector('.score')
        await pg.click('[data-j="0"]'); await pg.wait_for_timeout(600)
        await pg.screenshot(path=OUT+'s5_result.png', full_page=True)
        m = await b.new_page(viewport={'width':390,'height':844}, color_scheme='dark')
        await m.goto('http://localhost:8765/_local.html'); await m.wait_for_selector('.subj')
        await m.click('[data-s="3"]'); await m.check('#c3\\.1'); await m.click('#exam'); await m.wait_for_selector('.exam #exImg img')
        await m.screenshot(path=OUT+'s6_mobile_exam.png')
        sw = await m.evaluate('document.documentElement.scrollWidth'); print('mobile scrollWidth', sw)
        print('errors', errs)
        await b.close()
asyncio.run(main())
