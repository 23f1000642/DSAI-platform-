# Pack question images into labelled contact sheets for reading. usage: sheets.py <subject>
import json, sys, os
from PIL import Image, ImageDraw, ImageFont
subj = sys.argv[1]; MAXH = 1450; W = 1040
d = json.load(open('site/index.json'))
qs = [q for q in d['q'] if q['id'].split('.')[0] == subj]
out = f'sheets/{subj}'; os.makedirs(out, exist_ok=True)
try: font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 22)
except: font = ImageFont.load_default()
sheets = []; cur = []; h = 0
def flush():
    global cur, h
    if not cur: return
    H = sum(im.height + 34 for _, im, _ in cur)
    S = Image.new('RGB', (W, H), 'white'); y = 0; dr = ImageDraw.Draw(S)
    for qid, im, lab in cur:
        dr.rectangle([0, y, W, y + 30], fill=(40, 60, 160)); dr.text((8, y + 3), lab, fill='white', font=font); y += 32
        S.paste(im, (0, y)); y += im.height + 2
    n = len(sheets) + 1; S.save(f'{out}/s{n:03d}.png'); sheets.append([c[0] for c in cur]); cur = []; h = 0
for q in qs:
    im = Image.open(f"img/{q['id']}.webp").convert('RGB')
    if im.width > W: im = im.resize((W, int(im.height * W / im.width)))
    lab = f"{q['id']}  [{q['t']}]  key={q['ks']}  {q['src']}"
    if h + im.height + 34 > MAXH and cur: flush()
    cur.append((q['id'], im, lab)); h += im.height + 34
flush()
json.dump(sheets, open(f'{out}/index.json', 'w'))
print(len(sheets), 'sheets for', len(qs), 'questions')
