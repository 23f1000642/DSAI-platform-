import re, json
txt = open('pyq.txt').read().split('\n')
toc = {}
for l in txt[:400]:
    m = re.match(r'^\s*(\d+(?:\.\d+)?) (.+?) \((\d+)\)\s+\d+\s*$', l)
    if m: toc[m.group(1)] = dict(name=m.group(2), n=int(m.group(3)))
keys = {}
inkey = False
for l in txt:
    if l.strip() == 'Answer Keys': inkey = True; continue
    if not inkey: continue
    if re.match(r'^\s*\d+\.\d+\.\d+ [A-Za-z].*[:|]', l): inkey = False; continue
    for m in re.finditer(r'(\d+\.\d+\.\d+)\s+(.+?)(?=\s{2,}\d+\.\d+\.\d+\s|\s*$)', l):
        keys[m.group(1)] = m.group(2).strip()
json.dump(dict(toc=toc, keys=keys), open('meta.json', 'w'), indent=0)
print(len(toc), 'toc entries;', len(keys), 'keys')
import collections
print(collections.Counter(re.sub(r'[0-9.\-]+', '#', v) for v in keys.values()).most_common(30))
