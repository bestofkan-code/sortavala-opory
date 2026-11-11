#!/usr/bin/env python3
"""«План работ»: задание с порядком обхода опор (бурение котлованов, закладные, бетон).
- В режиме «Задания бригаде» добавлены виды работ «Котлованы», «Закладные», «Бетон» и кнопка
  «Порядок обхода» — выстраивает выбранные опоры в короткий маршрут (ближайшая следующая + 2-opt),
  начало — первая выбранная опора или ближайшая к вам, если включено «Где я». Порядок опор и есть маршрут
  (сохраняется в crew_tasks.uids по порядку). Выбранные опоры нумеруются на карте.
- Вверху панели блок «План работ»: открытые задания (сегодня / завтра — сверху). «Открыть план» —
  на карте номера опор по порядку и линия маршрута, красный номер — следующая опора; в блоке — список
  опор по порядку (нажать — карта покажет опору), «Следующая» и ссылки в Яндекс Карты (маршрут от вас
  до следующей опоры или по всем оставшимся). Готово — по отметкам работ задания.
- На монтажной карте бригаде эти задания (только котлованы / закладные / бетон) не показываются.
Применяется к redaktor.html (один раз): python3 tools/patch_main_plan.py redaktor.html
"""
import sys

path = sys.argv[1]
s = open(path, encoding='utf-8').read()
if 'id="pld"' in s:
    print('already applied')
    sys.exit(0)


def R(old, new, cnt=1):
    global s
    n = s.count(old)
    assert n == cnt, (old[:80], n)
    s = s.replace(old, new)


# 1) блок «План работ» — вверху панели
R('<div class="vw">Режим просмотра. Данные обновляются автоматически, редактирование недоступно.</div>',
  '<div class="vw">Режим просмотра. Данные обновляются автоматически, редактирование недоступно.</div>'
  '<details id="pld" open><summary><b>План работ</b><span id="pls"></span></summary><div id="pll"></div></details>', 1)

# 2) форма заданий: виды работ по фундаменту и кнопка порядка обхода
R('<b>Задания бригаде монтажников</b>', '<b>Задания бригаде и планы работ</b>', 1)
R('<label><input type="checkbox" data-k="5"> СИП</label><label><input type="checkbox" data-k="12"> Кронштейн</label>',
  '<label><input type="checkbox" data-k="1"> Котлованы</label><label><input type="checkbox" data-k="2"> Закладные</label><label><input type="checkbox" data-k="3"> Бетон</label>'
  '<label><input type="checkbox" data-k="5"> СИП</label><label><input type="checkbox" data-k="12"> Кронштейн</label>', 1)
R('<small id="tki" style="display:block"></small>',
  '<small id="tki" style="display:block"></small><div class="r"><button id="tkro" title="Выстроить выбранные опоры в короткий маршрут: начало — первая выбранная опора (или ближайшая к вам при включённом «Где я»)">Порядок обхода</button><small id="tkrl"></small></div>', 1)
R("const TKW=[[5,'СИП']", "const TKW=[[1,'Котлованы'],[2,'Закладные'],[3,'Бетон'],[5,'СИП']", 1)

# 3) бригаде (монтажная карта) планы по фундаментам не показываем
R("function tkAct(){return [...TK.values()].filter(t=>!t.done)}",
  "function plFnd(t){const w=t.works||[];return w.length>0&&w.every(k=>k==1||k==2||k==3)}\n"
  "function tkAct(){return [...TK.values()].filter(t=>!t.done&&!(TKV&&plFnd(t)))}", 1)
R("const A=L2.filter(t=>!t.done);", "const A=L2.filter(t=>!t.done&&!(TKV&&plFnd(t)));", 1)
R("toast('Задание «'+name+'» сохранено — бригада увидит его на монтажной карте')",
  "toast(plFnd(r)?'План «'+name+'» сохранён — он в блоке «План работ» вверху панели':'Задание «'+name+'» сохранено — бригада увидит его на монтажной карте')", 1)

