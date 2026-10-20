def ins(h,x,d=2):
    h.append(x); i=len(h)-1
    while i>0 and h[(i-1)//d]<h[i]: p=(i-1)//d; h[i],h[p]=h[p],h[i]; i=p
    return h
def delmax(h,d=2):
    h[0]=h[-1]; h.pop(); i=0
    while True:
        c=[d*i+k for k in range(1,d+1) if d*i+k<len(h)]
        if not c: break
        m=max(c,key=lambda j:h[j])
        if h[m]>h[i]: h[i],h[m]=h[m],h[i]; i=m
        else: break
    return h
def isheap(h,d=2): return all(h[(i-1)//d]>=h[i] for i in range(1,len(h)))
