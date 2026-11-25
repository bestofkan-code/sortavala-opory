import sys
FILES=['redaktor.html','prosmotr.html','montazh.html','zamechaniya.html','zamechaniya-prosmotr.html','uchastki.html']
R=[("r=ks.map(k=>{const v=wd(p,k);return(f||e)?(want?inr(v):!inr(v)):(!!v)==want});",
    "r=ks.map(k=>{const v=wd(p,k);if(k==11&&!want&&s.length&&!p.g)return false;return(f||e)?(want?inr(v):!inr(v)):(!!v)==want});"),
   ("const k=+c.dataset.f,M=B.filter(p=>{const v=wd(p,k);return",
    "const k=+c.dataset.f,M=B.filter(p=>{const v=wd(p,k);if(k==11&&!want&&!p.g)return false;return")]
for f in FILES:
    s=open(f,encoding='utf-8').read()
    for a,b in R:
        if s.count(a)!=1: sys.exit(f+' '+a[:40])
        s=s.replace(a,b)
    open(f,'w',encoding='utf-8').write(s); print('ok',f)
