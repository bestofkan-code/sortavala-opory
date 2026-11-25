import sys
FILES=['redaktor.html','prosmotr.html','montazh.html','zamechaniya.html','zamechaniya-prosmotr.html','uchastki.html']
A="${(()=>{const A=Q.filter(p=>!p.x),c=(h,t)=>A.filter(p=>(+p.h||8)==h&&p.t==t)"
B="+(nn?`<br><small style=\"color:#15803d\">Добавлено новых: ${nn}</small>`:'');"
C="$('st').innerHTML="
for f in FILES:
    s=open(f,encoding='utf-8').read()
    if 'class="stx"' in s: print('skip',f); continue
    for x in (A,B,C):
        if s.count(x)!=1: sys.exit(f'{f}: {x[:40]} count {s.count(x)}')
    s=s.replace(A,'<details class="stx"${window.STX?\' open\':\'\'}><summary style="font-size:12px;color:#9aa3b5;cursor:pointer;margin:4px 0">Подробнее: высота опор, ТП, СИП, заземление, подвеска</summary>'+A)
    s=s.replace(B,B[:-1]+"+'</details>';")
    s=s.replace(C,"if(!window.STXL){window.STXL=1;try{window.STX=localStorage.getItem('stx_open')==='1'}catch(e){}$('st').addEventListener('toggle',e=>{if(e.target.classList&&e.target.classList.contains('stx')){window.STX=e.target.open;try{localStorage.setItem('stx_open',e.target.open?'1':'0')}catch(_){}}},true)}"+C,1)
    open(f,'w',encoding='utf-8').write(s); print('ok',f)