# 4) стили
R('.tki2.dn{opacity:.55}',
  '.tki2.dn{opacity:.55}'
  '#pld{margin:6px 0 4px;border:1px solid #f59e0b;border-radius:8px;padding:3px 8px}'
  '#pld>summary{cursor:pointer;font-size:13px;list-style:none;display:flex;justify-content:space-between;align-items:center;gap:6px;padding:3px 0}'
  '#pld>summary::-webkit-details-marker{display:none}#pld>summary:after{content:\'▾\';opacity:.6}#pld:not([open])>summary:after{content:\'▸\'}'
  '#pls{font-size:11.5px;opacity:.9;margin-left:auto;text-align:right}'
  '#pll{font-size:12.5px}#pll .pli{border:1px solid rgba(127,127,127,.35);border-radius:8px;padding:5px 7px;margin:5px 0}'
  '#pll .pli>small{display:block;opacity:.85;margin-top:2px}#pll .pltg{display:inline-block;font-size:10.5px;font-weight:700;border-radius:8px;padding:0 6px;margin-left:4px;background:#f59e0b;color:#111}'
  '#pll .plnx{margin:6px 0;padding:6px 8px;border-radius:8px;background:rgba(220,38,38,.12);border:1px solid rgba(220,38,38,.5)}'
  '#pll .plnx a{display:inline-block;margin:4px 6px 0 0}'
  '#pll .plo{display:flex;flex-wrap:wrap;gap:3px;margin:5px 0}#pll .plo button{padding:2px 6px;font-size:11.5px;border-radius:9px}'
  '#pll .plo button.ok{border-color:#22c55e;opacity:.7}#pll .plo button.nx{border-color:#dc2626;font-weight:700}'
  '#pll .tkb{height:5px;background:rgba(127,127,127,.25);border-radius:3px;overflow:hidden;margin:3px 0}#pll .tkb i{display:block;height:100%;background:#22c55e}'
  '.pln{width:22px;height:22px;border-radius:50%;background:#f59e0b;color:#111;font:700 12px/22px system-ui,sans-serif;text-align:center;border:2px solid #fff;box-shadow:0 1px 4px rgba(0,0,0,.55);box-sizing:content-box}'
  '.pln.ok{background:#22c55e}.pln.nx{background:#dc2626;color:#fff;transform:scale(1.3)}', 1)

