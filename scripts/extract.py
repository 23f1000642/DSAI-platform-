import pymupdf, re, json, sys
d = pymupdf.open(sys.argv[1])
HDR = re.compile(r'^(\d+)\.(\d+)\.(\d+)$')
qs = []; cur = None
events = []  # (page, y0, y1, kind, data)
for pi in range(len(d)):
    p = d[pi]
    lines = []
    for b in p.get_text('dict')['blocks']:
        for l in b.get('lines', []):
            sp = [s for s in l['spans']]
            t = ''.join(s['text'] for s in sp).strip()
            if not t: continue
            lines.append((l['bbox'], t, sp[0]['font'], sp[0]['size']))
    lines.sort(key=lambda x: (round(x[0][1]), x[0][0]))
    for bb, t, f, s in lines:
        if 'Bold' in f and HDR.match(t) and abs(s - 9.75) < .3 and bb[0] < 60:
            events.append((pi, bb[1], bb[3], 'H', t))
        elif 'Bold' in f and bb[0] >= 65 and bb[0] < 120 and abs(s - 9.75) < .3:
            events.append((pi, bb[1], bb[3], 'T', t))
        elif 'Bold' in f and (re.match(r'^\d+(\.\d+)?$', t) or t.startswith('Answer Keys') or s > 10.5):
            events.append((pi, bb[1], bb[3], 'S', t))
        elif t.startswith('Answer key'):
            events.append((pi, bb[1], bb[3], 'A', t))
        elif 'Ubuntu' in f and s < 6:
            events.append((pi, bb[1], bb[3], 'G', t))
        else:
            events.append((pi, bb[1], bb[3], 'X', (t, bb[0])))
    if pi > 0 and pi % 100 == 0: print('page', pi, file=sys.stderr)
# images (QR codes) per page
qr = {}
for pi in range(len(d)):
    qr[pi] = [list(i['bbox']) for i in d[pi].get_image_info() if i['bbox'][0] > 480 and (i['bbox'][2]-i['bbox'][0]) < 50]
Hpos = {(e[0], round(e[1])) for e in events if e[3] == 'H'}
def nearH(pi, y): return any((pi, round(y) + d) in Hpos for d in range(-3, 4))
events = [e if e[3] != 'T' or nearH(e[0], e[1]) else (e[0], e[1], e[2], 'X', (e[4], 0)) for e in events]
events.sort(key=lambda e: (e[0], e[1], 0 if e[3] == 'H' else 1))
for e in events:
    pi, y0, y1, k, v = e
    if k == 'H':
        if cur:
            cur['end'] = cur['end'] or cur.get('tagpos', (pi, y0)); qs.append(cur)
        cur = dict(id=v, title='', start=(pi, y0), hb=(pi, y1), tags=[], end=None, text=[])
    elif cur is None: continue
    elif k == 'T' and not cur['title'] and pi == cur['start'][0] and abs(y0 - cur['start'][1]) < 3:
        cur['title'] = v
    elif k == 'G' and cur['end'] is None:
        cur['tags'].append(v); cur['tagpos'] = cur.get('tagpos', (pi, y0))
        if cur['title']: pass
    elif k == 'A' and cur['end'] is None:
        cur['end'] = cur.get('tagpos', (pi, y0))
        qs.append(cur); cur = None
    elif k in 'SH' or (k=='T' and cur['title']):
        cur['end'] = cur.get('tagpos', (pi, y0)); qs.append(cur); cur = None
    elif k == 'X' and cur['end'] is None and 'tagpos' not in cur:
        cur['text'].append(v[0])
if cur: qs.append(cur)
json.dump(dict(qs=qs, qr=qr), open(sys.argv[2], 'w'))
print(len(qs), 'questions;', sum(1 for q in qs if not q['title']), 'no title;', sum(1 for q in qs if not q['end']), 'no end')
