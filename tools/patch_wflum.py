import sys,io
FILES=['redaktor.html','prosmotr.html','montazh.html','zamechaniya.html','zamechaniya-prosmotr.html','uchastki.html']
OLD1="const k=+c.dataset.f,n=B.filter(p=>{const v=wd(p,k);return(f||t)?(want?inr(v):!inr(v)):(!!v)==want}).length;let i=c.parentNode.querySelector('i');if(!i){i=document.createElement('i');c.parentNode.appendChild(i)}i.textContent=n});"
NEW1="const k=+c.dataset.f,M=B.filter(p=>{const v=wd(p,k);return(f||t)?(want?inr(v):!inr(v)):(!!v)==want}),n=M.length;let i=c.parentNode.querySelector('i');if(!i){i=document.createElement('i');c.parentNode.appendChild(i)}if(k==6){const L=M.reduce((a,p)=>a+lumN(p),0);i.textContent=L==n?n:L+' шт · '+n+' оп.';i.title='Светильников '+L+' шт. на '+n+' опорах (2-рожковый кронштейн = 2 светильника)'}else{i.textContent=n;i.title=''}});"
OLD2="+'</small><small>стандартных '+(V.length-a)+' · анкерных '+a+'</small>'}"
NEW2="+'</small><small>стандартных '+(V.length-a)+' · анкерных '+a+'</small>'+(s.map(Number).includes(6)?'<small>светильников '+V.filter(p=>!p.x&&!isG(p)&&!p.pp).reduce((q,p)=>q+lumN(p),0)+' шт (по кронштейнам)</small>':'')}"
FN="function lumI(p){"
FNNEW="function lumN(p){return +p.kr==2?2:+p.kr==1?1:Math.max(1,+p.sv||1)}\nfunction lumI(p){"
for f in FILES:
    s=open(f,encoding='utf-8').read()
    for o,nw in ((OLD1,NEW1),(OLD2,NEW2),(FN,FNNEW)):
        c=s.count(o)
        if c!=1: sys.exit(f'{f}: {o[:40]} count={c}')
        s=s.replace(o,nw)
    open(f,'w',encoding='utf-8').write(s); print('ok',f)