# 5) код
R("setTimeout(()=>{tkPull();tkList();tkDraw()},1400);setInterval(tkPull,30000);",
  r"""setTimeout(()=>{tkPull();tkList();tkDraw()},1400);setInterval(tkPull,30000);
/* ---- план работ: порядок обхода опор, номера на карте, следующая опора, маршрут в Яндекс Картах ---- */
var PLID=null,PLLY=L.layerGroup().addTo(map);try{PLID=localStorage.getItem(KEY+'_pl')||null}catch(e){}
const plD=(a,b)=>map.distance([a.lat,a.lon],[b.lat,b.lon]),plLen=a=>{let d=0;for(let i=1;i<a.length;i++)d+=plD(a[i-1],a[i]);return d},
 plKm=m=>m<1000?Math.round(m)+' м':(Math.round(m/100)/10+' км').replace('.',','),
 plYa=a=>'https://yandex.ru/maps/?rtext=~'+a.map(p=>p.lat.toFixed(6)+','+p.lon.toFixed(6)).join('~')+'&rtt=auto';
function plOrd(U){if(U.length<3)return U.slice();const rest=U.slice(1),o=[U[0]];
 while(rest.length){const c=o[o.length-1];let bi=0,bd=1e18;rest.forEach((p,i)=>{const x=plD(c,p);if(x<bd){bd=x;bi=i}});o.push(rest.splice(bi,1)[0])}
 let imp=true,it=0;while(imp&&it++<300){imp=false;for(let i=1;i<o.length-1;i++)for(let j=i+1;j<o.length;j++){const a=o[i-1],b=o[i],c=o[j],e=o[j+1],
  old=plD(a,b)+(e?plD(c,e):0),nw=plD(a,c)+(e?plD(b,e):0);if(nw<old-.5){const seg=o.slice(i,j+1).reverse();o.splice(i,j-i+1,...seg);imp=true}}}
 return o}
function plPoles(t){const M=new Map(P.map(p=>[p.uid,p]));return (t.uids||[]).map(u=>M.get(u)).filter(p=>p&&!(p.x&&!p.sx))}
function plDay(t){const td=LD(),tm=LD(new Date(Date.now()+864e5)),a=t.d1||'',b=t.d2||'';if(!a)return b&&b<td?'срок прошёл':'';if(!b)return a<=td?'в работе':a==tm?'завтра':'';if(b<td)return'срок прошёл';if(a<=td)return'сегодня';if(a<=tm)return'завтра';return''}
function plOpen(id){PLID=id;try{id?localStorage.setItem(KEY+'_pl',id):localStorage.removeItem(KEY+'_pl')}catch(e){}plDraw();plUI();
 if(id){const Ps=plPoles(TK.get(id)||{});if(Ps.length)map.fitBounds(L.latLngBounds(Ps.map(p=>[p.lat,p.lon])).pad(.12))}}
function plGo(p){map.setView([p.lat,p.lon],Math.max(map.getZoom(),19));const m=mk.get(p);if(m&&lg.hasLayer(m))L.popup(PO()).setLatLng(m.getLatLng()).setContent(popup(p)).openOn(map);else toast('Опора скрыта фильтром')}
function plDraw(){PLLY.clearLayers();const t=PLID&&TK.get(PLID);if(!t||t.done)return;const Ps=plPoles(t);if(!Ps.length)return;
 const nx=Ps.findIndex(p=>!tkPoleDone(p,t));
 L.polyline(Ps.map(p=>[p.lat,p.lon]),{color:'#f97316',weight:4,opacity:.95,dashArray:'10 7',interactive:false}).addTo(PLLY);
 Ps.forEach((p,i)=>{const ok=tkPoleDone(p,t);L.marker([p.lat,p.lon],{icon:L.divIcon({html:`<div class="pln${ok?' ok':''}${i==nx?' nx':''}">${i+1}</div>`,className:'',iconSize:[26,26],iconAnchor:[-4,30]}),zIndexOffset:i==nx?2000:1000,title:(i+1)+'. '+p.id+(ok?' — готово':'')}).on('click',()=>plGo(p)).addTo(PLLY)})}
function plUI(){const e=$('pll');if(!e)return;const T=[...TK.values()].filter(t=>!t.done),cur=PLID&&TK.get(PLID);
 if(cur&&!cur.done){const Ps=plPoles(cur),dn=Ps.map(p=>tkPoleDone(p,cur)),k=dn.filter(Boolean).length,nx=dn.indexOf(false),rest=Ps.filter((p,i)=>!dn[i]),dy=plDay(cur);
  let h=`<div class="pli"><div><b>${esc(cur.name||'Без названия')}</b>${dy?`<span class="pltg">${dy}</span>`:''}</div><small>${esc(tkWN(cur))}${tkPer(cur)?' · '+tkPer(cur):''} · маршрут ≈ ${plKm(plLen(Ps))} по прямой</small>`+
   `<small>Готово <b>${k}</b> из ${Ps.length}</small><div class="tkb"><i style="width:${Ps.length?k/Ps.length*100:0}%"></i></div>${cur.note?'<small>'+esc(cur.note)+'</small>':''}`;
  if(nx>=0){const p=Ps[nx];h+=`<div class="plnx">Следующая: <b>${nx+1}. ${esc(p.id)}</b> <small>(${p.t=='A'?'анкерная':'стандартная'}${isG(p)?', гравит. фундамент':''})</small><br>`+
   `<button data-plg="${esc(p.uid)}">Показать</button> <a href="${plYa([p])}" target="_blank" rel="noopener">Маршрут до неё ↗</a>`+(rest.length>1?`<a href="${plYa(rest.slice(0,9))}" target="_blank" rel="noopener">Все оставшиеся${rest.length>9?' (первые 9)':''} ↗</a>`:'')+'</div>'}
  else h+='<div class="plnx" style="background:rgba(34,197,94,.12);border-color:rgba(34,197,94,.6)"><b>Все опоры плана готовы</b></div>';
  h+='<div class="plo">'+Ps.map((p,i)=>`<button data-plg="${esc(p.uid)}" class="${dn[i]?'ok':i==nx?'nx':''}" title="${esc(p.id)}${dn[i]?' — готово':''}">${i+1}. ${esc(p.id)}${dn[i]?' ✓':''}</button>`).join('')+'</div>';
  h+=`<div class="r"><button data-plz>Показать весь план</button><button data-plc>Закрыть план</button></div></div>`;
  if(T.length>1)h+=`<small style="opacity:.75">Других открытых планов и заданий: ${T.length-1} — «Закрыть план», чтобы увидеть список.</small>`;
  e.innerHTML=h;$('pls').innerHTML=`<b>${k}</b> из ${Ps.length}`}
 else{const od=t=>({'сегодня':0,'завтра':1,'в работе':2,'срок прошёл':3,'':4})[plDay(t)];T.sort((a,b)=>od(a)-od(b)||String(a.d1||'9').localeCompare(String(b.d1||'9')));
  e.innerHTML=T.length?T.map(t=>{const g=tkProg(t),dy=plDay(t);return `<div class="pli"><div><b>${esc(t.name||'Без названия')}</b>${dy?`<span class="pltg">${dy}</span>`:''}</div><small>${esc(tkWN(t))}${tkPer(t)?' · '+tkPer(t):''} · опор ${g.N} · выполнено ${g.pc}%</small><div class="tkb"><i style="width:${g.pc}%"></i></div><div class="r"><button data-plo="${esc(t.id)}">Открыть план</button></div></div>`}).join('')
   :'<small style="opacity:.8">Открытых планов нет. Создать: режим «Задания бригаде» — выберите опоры, отметьте «Котлованы» (или другие работы), нажмите «Порядок обхода» и сохраните.</small>';
  $('pls').innerHTML=T.length?'открыто: <b>'+T.length+'</b>':''}}
$('pll').onclick=e=>{const b=e.target.closest('button');if(!b)return;
 if(b.dataset.plo)return plOpen(b.dataset.plo);if(b.dataset.plc!=null)return plOpen(null);
 if(b.dataset.plz!=null){const t=TK.get(PLID);if(t){const Ps=plPoles(t);if(Ps.length)map.fitBounds(L.latLngBounds(Ps.map(p=>[p.lat,p.lon])).pad(.12))}return}
 if(b.dataset.plg){const p=P.find(o=>o.uid==b.dataset.plg);if(p)plGo(p)}};
{const _tl=tkList;tkList=function(){_tl.apply(this,arguments);try{plDraw();plUI()}catch(e){}}}
{const _td=tkDraw;tkDraw=function(){_td.apply(this,arguments);if(mode!='task'||TKS.size<2)return;const M=new Map(P.map(p=>[p.uid,p])),Ps=[...TKS].map(u=>M.get(u)).filter(Boolean);
 L.polyline(Ps.map(p=>[p.lat,p.lon]),{color:'#22d3ee',weight:2,opacity:.8,dashArray:'4 6',interactive:false}).addTo(TKLY);
 Ps.forEach((p,i)=>L.marker([p.lat,p.lon],{icon:L.divIcon({html:`<div class="pln" style="background:#22d3ee">${i+1}</div>`,className:'',iconSize:[26,26],iconAnchor:[-4,30]}),interactive:false,zIndexOffset:1000}).addTo(TKLY));
 const r=$('tkrl');if(r)r.textContent='≈ '+plKm(plLen(Ps))+' по прямой'}}
if(!RO&&$('tkro'))$('tkro').onclick=()=>{const M=new Map(P.map(p=>[p.uid,p]));let U=[...TKS].map(u=>M.get(u)).filter(Boolean);if(U.length<2)return toast('Выберите хотя бы 2 опоры');
 if(typeof pos!='undefined'&&pos){const me={lat:pos[0],lon:pos[1]};let bi=0,bd=1e18;U.forEach((p,i)=>{const d=plD(me,p);if(d<bd){bd=d;bi=i}});U=[U[bi],...U.filter((p,i)=>i!=bi)]}
 const a=plLen(U),o=plOrd(U);TKS=new Set(o.map(p=>p.uid));tkDraw();tkInfo();toast('Порядок обхода: '+o.length+' опор, ≈ '+plKm(plLen(o))+' по прямой (было '+plKm(a)+'). Начало — '+o[0].id)};
setTimeout(()=>{plDraw();plUI()},1500);""", 1)

open(path, 'w', encoding='utf-8').write(s)
print('ok', path)
