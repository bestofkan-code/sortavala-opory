import sys
FILES=['redaktor.html','prosmotr.html','montazh.html','zamechaniya.html','zamechaniya-prosmotr.html','uchastki.html']
R=[("function upd(p){const m=mk.get(p);","function upd(p){if(!p.g&&p.w&&p.w[11])p.g=true;const m=mk.get(p);"),
   ("function setW(p,k,on,d){if(k==10&&on)p.f='G';","function setW(p,k,on,d){if(k==10&&on)p.f='G';if(k==11&&on)p.g=true;")]
for f in FILES:
    s=open(f,encoding='utf-8').read()
    for a,b in R:
        if s.count(a)!=1: sys.exit(f+' '+a[:30])
        s=s.replace(a,b)
    open(f,'w',encoding='utf-8').write(s); print('ok',f)
