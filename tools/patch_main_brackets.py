#!/usr/bin/env python3
"""Блок «Проверка кронштейнов» под таблицей «Контракт и выполнение»:
по каждой ТП — однорожковые / 90° / 180° (установлено из всего), тип не указан, «можно ставить»
(опора стоит, кронштейна нет), опоры с замечаниями; список замечаний (нажать — карта покажет опору);
выгрузка «Таблица проверки кронштейнов» в Excel (по ТП, по опорам с графами для проверки на месте, замечания).
Применяется к redaktor.html (один раз): python3 tools/patch_main_brackets.py redaktor.html
"""
import sys

path = sys.argv[1]
s = open(path, encoding='utf-8').read()
if 'id="kcd"' in s:
    print('already applied')
    sys.exit(0)


def R(old, new, cnt=1):
    global s
    n = s.count(old)
    assert n == cnt, (old[:80], n)
    s = s.replace(old, new)


# 1) блок — сразу после «Контракт и выполнение»
R('Красным — расхождение карты с контрактом.</small></details>',
  'Красным — расхождение карты с контрактом.</small></details>'
  '<details id="kcd"><summary><b>Проверка кронштейнов</b><span id="kcs"></span></summary>'
  '<small id="kcn">Цифры — установлено / всего этого типа. «Можно» — опора стоит, кронштейна ещё нет. '
  '«⚠» — опор с замечаниями. Нажмите на опору в списке — карта покажет её.</small>'
  '<table id="kct"></table><div id="kcl"></div>'
  '<div class="r"><button id="kcx">Таблица проверки (Excel)</button></div></details>', 1)

# 2) стили — по образцу «Контракт и выполнение»
R('#ktn{display:block;opacity:.75;margin:2px 0 3px;line-height:1.3}',
  '#ktn{display:block;opacity:.75;margin:2px 0 3px;line-height:1.3}'
  '#kcd{margin:6px 0 4px;border:1px solid rgba(127,127,127,.4);border-radius:8px;padding:3px 8px}'
  '#kcd>summary{cursor:pointer;font-size:13px;list-style:none;display:flex;justify-content:space-between;align-items:center;gap:6px;padding:3px 0}'
  '#kcd>summary::-webkit-details-marker{display:none}#kcd>summary:after{content:\'▾\';opacity:.6}#kcd:not([open])>summary:after{content:\'▸\'}'
  '#kcs{font-size:11.5px;opacity:.9;margin-left:auto;text-align:right}'
  '#kct{width:100%;border-collapse:collapse;font-size:12px;margin:3px 0 2px}'
  '#kct th,#kct td{padding:3px 4px;text-align:right;border-bottom:1px solid rgba(127,127,127,.22);white-space:nowrap;font-variant-numeric:tabular-nums}'
  '#kct th{font-weight:600;font-size:11px;opacity:.85}#kct th:first-child,#kct td:first-child{text-align:left;white-space:normal}'
  '#kct td small{opacity:.6;font-size:10.5px}#kct td.z{opacity:.4}#kct tr.kt td{font-weight:700}'
  '#kcd .bad{color:#dc2626;font-weight:700}.dk #kcd .bad{color:#f87171}#kcd .ok{color:#15803d}.dk #kcd .ok{color:#4ade80}'
  '#kcn{display:block;opacity:.75;margin:2px 0 3px;line-height:1.3}'
  '.kcg{margin:6px 0 2px;font-size:12px}.kcg>div{display:flex;flex-wrap:wrap;gap:3px;margin-top:3px}'
  '.kcg button{padding:2px 6px;font-size:11.5px;border-radius:9px}', 1)

# 3) пересчёт вместе с «Контракт и выполнение»
R('try{ktUI()}catch(e){}', 'try{ktUI()}catch(e){}try{kcUI()}catch(e){}', 1)

