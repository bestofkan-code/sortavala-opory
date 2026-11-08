#!/usr/bin/env python3
"""Таблица «Контракт и выполнение» в шапке панели: опоры по типам, кронштейны по типам,
светильники — контракт / на карте / сделано / осталось.
Применяется к redaktor.html (один раз): python3 tools/patch_main_contract.py redaktor.html
"""
import sys

path = sys.argv[1]
s = open(path, encoding='utf-8').read()
if 'id="ktd"' in s:
    print('already applied')
    sys.exit(0)


def R(old, new, cnt=1):
    global s
    n = s.count(old)
    assert n == cnt, (old[:80], n)
    s = s.replace(old, new)


# 1) блок в шапке — сразу после склада закладных
R('Опорам на гравитационном фундаменте закладная не нужна.</small></details>',
  'Опорам на гравитационном фундаменте закладная не нужна.</small></details>'
  '<details id="ktd" open><summary><b>Контракт и выполнение</b><span id="kts"></span></summary>'
  '<table id="ktt"></table>'
  '<small id="ktn">На карте — опоры контракта без исключённых и опор на гравитационном фундаменте (следующий этап). '
  'Сделано — по отметкам работ «Установлена опора», «Установлена закладная», «Установлен кронштейн», «Установлен светильник»; закладная — по типу опоры (стандартная — ФМ-0,219, анкерная — ФМ-0,273). '
  'Красным — расхождение карты с контрактом.</small></details>', 1)

# 2) стили — по образцу склада закладных
R('#skn{display:block;opacity:.75;margin:2px 0 3px;line-height:1.3}</style>',
  '#skn{display:block;opacity:.75;margin:2px 0 3px;line-height:1.3}'
  '#ktd{margin:6px 0 4px;border:1px solid rgba(127,127,127,.4);border-radius:8px;padding:3px 8px}'
  '#ktd>summary{cursor:pointer;font-size:13px;list-style:none;display:flex;justify-content:space-between;align-items:center;gap:6px;padding:3px 0}'
  '#ktd>summary::-webkit-details-marker{display:none}#ktd>summary:after{content:\'▾\';opacity:.6}#ktd:not([open])>summary:after{content:\'▸\'}'
  '#kts{font-size:11.5px;opacity:.85;margin-left:auto;text-align:right}'
  '#ktt{width:100%;border-collapse:collapse;font-size:12px;margin:3px 0 2px}'
  '#ktt th,#ktt td{padding:3px 4px;text-align:right;border-bottom:1px solid rgba(127,127,127,.22);white-space:nowrap;font-variant-numeric:tabular-nums}'
  '#ktt th{font-weight:600;font-size:11px;opacity:.85}#ktt th:first-child,#ktt td:first-child{text-align:left;white-space:normal}'
  '#ktt td:first-child small{display:block;font-size:10px;opacity:.7;line-height:1.1}'
  '#ktt tr.kh td{font-size:10.5px;font-weight:600;letter-spacing:.06em;text-transform:uppercase;opacity:.75;padding-top:7px;border-bottom:0}'
  '#ktt tr.kt td{font-weight:700}'
  '#ktt .bad{color:#dc2626;font-weight:700}.dk #ktt .bad{color:#f87171}#ktt .ok{color:#15803d}.dk #ktt .ok{color:#4ade80}'
  '#ktn{display:block;opacity:.75;margin:2px 0 3px;line-height:1.3}</style>', 1)

# 3) пересчёт вместе со складом
R('try{skUI()}catch(e){}', 'try{skUI()}catch(e){}try{ktUI()}catch(e){}', 1)

