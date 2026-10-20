import json, re, sys
subj = sys.argv[1]
idx = {q['id']: q for q in json.load(open('site/index.json'))['q']}
sol = json.load(open(f'site/sol/{subj}.json'))
bad = []
for qid, e in sol.items():
    q = idx[qid]; key = e.get('fix') or q['k'] or e.get('a', '')
    s = e['s']
    if re.fullmatch(r'[A-E]', key or ''):
        m = re.findall(r'\*\*[Oo]ption ([A-E])\*\*|[Oo]ption \*\*([A-E])\b|\*\*([A-E])\*\*\.?\s*$|answer is \*\*([A-E])\b|\*\*([A-E])\*\*', s)
        got = [x for t in m for x in t if x]
        if got and got[-1] != key: bad.append((qid, key, got[-1]))
        if not got: bad.append((qid, key, '?'))
    elif re.fullmatch(r'[A-E](;[A-E])+', key or ''):
        letters = set(key.split(';'))
        tail = s[-200:]
        found = set(re.findall(r'\b([A-E])\b', re.sub(r'\$.*?\$', '', tail)))
        if not letters <= found: bad.append((qid, key, ''.join(sorted(found))))
    elif re.match(r'^-?\d', key or ''):
        nums = key.replace(';', ':').split(':')
        if not any(n.strip() in s for n in nums): bad.append((qid, key, 'num?'))
print(len(bad)); [print(b) for b in bad]
