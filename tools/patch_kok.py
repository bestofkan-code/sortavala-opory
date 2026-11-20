# Подсказки до сметы по кронштейнам: кнопка «Исключить» — тип кронштейна на опоре подобран правильно (поле poles.kok),
# опора больше не попадает в подсказки. Галочка «тип кронштейна подтверждён» в карточке опоры (снять — вернуть в подсказки).
import sys
p=sys.argv[1];s=open(p,encoding='utf-8').read()
def R(a,b,n=1):
    global s
    assert s.count(a)==n,(a[:90],s.count(a));s=s.replace(a,b)
R("vk:!!p.vk,rz:!!p.rz,h:+p.h||8,","vk:!!p.vk,rz:!!p.rz,kok:!!p.kok,h:+p.h||8,")
R("vk:!!r.vk,rz:!!r.rz,h:+r.h||8,","vk:!!r.vk,rz:!!r.rz,kok:!!r.kok,h:+r.h||8,")
# подсказки: исключённые не предлагать
R("C.forEach(p=>{const x=kcT(p);if(!ov.includes(x)||used.has(p.uid)||wdone(p,12))return;",
  "C.forEach(p=>{const x=kcT(p);if(!ov.includes(x)||used.has(p.uid)||wdone(p,12)||p.kok)return;")
# кнопка и счётчик
R("<button data-kca=\"${esc(x.p.uid)}\" data-to=\"${x.to}\" title=\"Сменить тип кронштейна на опоре\">Применить</button>`}",
  "<button data-kca=\"${esc(x.p.uid)}\" data-to=\"${x.to}\" title=\"Сменить тип кронштейна на опоре\">Применить</button><button data-kcx=\"${esc(x.p.uid)}\" title=\"Тип кронштейна на опоре подобран правильно — больше не предлагать\">Исключить</button>`}")
R("Проверьте на месте или по спутнику.</small>`+",
  "Проверьте на месте или по спутнику.</small>`+(()=>{const n=P.filter(p=>p.kok&&!p.x).length;return n?`<small style=\"display:block;opacity:.75\">Исключено из подсказок (тип подтверждён): <b>${n}</b> — вернуть можно в карточке опоры.</small>`:''})()+")
R("$('kcm').onclick=e=>{const a=e.target.closest('[data-kca]');",
  "$('kcm').onclick=e=>{{const x=e.target.closest('[data-kcx]');if(x){if(RO)return;const p=P.find(o=>o.uid==x.dataset.kcx);if(!p)return;p.kok=true;upd(p);save();stats();mark(p);try{kcSm()}catch(er){}toast(p.id+': тип кронштейна подтверждён, из подсказок исключена');return}}const a=e.target.closest('[data-kca]');")
# карточка опоры
R("<b style=\"color:#facc15\">разметка 2.1.3</b></label>",
  "<b style=\"color:#facc15\">разметка 2.1.3</b></label><label title=\"Тип кронштейна на опоре подобран правильно — не предлагать в подсказках до сметы\"><input type=checkbox data-kok ${p.kok?'checked':''}> <b style=\"color:#86efac\">тип кронштейна подтверждён</b></label>")
R("{const e=d.querySelector('[data-rz]');if(e)e.onchange=",
  "{const e=d.querySelector('[data-kok]');if(e)e.onchange=()=>{PSEL=Date.now();p.kok=e.checked;ch();upd(p);stats();try{kcSm()}catch(er){}toast(p.id+(p.kok?': тип кронштейна подтверждён':': опора снова в подсказках по кронштейнам'))}} {const e=d.querySelector('[data-rz]');if(e)e.onchange=")
open(p,'w',encoding='utf-8').write(s);print('ok kok',p)
