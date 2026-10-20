import asyncio
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page(viewport={'width':1200,'height':900})
        errs=[]; pg.on('pageerror', lambda e: errs.append(str(e)))
        await pg.goto('http://localhost:8765/_local.html'); await pg.wait_for_selector('.subj')
        await pg.click('[data-s="1"]'); await pg.click('#none'); await pg.check('#c1\\.42'); await pg.click('#prac'); await pg.wait_for_selector('.opt, #reveal')
        for i in range(3): await pg.click('#next'); await pg.wait_for_timeout(200)
        if await pg.query_selector('.opt'): await pg.click('.opt >> nth=0')
        await pg.click('#reveal'); await pg.wait_for_selector('.sol .body'); await pg.wait_for_timeout(400)
        await pg.screenshot(path='/tmp/claude-0/sol.png', full_page=True)
        t = await pg.inner_text('.sol'); print(t[:300]); print('errs', errs)
        await b.close()
asyncio.run(main())
