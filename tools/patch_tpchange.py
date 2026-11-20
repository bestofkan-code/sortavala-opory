# Смена ТП опоры прямо в карточке: выпадающий список «ТП» в заголовке карточки (редактор).
# Номер сохраняется, если свободен в новой ТП, иначе — следующий свободный. Линии перерисовываются:
# пролёты к опорам той же ТП — цветом новой ТП, к опорам другой ТП — серые «между ТП».
import sys
p=sys.argv[1];s=open(p,encoding='utf-8').read()
def R(a,b,n=1):
    global s
    assert s.count(a)==n,(a[:90],s.count(a));s=s.replace(a,b)
R("d.innerHTML=`<div><b>${esc(p.id)}</b> <small data-hs></small>",
  "d.innerHTML=`<div><b data-pid>${esc(p.id)}</b> <select data-tpsel title=\"Принадлежность к ТП — выберите другую, чтобы перенести опору\" style=\"width:auto;display:inline-block;padding:1px 4px;font-size:12px;margin:0 4px;border-left:4px solid ${tpCol(p.tp)}\">${tpList().map(t=>`<option value=\"${esc(t)}\" ${String(p.tp||'')==t?'selected':''}>${esc(tpn(t))}</option>`).join('')}</select> <small data-hs></small>")
R("if(k=='js'||k=='x'||k=='sx'||k=='pp'||(k=='tp'&&p.vk))lines();","if(k=='js'||k=='x'||k=='sx'||k=='pp'||k=='tp'||k=='n')lines();")
R("{const e=d.querySelector('[data-rz]');",
  "{const e=d.querySelector('[data-tpsel]');if(e)e.onchange=()=>{const t=e.value,o=String(p.tp||''),oid=p.id;if(t==o)return;const used=new Set(P.filter(q=>q!==p&&String(q.tp||'')==t).map(q=>+q.n));let n=+p.n;const busy=!n||used.has(n);if(busy)n=Math.max(0,...used)+1;"
  "if(!confirm('Перенести опору '+oid+' в '+tpn(t)+'?\\nНовый номер: '+pid(t,n)+(busy?' (номер '+(p.n||'—')+' в '+tpn(t)+' занят — взят следующий свободный)':'')))return void(e.value=o);"
  "PSEL=Date.now();p.tp=t;p.n=n;p.id=pid(t,n);const b=d.querySelector('[data-pid]');if(b)b.textContent=p.id;e.style.borderLeftColor=tpCol(t);const it=d.querySelector('[data-k=tp]');if(it)it.value=t;const nn=d.querySelector('[data-k=n]');if(nn)nn.value=n;ch();lines();try{numLabels()}catch(x){}toast(oid+' → '+p.id+': опора перенесена в '+tpn(t))}} {const e=d.querySelector('[data-rz]');")
open(p,'w',encoding='utf-8').write(s);print('ok tpchange',p)
