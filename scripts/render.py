import pymupdf, json, sys, os, io
from PIL import Image, ImageOps, ImageChops
d = pymupdf.open('pyq_clean.pdf'); R = json.load(open('raw.json'))
DPI = 144; S = DPI / 72; X0, X1 = 45, 560; TOP, BOT = 38, 812
os.makedirs('img', exist_ok=True)
qrs = {int(k): [b for b in v if b[2]-b[0] > 30 and b[3]-b[1] > 30] for k, v in R['qr'].items()}
def seg(pi, y0, y1):
    if y1 - y0 < 4: return None
    pix = d[pi].get_pixmap(dpi=DPI, clip=pymupdf.Rect(X0, y0, X1, y1))
    im = Image.frombytes('RGB', (pix.width, pix.height), pix.samples)
    for b in qrs.get(pi, []):
        if b[3] > y0 and b[1] < y1:
            im.paste((255, 255, 255), (int((b[0]-X0)*S)-2, max(0, int((b[1]-y0)*S)-2), int((b[2]-X0)*S)+3, int((b[3]-y0)*S)+3))
    import numpy as np
    from PIL import ImageFilter
    arr = np.asarray(im).astype(int); r, g, bl = arr[..., 0], arr[..., 1], arr[..., 2]
    ym = (r > 150) & (g > 110) & (bl < 160) & (r - bl > 50)
    if ym.sum() > 30:
        dil = np.asarray(Image.fromarray((ym * 255).astype('uint8')).filter(ImageFilter.MaxFilter(5))) > 0
        light = (np.minimum(r, g) > 140)
        kill = (ym | (dil & light))
        arr2 = arr.copy(); arr2[kill] = 255
        # darken remaining tinted text pixels to neutral grey so no yellow cast remains
        tint = dil & ~kill
        lum = (0.3 * r + 0.59 * g + 0.11 * bl).astype(int)
        for c in range(3): arr2[..., c][tint] = lum[tint]
        im.paste(Image.fromarray(arr2.astype('uint8')))
    bb = ImageOps.invert(im.convert('L')).point(lambda v: 255 if v > 25 else 0).getbbox()
    if not bb: return None
    return im.crop((0, max(0, bb[1]-6), min(im.width, bb[2]+12), min(im.height, bb[3]+8)))
only = set(sys.argv[1:])
for q in R['qs']:
    if only and q['id'] not in only: continue
    (sp, sy), (ep, ey) = q['hb'], q['end']
    parts = []
    for pi in range(sp, ep + 1):
        a = sy + 3 if pi == sp else TOP
        b = ey - 1 if pi == ep else BOT
        s = seg(pi, a, b)
        if s: parts.append(s)
    if not parts: print('EMPTY', q['id']); continue
    H = sum(p.height for p in parts) + 10 * (len(parts) - 1)
    out = Image.new('RGB', (max(p.width for p in parts), H), 'white'); y = 0
    for p in parts: out.paste(p, (0, y)); y += p.height + 10
    out.save(f"img/{q['id']}.webp", 'WEBP', quality=72, method=6)
