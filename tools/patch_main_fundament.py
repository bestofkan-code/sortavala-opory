#!/usr/bin/env python3
"""Блок «Проверка котлованов, закладных и бетона» под «Проверкой кронштейнов»:
по каждой ТП — котлованы / закладные / бетон (сделано из всего), «можно ставить закладную»
(котлован есть, закладной нет), «можно бетонировать» (закладная есть, бетона нет), опоры с замечаниями;
список замечаний (нажать — карта покажет опору); выгрузка «Таблица проверки» в Excel.
Применяется к redaktor.html (один раз, после patch_main_brackets.py): python3 tools/patch_main_fundament.py redaktor.html
"""
import sys

path = sys.argv[1]
s = open(path, encoding='utf-8').read()
if 'id="fdd"' in s:
    print('already applied')
    sys.exit(0)


def R(old, new, cnt=1):
    global s
    n = s.count(old)
    assert n == cnt, (old[:80], n)
    s = s.replace(old, new)


# 1) блок — сразу после «Проверки кронштейнов»
R('<button id="kcx">Таблица проверки (Excel)</button></div></details>',
  '<button id="kcx">Таблица проверки (Excel)</button></div></details>'
  '<details id="fdd"><summary><b>Проверка котлованов, закладных, бетона</b><span id="fds"></span></summary>'
  '<small id="fdn">Цифры — сделано / всего. «→закл.» — котлован забурен, закладной ещё нет. '
  '«→бет.» — закладная стоит, ещё не забетонирована. «⚠» — опор с замечаниями. '
  'Опоры на гравитационном фундаменте и исключённые не считаются. Нажмите на опору в списке — карта покажет её.</small>'
  '<table id="fdt"></table><div id="fdl"></div>'
  '<div class="r"><button id="fdx">Таблица проверки (Excel)</button></div></details>', 1)

# 2) стили — как у «Проверки кронштейнов»
R('.kcg button{padding:2px 6px;font-size:11.5px;border-radius:9px}',
  '.kcg button{padding:2px 6px;font-size:11.5px;border-radius:9px}'
  '#fdd{margin:6px 0 4px;border:1px solid rgba(127,127,127,.4);border-radius:8px;padding:3px 8px}'
  '#fdd>summary{cursor:pointer;font-size:13px;list-style:none;display:flex;justify-content:space-between;align-items:center;gap:6px;padding:3px 0}'
  '#fdd>summary::-webkit-details-marker{display:none}#fdd>summary:after{content:\'▾\';opacity:.6}#fdd:not([open])>summary:after{content:\'▸\'}'
  '#fds{font-size:11.5px;opacity:.9;margin-left:auto;text-align:right}'
  '#fdt{width:100%;border-collapse:collapse;font-size:12px;margin:3px 0 2px}'
  '#fdt th,#fdt td{padding:3px 4px;text-align:right;border-bottom:1px solid rgba(127,127,127,.22);white-space:nowrap;font-variant-numeric:tabular-nums}'
  '#fdt th{font-weight:600;font-size:11px;opacity:.85}#fdt th:first-child,#fdt td:first-child{text-align:left;white-space:normal}'
  '#fdt td small{opacity:.6;font-size:10.5px}#fdt td.z{opacity:.4}#fdt tr.kt td{font-weight:700}'
  '#fdd .bad{color:#dc2626;font-weight:700}.dk #fdd .bad{color:#f87171}#fdd .ok{color:#15803d}.dk #fdd .ok{color:#4ade80}'
  '#fdn{display:block;opacity:.75;margin:2px 0 3px;line-height:1.3}', 1)

# 3) пересчёт вместе с остальными
R('try{kcUI()}catch(e){}', 'try{kcUI()}catch(e){}try{fdUI()}catch(e){}', 1)

