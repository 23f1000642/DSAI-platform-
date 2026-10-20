import itertools, re
def closure(attrs, fds):
    c=set(attrs); ch=True
    while ch:
        ch=False
        for l,r in fds:
            if set(l)<=c and not set(r)<=c: c|=set(r); ch=True
    return c
def parse_fds(s):
    out=[]
    for part in s.split(','):
        l,r=part.split('->'); out.append((l.strip(),r.strip()))
    return out
def keys(R, fds):
    R=set(R); ks=[]
    for n in range(1,len(R)+1):
        for comb in itertools.combinations(sorted(R),n):
            if any(set(k)<=set(comb) for k in ks): continue
            if closure(comb,fds)>=R: ks.append(''.join(comb))
    return ks
def parse_sched(s):
    return [(m.group(1),m.group(2),m.group(3)) for m in re.finditer(r'([rw])(\d+)\(?(\w)\)?', s)]
def precedence(ops):
    E=set()
    for i,(a,t1,x1) in enumerate(ops):
        for b,t2,x2 in ops[i+1:]:
            if t1!=t2 and x1==x2 and 'w' in (a,b): E.add((t1,t2))
    return E
def acyclic(E):
    nodes={u for e in E for u in e}; 
    import collections
    indeg=collections.Counter(v for u,v in E); q=[n for n in nodes if indeg[n]==0]; seen=0; order=[]
    while q:
        n=q.pop(); seen+=1; order.append(n)
        for u,v in E:
            if u==n:
                indeg[v]-=1
                if indeg[v]==0: q.append(v)
    return seen==len(nodes), order
def cs(s):
    ops=parse_sched(s); E=precedence(ops); return acyclic(E), sorted(E)
