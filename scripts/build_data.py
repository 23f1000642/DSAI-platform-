import json, re, os, base64, collections
R = json.load(open('raw.json')); M = json.load(open('meta.json'))
toc, keys = M['toc'], M['keys']
out = 'site'; os.makedirs(f'{out}/q', exist_ok=True)
subjects = []
for sid in sorted([k for k in toc if '.' not in k], key=int):
    subjects.append(dict(id=sid, name=toc[sid]['name'], subs=[]))
smap = {s['id']: s for s in subjects}
qmeta = []; bysub = collections.defaultdict(list)
for q in R['qs']:
    qid = q['id']; a, b, c = qid.split('.'); sub = f'{a}.{b}'
    tags = ' '.join(q['tags']).split()
    title = q['title']
    src = title.split(': ', 1)[1] if (': ' in title and '|' not in title.split(': ', 1)[0]) else title
    k = keys.get(qid, 'TBA')
    text = q['text']
    opts = set()
    for t in text:
        m = re.match(r'^\(?([A-E])[.)]\s', t + ' ')
        if m: opts.add(m.group(1))
    if re.fullmatch(r'[A-E](;[A-E])*', k):
        typ = 'MSQ' if (';' in k or 'multiple-selects' in tags) else 'MCQ'
    elif k in ('True', 'False'): typ = 'TF'
    elif re.match(r'^-?\d', k): typ = 'NAT'
    else:
        if 'multiple-selects' in tags: typ = 'MSQ'
        elif len(opts) >= 3: typ = 'MCQ'
        elif 'numerical-answers' in tags or 'fill-in-the-blanks' in tags: typ = 'NAT'
        elif 'descriptive' in tags: typ = 'DESC'
        else: typ = 'DESC'
    nopt = 5 if ('E' in opts or 'E' in k) else 4
    exam = 'GATE' if 'GATE' in src else ('UGC NET' if 'UGC NET' in src else 'Other')
    ym = re.search(r'(19|20)\d\d', src)
    diff = next((t for t in tags if t in ('easy', 'normal', 'difficult', 'hard')), '')
    marks = 2 if ('two-marks' in tags or exam == 'UGC NET') else 1
    qm = dict(id=qid, sub=sub, src=src, t=typ, k=k if k not in ('TBA', 'N/A', 'X') else '', ks=k, n=nopt,
              m=marks, ex=exam, y=int(ym.group(0)) if ym else 0, d=diff,
              tg=[t for t in tags if not re.search(r'\d{4}|marks?$|^(easy|normal|difficult)$', t)][:6])
    qmeta.append(qm); bysub[sub].append(qid)
for sub, ids in bysub.items():
    s = smap[sub.split('.')[0]]
    name = toc.get(sub, {}).get('name') or ('General / Miscellaneous' if sub.endswith('.0') else sub)
    s['subs'].append(dict(id=sub, name=name, n=len(ids)))
    if os.environ.get('SKIPIMG'): continue
    data = {i: base64.b64encode(open(f'img/{i}.webp', 'rb').read()).decode() for i in ids}
    json.dump(data, open(f'{out}/q/{sub}.json', 'w'), separators=(',', ':'))
for s in subjects: s['subs'].sort(key=lambda x: int(x['id'].split('.')[1]))
json.dump(dict(subjects=subjects, q=qmeta), open(f'{out}/index.json', 'w'), separators=(',', ':'))
print(collections.Counter(q['t'] for q in qmeta)); print(collections.Counter(q['ks'] for q in qmeta if not q['k']))
print(len(bysub), 'subtopic files;', sum(1 for q in qmeta if not q['k']), 'without key')
