# Compile solsrc/<subj>/*.txt (blocks: "=== id" / optional "a: ANS" / markdown) into site/sol/<subj>.json
import sys, os, re, json, glob
idx = {q['id']: q for q in json.load(open('site/index.json'))['q']}
for subj in sys.argv[1:]:
    out = {}
    for f in sorted(glob.glob(f'solsrc/{subj}/*.txt')):
        for blk in re.split(r'^=== ', open(f).read(), flags=re.M)[1:]:
            head, _, body = blk.partition('\n'); qid = head.strip()
            assert qid in idx, (f, qid)
            ent = {}
            while True:
                m = re.match(r'(a|fix):\s*(\S+)\s*\n', body)
                if not m: break
                ent[m.group(1)] = m.group(2); body = body[m.end():]
            ent['s'] = body.strip()
            out[qid] = ent
    json.dump(out, open(f'site/sol/{subj}.json', 'w'), ensure_ascii=False, separators=(',', ':'))
    total = sum(1 for q in idx if q.split('.')[0] == subj)
    print(f'subject {subj}: {len(out)}/{total} solutions')