# 4) код — сразу после «Проверки кронштейнов»
R("$('kcx').onclick=()=>{try{kcXl()}catch(e){alert('Ошибка выгрузки: '+(e.message||e))}};",
  r"""$('kcx').onclick=()=>{try{kcXl()}catch(e){alert('Ошибка выгрузки: '+(e.message||e))}};
/* ---- проверка котлованов, закладных, бетона: по ТП, замечания по опорам, Excel ---- */
try{if(localStorage.getItem(KEY+'_fd')==='1')$('fdd').open=true}catch(e){}
$('fdd').addEventListener('toggle',()=>{try{localStorage.setItem(KEY+'_fd',$('fdd').open?'1':'0')}catch(e){}});
var FDG=[['zk','Закладная отмечена, а котлован нет'],['bz','Забетонирована, а закладная не отмечена'],['oz','Опора установлена, а закладная не отмечена'],['ob','Опора установлена, а бетон не отмечен'],
 ['d1','Даты не по порядку: закладная раньше котлована'],['d2','Даты не по порядку: бетон раньше закладной'],['d3','Даты не по порядку: опора раньше бетона'],
 ['gz','Закладная или бетон на гравитационном фундаменте'],['ex','Работы по фундаменту отмечены на исключённой опоре']];
const fdD=v=>/^\d{4}-\d\d-\d\d/.test(v)?v.slice(0,10):'',fdZn=p=>p.t=='A'?'под анкерную (СФГ-700)':'под стандартную (СФГ-400)';
function fdIss(p){const r=[],w1=wdone(p,1),w2=wdone(p,2),w3=wdone(p,3),d1=fdD(wd(p,1)),d2=fdD(wd(p,2)),d3=fdD(wd(p,3)),d4=fdD(wd(p,4)),rd=v=>v.slice(8,10)+'.'+v.slice(5,7);
 if(p.x){if(w1||w2||w3)r.push(['ex','отмечено: '+[w1&&'котлован',w2&&'закладная',w3&&'бетон'].filter(Boolean).join(', ')+', а опора исключена']);return r}
 if(isG(p)){if(w2||w3)r.push(['gz','отмечено: '+[w2&&'закладная',w3&&'бетон'].filter(Boolean).join(', ')+', а опора на гравитационном фундаменте']);return r}
 if(w2&&!w1)r.push(['zk','закладная отмечена, а котлован нет']);
 if(w3&&!w2)r.push(['bz','забетонирована, а закладная не отмечена']);
 if(p.done&&!w2)r.push(['oz','опора установлена, а закладная не отмечена']);
 if(p.done&&!w3)r.push(['ob','опора установлена, а бетон не отмечен']);
 if(d1&&d2&&d2<d1)r.push(['d1','закладная '+rd(d2)+', котлован '+rd(d1)]);
 if(d2&&d3&&d3<d2)r.push(['d2','бетон '+rd(d3)+', закладная '+rd(d2)]);
 if(d3&&d4&&d4<d3)r.push(['d3','опора '+rd(d4)+', бетон '+rd(d3)]);
 return r}
function fdData(){const C=P.filter(p=>!p.x&&!isG(p)),G=new Map();
 C.forEach(p=>{const k=String(p.tp||'—');if(!G.has(k))G.set(k,[]);G.get(k).push(p)});
 const I=[];P.forEach(p=>fdIss(p).forEach(([c,m])=>I.push({p,c,m})));
 const st=a=>{const o={n:a.length,k:0,z:0,b:0,o:0,zS:0,zA:0,nS:0,nA:0,cz:0,cb:0,iss:0};
  a.forEach(p=>{const w1=wdone(p,1),w2=wdone(p,2),w3=wdone(p,3);if(w1)o.k++;if(w2)o.z++;if(w3)o.b++;if(p.done)o.o++;
   if(p.t=='A'){o.nA++;if(w2)o.zA++}else{o.nS++;if(w2)o.zS++}if(w1&&!w2)o.cz++;if(w2&&!w3)o.cb++;if(fdIss(p).length)o.iss++});return o};
 const T=[...G.keys()].sort(kcRu).map(k=>({k,a:G.get(k),s:st(G.get(k))}));
 return{C,T,S:st(C),I}}
function fdUI(){const t=$('fdt');if(!t)return;const D=fdData(),I=D.I;
 const c=(d,n,tt)=>n?`<td title="${tt} ${d} из ${n}">${d}<small>/${n}</small></td>`:'<td class="z">—</td>';
 const row=(nm,o,cls)=>`<tr${cls?' class="'+cls+'"':''}><td>${nm}</td>${c(o.k,o.n,'котлованов забурено')}${c(o.z,o.n,'закладных установлено')}${c(o.b,o.n,'забетонировано')}<td title="котлован забурен, закладной нет">${o.cz||'—'}</td><td title="закладная стоит, бетона нет">${o.cb||'—'}</td><td class="${o.iss?'bad':'ok'}">${o.iss||'✓'}</td></tr>`;
 let h='<tr><th>ТП</th><th title="котлованов забурено / всего">котл.</th><th title="закладных установлено / всего">закл.</th><th title="забетонировано / всего">бет.</th><th title="котлован забурен, закладной ещё нет — можно ставить закладную">→закл.</th><th title="закладная стоит — можно бетонировать">→бет.</th><th title="опор с замечаниями">⚠</th></tr>';
 D.T.forEach(r=>h+=row(esc(tpn(r.k)),r.s));h+=row('Всего',D.S,'kt');t.innerHTML=h;
 let l='';FDG.forEach(([g,nm])=>{const a=I.filter(x=>x.c==g).sort((x,y)=>kcRu(x.p.id,y.p.id));if(!a.length)return;
  l+=`<div class="kcg"><b>${nm} — ${a.length}</b><div>${a.map(x=>`<button data-fd="${esc(x.p.uid)}" title="${esc(x.m)}">${esc(x.p.id)}</button>`).join('')}</div></div>`});
 $('fdl').innerHTML=l||'<small class="ok">Замечаний нет</small>';
 const n=new Set(I.map(x=>x.p.uid)).size,S=D.S;$('fds').innerHTML=`котл. <b>${S.k}</b> · закл. <b>${S.z}</b> · бет. <b>${S.b}</b> · `+(n?`<b class="bad">⚠ ${n}</b>`:'<b class="ok">✓</b>');
 $('fds').title='Из '+S.n+' опор: котлованов '+S.k+', закладных '+S.z+', забетонировано '+S.b+(n?', опор с замечаниями '+n:', замечаний нет')}
$('fdl').onclick=e=>{const b=e.target.closest('[data-fd]');if(!b)return;const p=P.find(o=>o.uid==b.dataset.fd);if(!p)return;
 map.setView([p.lat,p.lon],Math.max(map.getZoom(),19));const m=mk.get(p);if(m&&lg.hasLayer(m))L.popup(PO()).setLatLng(m.getLatLng()).setContent(popup(p)).openOn(map);else toast('Опора скрыта фильтром')};
function fdXl(){const D=fdData(),wb=XLSX.utils.book_new(),dt=v=>/^\d{4}-\d\d-\d\d/.test(v)?v.slice(8,10)+'.'+v.slice(5,7)+'.'+v.slice(0,4):(v?'да':''),K=592,KS=402,KA=190;
 const h1=['ТП','Опор','Котлованов забурено','Котлованов осталось','Закладных под станд. всего','Закладных под станд. установлено','Закладных под анкер. всего','Закладных под анкер. установлено','Закладных установлено','Закладных осталось','Забетонировано','Бетон осталось','Можно ставить закладную (котлован есть)','Можно бетонировать (закладная есть)','Опор установлено','Опор с замечаниями'];
 const r1=(nm,o)=>[nm,o.n,o.k,o.n-o.k,o.nS,o.zS,o.nA,o.zA,o.z,o.n-o.z,o.b,o.n-o.b,o.cz,o.cb,o.o,o.iss];
 const S=D.S,A1=[['Проверка котлованов, закладных и бетона по ТП — '+dt(LD())],[],h1,...D.T.map(r=>r1(tpn(r.k),r.s)),r1('Всего на карте',S),
  ['По контракту',K,'',K-S.k,KS,'',KA,'','',K-S.z,'',K-S.b,'','','',''],
  ['Разница карта − контракт',S.n-K,'','',S.nS-KS,'',S.nA-KA,'','','','','','','','',''],[],
  ['На карте — опоры контракта без исключённых и опор на гравитационном фундаменте (следующий этап). «Котлованов осталось» в строке «По контракту» — до 592.'],
  ['Сделано — по отметкам «Забурен котлован», «Установлена закладная», «Забетонирована», «Установлена опора». Закладная под стандартную опору — ЗФ-24/8 (СФГ-400), под анкерную — ЗФ-30/8 (СФГ-700).']];
 const w1=XLSX.utils.aoa_to_sheet(A1);w1['!cols']=[{wch:22},...h1.slice(1).map(()=>({wch:12}))];XLSX.utils.book_append_sheet(wb,w1,'По ТП');
 const h2=['№','Опора','ТП','Тип опоры','Закладная','Котлован','Закладная установлена','Забетонирована','Опора установлена','Следующий шаг','Замечание по карте','Проверено на месте (✓)','Примечание'];
 const nx=p=>p.x?'исключена':isG(p)?'гравит. фундамент':!wdone(p,1)?'бурить котлован':!wdone(p,2)?'ставить закладную':!wdone(p,3)?'бетонировать':!p.done?'ставить опору':'опора стоит';
 const pl=P.filter(p=>(!p.x&&!isG(p))||fdIss(p).length).sort((a,b)=>kcRu(a.tp,b.tp)||kcRu(a.id,b.id));
 const A2=[h2,...pl.map((p,i)=>[i+1,p.id,tpn(String(p.tp||'')),(p.t=='A'?'анкерная':'стандартная')+(p.pp?' (серая, предлагаемая)':''),p.x||isG(p)?'—':fdZn(p),dt(wd(p,1)),dt(wd(p,2)),dt(wd(p,3)),dt(wd(p,4)),nx(p),fdIss(p).map(x=>x[1]).join('; '),'',''])];
 const w2=XLSX.utils.aoa_to_sheet(A2);w2['!cols']=[{wch:5},{wch:18},{wch:14},{wch:26},{wch:26},{wch:12},{wch:12},{wch:12},{wch:12},{wch:18},{wch:48},{wch:12},{wch:24}];
 w2['!autofilter']={ref:'A1:M'+A2.length};XLSX.utils.book_append_sheet(wb,w2,'По опорам');
 const A3=[['Замечание','Опора','ТП','Подробно'],...FDG.flatMap(([g,nm])=>D.I.filter(x=>x.c==g).sort((x,y)=>kcRu(x.p.id,y.p.id)).map(x=>[nm,x.p.id,tpn(String(x.p.tp||'')),x.m]))];
 if(A3.length==1)A3.push(['Замечаний нет']);const w3=XLSX.utils.aoa_to_sheet(A3);w3['!cols']=[{wch:50},{wch:18},{wch:14},{wch:50}];XLSX.utils.book_append_sheet(wb,w3,'Замечания');
 XLSX.writeFile(wb,'Проверка_котлованов_закладных_бетона_'+LD()+'.xlsx')}
$('fdx').onclick=()=>{try{fdXl()}catch(e){alert('Ошибка выгрузки: '+(e.message||e))}};""", 1)

open(path, 'w', encoding='utf-8').write(s)
print('ok', path)
