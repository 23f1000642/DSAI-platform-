def insb(t,x):
  if t is None: return [x,None,None]
  if x<t[0]: t[1]=insb(t[1],x)
  else: t[2]=insb(t[2],x)
  return t
def build(xs):
  t=None
  for x in xs: t=insb(t,x)
  return t
def pre(t): return [] if t is None else [t[0]]+pre(t[1])+pre(t[2])
def post(t): return [] if t is None else post(t[1])+post(t[2])+[t[0]]
def ino(t): return [] if t is None else ino(t[1])+[t[0]]+ino(t[2])
def h(t): return -1 if t is None else 1+max(h(t[1]),h(t[2]))
def show(t,d=0):
  if t is None: return ''
  return show(t[2],d+1)+'    '*d+str(t[0])+'\n'+show(t[1],d+1)
