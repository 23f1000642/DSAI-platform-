import os, numpy as np
from PIL import Image
hits=[]
for f in sorted(os.listdir('img')):
    a=np.asarray(Image.open('img/'+f).convert('RGB')).astype(int)
    r,g,b=a[...,0],a[...,1],a[...,2]
    m=(r>170)&(g>130)&(b<110)&(r-b>90)
    n=int(m.sum())
    if n>30: hits.append((f[:-5],n))
print(len(hits)); print(hits[:40])
import collections; print(collections.Counter(h[0].split('.')[0] for h in hits))
