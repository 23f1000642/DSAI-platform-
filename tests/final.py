import asyncio, json
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page(viewport={'width':1200,'height':900})
        errs=[]; pg.on('pageerror', lambda e: errs.append(str(e)))
        await pg.goto('http://localhost:8765/_local.html'); await pg.wait_for_selector('.subj')
        n = await pg.eval_on_selector_all('.subj','e=>e.length'); print('subjects',n)
        # practice in every subject: open first subtopic, reveal solution
        for s in range(1,16):
            await pg.goto('http://localhost:8765/_local.html'); await pg.wait_for_selector('.subj')
            await pg.click(f'[data-s="{s}"]'); await pg.wait_for_selector('#subs')
            await pg.click('#none'); await pg.check('#subs input >> nth=0')
            await pg.click('#prac'); await pg.wait_for_selector('#reveal')
            await pg.click('#reveal'); await pg.wait_for_selector('.sol .body')
            t = await pg.inner_text('.sol .body'); print(s, 'sol chars', len(t), 'missing' if 'still being written' in t else 'ok')
        # exam in DBMS
        await pg.goto('http://localhost:8765/_local.html'); await pg.wait_for_selector('.subj')
        await pg.click('[data-s="3"]'); await pg.click('#all'); await pg.fill('#cnt','10'); await pg.dispatch_event('#cnt','change')
        await pg.click('#exam'); await pg.wait_for_selector('.exam #exImg img')
        for i in range(10):
            if await pg.query_selector('.exopts input[type=radio]'): await pg.check('.exopts input[type=radio] >> nth=0')
            elif await pg.query_selector('.exopts input[type=checkbox]'): await pg.check('.exopts input[type=checkbox] >> nth=0')
            else: await pg.fill('#exnat','1')
            await pg.click('#save'); await pg.wait_for_timeout(100)
        await pg.click('#submit'); await pg.click('#yes'); await pg.wait_for_selector('.score')
        print('score', await pg.inner_text('.score'))
        await pg.click('[data-j="0"]'); await pg.wait_for_selector('#revq .sol .body')
        print('errors', errs)
        await b.close()
asyncio.run(main())