# 4) код таблицы — рядом с кодом склада
R('/* ---- склад закладных: привезено − установлено по карте ---- */',
  r'''/* ---- контракт и выполнение: опоры, кронштейны, светильники ---- */
var KTC={op:[['Станд. 8 м','ОГС 0,4-8','S',8,397],['Анкер. 8 м','ОГС 0,7-8','A',8,183],['Станд. 9 м','ОГС 0,4-9','S',9,5],['Анкер. 9 м','ОГС 0,7-9','A',9,7]],
zk:[['Стандартная','ФМ-0,219','S',402],['Анкерная','ФМ-0,273','A',190]],
kr:[['1-рожковый',p=>(+p.kr||0)==1,353],['2-рожк. 90°',p=>(+p.kr||0)==2&&+p.ka==90,50],['2-рожк. 180°',p=>(+p.kr||0)==2&&+p.ka==180,189]],lum:831};
try{if(localStorage.getItem(KEY+'_kt')==='0')$('ktd').open=false}catch(e){}
$('ktd').addEventListener('toggle',()=>{try{localStorage.setItem(KEY+'_kt',$('ktd').open?'1':'0')}catch(e){}});
function ktUI(){const t=$('ktt');if(!t)return;const C=P.filter(p=>!p.x&&!isG(p)),cnt=f=>C.filter(f).length,
ty=p=>p.t=='A'?'A':'S',hh=p=>+p.h==9?9:8,lp=p=>(+p.kr||0)==2?2:(+p.kr||0)==1?1:0,
li=p=>wdone(p,6)?(+p.sv||Math.max(1,+p.kr||1)):0,sum=a=>a.reduce((x,y)=>x+y,0),
mc=(m,c)=>`<td class="${m==c?'ok':'bad'}" title="${m==c?'совпадает с контрактом':(m>c?'на карте больше на ':'на карте меньше на ')+Math.abs(m-c)}">${m}</td>`,
rw=(l,s,c,m,d,cl)=>`<tr${cl?' class="'+cl+'"':''}><td>${l}${s?'<small>'+s+'</small>':''}</td><td>${c}</td>${mc(m,c)}<td>${d}</td><td>${Math.max(0,c-d)}</td></tr>`,
kh=l=>`<tr class="kh"><td colspan="5">${l}</td></tr>`;
let h='<tr><th></th><th>Контракт</th><th>На карте</th><th>Сделано</th><th>Осталось</th></tr>'+kh('Опоры');
const O=KTC.op.map(([l,s,a,b,c])=>[l,s,c,cnt(p=>ty(p)==a&&hh(p)==b),cnt(p=>ty(p)==a&&hh(p)==b&&p.done)]);
O.forEach(o=>h+=rw(...o));const oc=sum(O.map(o=>o[2])),om=sum(O.map(o=>o[3])),od=sum(O.map(o=>o[4]));h+=rw('Всего опор','',oc,om,od,'kt');
h+=kh('Закладные');const Z=KTC.zk.map(([l,s,a,c])=>[l,s,c,cnt(p=>ty(p)==a),cnt(p=>ty(p)==a&&wdone(p,2))]);Z.forEach(z=>h+=rw(...z));h+=rw('Всего закладных','',sum(Z.map(z=>z[2])),sum(Z.map(z=>z[3])),sum(Z.map(z=>z[4])),'kt');
h+=kh('Кронштейны');const K=KTC.kr.map(([l,f,c])=>[l,'',c,cnt(f),cnt(p=>f(p)&&wdone(p,12))]);K.forEach(k=>h+=rw(...k));
const nk=cnt(p=>!(+p.kr)||((+p.kr)==2&&+p.ka!=90&&+p.ka!=180));if(nk)h+=`<tr><td>тип не указан</td><td>—</td><td class="bad">${nk}</td><td>${cnt(p=>wdone(p,12)&&(!(+p.kr)||((+p.kr)==2&&+p.ka!=90&&+p.ka!=180)))}</td><td>—</td></tr>`;
const kc=sum(K.map(k=>k[2])),km=sum(K.map(k=>k[3]))+nk,kd=cnt(p=>wdone(p,12));h+=rw('Всего кронштейнов','',kc,km,kd,'kt');
h+=kh('Светильники');const lm=sum(C.map(lp)),ld=sum(C.map(li));h+=rw('Светильники','',KTC.lum,lm,ld,'kt');
t.innerHTML=h;
$('kts').innerHTML=`оп. <b>${od}</b> · кр. <b>${kd}</b> · св. <b>${ld}</b>`;$('kts').title='Сделано: опор '+od+' из '+oc+', кронштейнов '+kd+' из '+kc+', светильников '+ld+' из '+KTC.lum}
/* ---- склад закладных: привезено − установлено по карте ---- */''', 1)

open(path, 'w', encoding='utf-8').write(s)
print('ok')