# 4) код — сразу после «Контракт и выполнение»
R('/* ---- фильтр «Опоры»: стандартные/анкерные, 8/9 м ---- */',
  r'''/* ---- проверка кронштейнов: по ТП, замечания по опорам, Excel ---- */
try{if(localStorage.getItem(KEY+'_kc')==='1')$('kcd').open=true}catch(e){}
$('kcd').addEventListener('toggle',()=>{try{localStorage.setItem(KEY+'_kc',$('kcd').open?'1':'0')}catch(e){}});
var KCG=[['nt','Тип кронштейна не указан'],['na','Двухрожковый — не указан угол 90° или 180°'],['nd','Кронштейн отмечен, а опора не отмечена установленной'],
 ['nk','Светильник отмечен, а кронштейн нет'],['sv','Светильников больше, чем рожков'],['s1','Двухрожковый, светильник отмечен 1 из 2'],['ex','Кронштейн отмечен на исключённой опоре или на гравитационном фундаменте']];
const kcT=p=>{const k=+p.kr||0;return k==1?'1':k==2?(+p.ka==90?'90':+p.ka==180?'180':'2?'):'?'},
 kcNm={'1':'1-рожковый','90':'2-рожк. 90°','180':'2-рожк. 180°','2?':'2-рожк., угол не указан','?':'не указан'},
 kcRu=(a,b)=>String(a).localeCompare(String(b),'ru',{numeric:true}),
 kcLum=p=>(+p.kr||0)==2?2:(+p.kr||0)==1?1:0,kcLi=p=>wdone(p,6)?(+p.sv||Math.max(1,+p.kr||1)):0;
function kcIss(p){const r=[],t=kcT(p),k12=wdone(p,12),k6=wdone(p,6),sv=+p.sv||0,kr=+p.kr||0;
 if(p.x||isG(p)){if(k12)r.push(['ex','кронштейн отмечен, а опора '+(p.x?'исключена':'на гравитационном фундаменте')]);return r}
 if(t=='?')r.push(['nt','тип кронштейна не указан']);
 if(t=='2?')r.push(['na','двухрожковый — не указан угол 90° или 180°']);
 if(k12&&!p.done)r.push(['nd','кронштейн отмечен, а опора не отмечена установленной']);
 if(k6&&!k12)r.push(['nk','светильник отмечен, а кронштейн нет']);
 if(k6&&kr&&sv>kr)r.push(['sv','светильников '+sv+', а рожков '+kr]);
 if(k6&&kr==2&&sv==1)r.push(['s1','двухрожковый, светильник отмечен 1 из 2']);
 return r}
function kcData(){const C=P.filter(p=>!p.x&&!isG(p)),G=new Map();
 C.forEach(p=>{const k=String(p.tp||'—');if(!G.has(k))G.set(k,[]);G.get(k).push(p)});
 const I=[];P.forEach(p=>kcIss(p).forEach(([c,m])=>I.push({p,c,m})));
 const st=a=>{const o={n:a.length,lum:0,li:0,can:0,iss:0,unk:0,dn:0};['1','90','180'].forEach(f=>{const x=a.filter(p=>kcT(p)==f);o['a'+f]=x.length;o['d'+f]=x.filter(p=>wdone(p,12)).length});
  a.forEach(p=>{const t=kcT(p);if(t=='?'||t=='2?')o.unk++;if(wdone(p,12))o.dn++;if(p.done&&!wdone(p,12))o.can++;if(kcIss(p).length)o.iss++;o.lum+=kcLum(p);o.li+=kcLi(p)});return o};
 const T=[...G.keys()].sort(kcRu).map(k=>({k,a:G.get(k),s:st(G.get(k))}));
 return{C,T,S:st(C),I}}
function kcUI(){const t=$('kct');if(!t)return;const D=kcData(),I=D.I;
 const c=(o,f)=>o['a'+f]?`<td title="установлено ${o['d'+f]} из ${o['a'+f]}">${o['d'+f]}<small>/${o['a'+f]}</small></td>`:'<td class="z">—</td>';
 const row=(nm,o,cls)=>`<tr${cls?' class="'+cls+'"':''}><td>${nm}</td>${c(o,'1')}${c(o,'90')}${c(o,'180')}<td${o.unk?' class="bad"':''}>${o.unk||'—'}</td><td title="опора стоит, кронштейна ещё нет">${o.can||'—'}</td><td class="${o.iss?'bad':'ok'}">${o.iss||'✓'}</td></tr>`;
 let h='<tr><th>ТП</th><th title="однорожковые: установлено / всего">1-р.</th><th title="двухрожковые 90°: установлено / всего">90°</th><th title="двухрожковые 180°: установлено / всего">180°</th><th title="тип кронштейна не указан">тип?</th><th title="опора стоит, кронштейна ещё нет — можно ставить">можно</th><th title="опор с замечаниями">⚠</th></tr>';
 D.T.forEach(r=>h+=row(esc(tpn(r.k)),r.s));h+=row('Всего',D.S,'kt');t.innerHTML=h;
 let l='';KCG.forEach(([g,nm])=>{const a=I.filter(x=>x.c==g).sort((x,y)=>kcRu(x.p.id,y.p.id));if(!a.length)return;
  l+=`<div class="kcg"><b>${nm} — ${a.length}</b><div>${a.map(x=>`<button data-kc="${esc(x.p.uid)}" title="${esc(x.m)}">${esc(x.p.id)}</button>`).join('')}</div></div>`});
 $('kcl').innerHTML=l||'<small class="ok">Замечаний нет</small>';
 const n=new Set(I.map(x=>x.p.uid)).size;$('kcs').innerHTML=`кр. <b>${D.S.dn}</b> · можно <b>${D.S.can}</b> · `+(n?`<b class="bad">⚠ ${n}</b>`:'<b class="ok">✓</b>');
 $('kcs').title='Кронштейнов установлено '+D.S.dn+', можно ставить сейчас '+D.S.can+(n?', опор с замечаниями '+n:', замечаний нет')}
$('kcl').onclick=e=>{const b=e.target.closest('[data-kc]');if(!b)return;const p=P.find(o=>o.uid==b.dataset.kc);if(!p)return;
 map.setView([p.lat,p.lon],Math.max(map.getZoom(),19));const m=mk.get(p);if(m&&lg.hasLayer(m))L.popup(PO()).setLatLng(m.getLatLng()).setContent(popup(p)).openOn(map);else toast('Опора скрыта фильтром')};
function kcXl(){const D=kcData(),wb=XLSX.utils.book_new(),dt=v=>/^\d{4}-\d\d-\d\d/.test(v)?v.slice(8,10)+'.'+v.slice(5,7)+'.'+v.slice(0,4):(v?'да':''),
 K={'1':353,'90':50,'180':189};
 const h1=['ТП','1-рожк. всего','1-рожк. установлено','2-рожк. 90° всего','2-рожк. 90° установлено','2-рожк. 180° всего','2-рожк. 180° установлено','Тип не указан','Кронштейнов установлено','Осталось установить','Можно ставить сейчас (опора стоит)','Светильников по типу кронштейна','Светильников установлено','Опор с замечаниями'];
 const r1=(nm,o)=>[nm,o.a1,o.d1,o.a90,o.d90,o.a180,o.d180,o.unk,o.dn,o.n-o.dn,o.can,o.lum,o.li,o.iss];
 const A1=[['Проверка кронштейнов по ТП — '+dt(LD())],[],h1,...D.T.map(r=>r1(tpn(r.k),r.s)),r1('Всего на карте',D.S),
  ['По контракту',K['1'],'',K['90'],'',K['180'],'','',  '','','',KTC.lum,'',''],
  ['Разница карта − контракт',D.S.a1-K['1'],'',D.S.a90-K['90'],'',D.S.a180-K['180'],'','','','','',D.S.lum-KTC.lum,'',''],[],
  ['На карте — опоры контракта без исключённых и опор на гравитационном фундаменте. Установлено — по отметке «Установлен кронштейн».']];
 const w1=XLSX.utils.aoa_to_sheet(A1);w1['!cols']=[{wch:18},...h1.slice(1).map(()=>({wch:12}))];XLSX.utils.book_append_sheet(wb,w1,'По ТП');
 const h2=['№','Опора','ТП','Тип опоры','Высота, м','Кронштейн по карте','Светильников по типу','Опора установлена','Кронштейн установлен','Светильник установлен','Светильников отмечено','Замечание по карте','Проверено на месте (✓)','Кронштейн по факту','Примечание'];
 const pl=P.filter(p=>(!p.x&&!isG(p))||kcIss(p).length).sort((a,b)=>kcRu(a.tp,b.tp)||kcRu(a.id,b.id));
 const A2=[h2,...pl.map((p,i)=>[i+1,p.id,tpn(String(p.tp||'')),p.x?'исключена':isG(p)?'гравит. фундамент':p.t=='A'?'анкерная':'стандартная',+p.h==9?9:8,kcNm[kcT(p)],kcLum(p),dt(wd(p,4)),dt(wd(p,12)),dt(wd(p,6)),wdone(p,6)?(+p.sv||Math.max(1,+p.kr||1)):'',kcIss(p).map(x=>x[1]).join('; '),'','',''])];
 const w2=XLSX.utils.aoa_to_sheet(A2);w2['!cols']=[{wch:5},{wch:18},{wch:14},{wch:13},{wch:8},{wch:22},{wch:10},{wch:12},{wch:12},{wch:12},{wch:10},{wch:44},{wch:12},{wch:16},{wch:24}];
 w2['!autofilter']={ref:'A1:O'+A2.length};XLSX.utils.book_append_sheet(wb,w2,'По опорам');
 const A3=[['Замечание','Опора','ТП','Кронштейн по карте','Подробно'],...KCG.flatMap(([g,nm])=>D.I.filter(x=>x.c==g).sort((x,y)=>kcRu(x.p.id,y.p.id)).map(x=>[nm,x.p.id,tpn(String(x.p.tp||'')),kcNm[kcT(x.p)],x.m]))];
 if(A3.length==1)A3.push(['Замечаний нет']);const w3=XLSX.utils.aoa_to_sheet(A3);w3['!cols']=[{wch:50},{wch:18},{wch:14},{wch:22},{wch:44}];XLSX.utils.book_append_sheet(wb,w3,'Замечания');
 XLSX.writeFile(wb,'Проверка_кронштейнов_'+LD()+'.xlsx')}
$('kcx').onclick=()=>{try{kcXl()}catch(e){alert('Ошибка выгрузки: '+(e.message||e))}};
/* ---- фильтр «Опоры»: стандартные/анкерные, 8/9 м ---- */''', 1)

open(path, 'w', encoding='utf-8').write(s)
print('ok', path)
