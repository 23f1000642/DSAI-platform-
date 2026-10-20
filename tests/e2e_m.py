import asyncio
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        m = await b.new_page(viewport={'width':390,'height':844}, color_scheme='dark')
        errs=[]; m.on('pageerror', lambda e: errs.append(str(e)))
        await m.goto('http://localhost:8765/_local.html'); await m.wait_for_selector('.subj')
        await m.screenshot(path='/tmp/claude-0/m1.png')
        await m.click('[data-s="3"]'); await m.check('#c3\\.2'); await m.check('#c3\\.3'); await m.click('#exam'); await m.wait_for_selector('.exam #exImg img')
        await m.screenshot(path='/tmp/claude-0/m2.png')
        await m.click('#palbtn'); await m.wait_for_timeout(400); await m.screenshot(path='/tmp/claude-0/m3.png')
        print('sw', await m.evaluate('document.documentElement.scrollWidth'), errs)
        await b.close()
asyncio.run(main())
