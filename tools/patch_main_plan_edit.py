#!/usr/bin/env python3
"""Правка «Плана работ» прямо на карте (после patch_main_plan.py):
- «Изменить план»: нажимайте на опоры на карте — опора добавляется в маршрут на самое выгодное место
  (после уже сделанных) или убирается; в списке ↑ ↓ ✕; «Пересчитать порядок» — короткий маршрут по несделанным;
  подсказка «Рядом ещё не сделано» — ближайшие опоры без этой работы в 500 м от маршрута, «+» — добавить;
  название и дата плана; «Сохранить» / «Отмена».
- «Новый план» — пустой план бурения на завтра, сразу в режиме правки.
Только в редакторе (в просмотре правки нет).
Применяется к redaktor.html (один раз): python3 tools/patch_main_plan_edit.py redaktor.html
"""
import sys

path = sys.argv[1]
s = open(path, encoding='utf-8').read()
if 'function plTog(' in s:
    print('already applied')
    sys.exit(0)


def R(old, new, cnt=1):
    global s
    n = s.count(old)
    assert n == cnt, (old[:80], n)
    s = s.replace(old, new)


# нажатие на опору в режиме правки плана
R("m.on('click',()=>{if(DGM)return;",
  "m.on('click',()=>{if(DGM)return;if(typeof PLED!='undefined'&&PLED&&!SELA&&!dt){plTog(p);return}", 1)
# план берём с учётом правки
R("const t=PLID&&TK.get(PLID);if(!t||t.done)return;", "const t=plCur();if(!t||t.done)return;", 1)
R("cur=PLID&&TK.get(PLID);", "cur=plCur();", 1)
# в режиме правки — свой вид блока
R('h+=`<div class="r"><button data-plz>Показать весь план</button><button data-plc>Закрыть план</button></div></div>`;',
  'h+=`<div class="r"><button data-plz>Показать весь план</button>${RO?\'\':\'<button data-ple>Изменить план</button>\'}<button data-plc>Закрыть план</button></div></div>`;\n'
  '  if(PLED){e.innerHTML=plEdUI(cur,Ps,dn);$(\'pls\').innerHTML=\'<b style="color:#f59e0b">правка</b>\';return}', 1)
R(":'<small style=\"opacity:.8\">Открытых планов нет.",
  ":'<small style=\"opacity:.8\">Открытых планов нет. Нажмите «Новый план» или создайте его в режиме «Задания бригаде».</small><small style=\"display:none\">", 1)
R("$('pls').innerHTML=T.length?'открыто: <b>'+T.length+'</b>':''}}",
  "if(!RO)e.insertAdjacentHTML('beforeend','<div class=\"r\"><button data-pln>+ Новый план бурения</button></div>');$('pls').innerHTML=T.length?'открыто: <b>'+T.length+'</b>':''}}", 1)
R("$('pll').onclick=e=>{const b=e.target.closest('button');if(!b)return;",
  "$('pll').onclick=e=>{const b=e.target.closest('button');if(!b)return;if(plEdClick(b))return;", 1)

# стили
R('.pln.ok{background:#22c55e}',
  '.pln.ok{background:#22c55e}'
  '#pll .ple{border:1px dashed #f59e0b;border-radius:8px;padding:6px 7px;margin:5px 0}#pll .ple input{width:100%;box-sizing:border-box;margin:2px 0}'
  '#pll .plr{display:flex;align-items:center;gap:3px;padding:2px 0;border-bottom:1px solid rgba(127,127,127,.18)}#pll .plr span{flex:1;min-width:0}'
  '#pll .plr button{padding:1px 7px;font-size:12px}#pll .plr.ok span{opacity:.6}#pll .plr button[data-plx]{color:#f87171}'
  '#pll .plsg{display:flex;flex-wrap:wrap;gap:3px;margin:3px 0}#pll .plsg button{padding:2px 6px;font-size:11.5px;border-radius:9px;border-style:dashed}', 1)

# код
R("setTimeout(()=>{plDraw();plUI()},1500);",
  r"""setTimeout(()=>{plDraw();plUI()},1500);
/* ---- правка плана на карте ---- */
var PLED=false,PLE=[],PLNEW=null,PLN={};
function plRd(){const n=$('plen'),a=$('pled1'),c=$('pled2');if(n)PLN.name=n.value;if(a)PLN.d1=a.value||null;if(c)PLN.d2=c.value||null}
function plCur(){const t=PLID&&(TK.get(PLID)||(PLNEW&&PLNEW.id==PLID?PLNEW:null));return t&&PLED?Object.assign({},t,{uids:PLE,name:PLN.name??t.name,d1:PLN.d1??t.d1,d2:PLN.d2??t.d2}):t}
function plEdStart(){const t=TK.get(PLID)||PLNEW;if(!t)return;PLED=true;PLE=(t.uids||[]).slice();PLN={};map.closePopup();plDraw();plUI();toast('Правка плана: нажимайте на опоры на карте — добавить или убрать')}
function plEdEnd(){PLED=false;PLE=[];PLN={};if(PLNEW){TK.delete(PLID);PLNEW=null;PLID=null;try{localStorage.removeItem(KEY+'_pl')}catch(e){}}plDraw();plUI()}
function plTail(t,Ps){let k=0;Ps.forEach((p,i)=>{if(tkPoleDone(p,t))k=i+1});return k}
function plTog(p){plRd();const t=plCur();if(!t)return;const i=PLE.indexOf(p.uid);
 if(i>=0){PLE.splice(i,1);toast('Убрана из плана: '+p.id)}
 else{if(p.x&&!p.sx)return toast('Опора исключена — в план не добавляется');const Ps=plPoles(t),s0=plTail(t,Ps);let bi=Ps.length,bd=1e18;
  for(let j=s0;j<=Ps.length;j++){const a=Ps[j-1],b=Ps[j],d=(a?plD(a,p):0)+(b?plD(p,b):0)-(a&&b?plD(a,b):0);if(d<bd){bd=d;bi=j}}
  const at=bi<Ps.length?PLE.indexOf(Ps[bi].uid):PLE.length;PLE.splice(at,0,p.uid);toast('Добавлена: '+p.id+' — №'+(at+1)+(tkPoleDone(p,t)?' (эта работа на ней уже отмечена)':''))}
 plDraw();plUI()}
function plSug(t,Ps){if(!Ps.length)return[];const S=new Set(PLE),w=t.works||[];
 return P.filter(p=>!S.has(p.uid)&&!p.x&&!(w.includes(1)&&isG(p))&&!tkPoleDone(p,t)).map(p=>{let d=1e9;Ps.forEach(q=>{const x=plD(p,q);if(x<d)d=x});return{p,d}}).filter(x=>x.d<=500).sort((a,b)=>a.d-b.d).slice(0,10)}
function plEdUI(t,Ps,dn){const sg=plSug(t,Ps);
 return `<div class="ple"><b>Правка плана</b><small style="display:block;opacity:.8;margin:2px 0 4px">Нажимайте на опоры на карте: добавить — встанет в маршрут на самое выгодное место, повторно — убрать.</small>`+
  `<input type="text" id="plen" value="${esc(t.name||'')}" placeholder="Название плана"><div class="r">Дата: <input type="date" id="pled1" value="${t.d1||''}" style="width:auto"> по <input type="date" id="pled2" value="${t.d2||''}" style="width:auto"></div>`+
  `<small style="display:block;margin-top:4px">Опор в плане: <b>${Ps.length}</b>, готово ${dn.filter(Boolean).length} · маршрут ≈ ${plKm(plLen(Ps))} по прямой</small>`+
  Ps.map((p,i)=>`<div class="plr${dn[i]?' ok':''}"><span>${i+1}. ${esc(p.id)}${dn[i]?' ✓':''}${isG(p)?' <small>(гравит.)</small>':''}</span><button data-plu="${i}" title="Выше"${i?'':' disabled'}>↑</button><button data-pldn="${i}" title="Ниже"${i<Ps.length-1?'':' disabled'}>↓</button><button data-plx="${i}" title="Убрать из плана">✕</button></div>`).join('')+
  (sg.length?`<small style="display:block;margin-top:6px">Рядом ещё не сделано (до 500 м от маршрута):</small><div class="plsg">${sg.map(x=>`<button data-pla="${esc(x.p.uid)}" title="Добавить в план">+ ${esc(x.p.id)} · ${plKm(x.d)}</button>`).join('')}</div>`:'')+
  `<div class="r" style="margin-top:6px"><button data-plo2 title="Сделанные опоры — в начало списка, остальные — короткий маршрут от последней сделанной (или от первой в списке)">Пересчитать порядок</button><button data-pls style="border-color:#22c55e">Сохранить</button><button data-plq>Отмена</button></div></div>`}
function plEdClick(b){const d=b.dataset;
 if(d.ple!=null){plEdStart();return true}
 if(d.pln!=null){const tm=LD(new Date(Date.now()+864e5)),id='tk'+Date.now().toString(36)+Math.random().toString(36).slice(2,6);
  PLNEW={id,name:'Бурение котлованов '+tm.slice(8,10)+'.'+tm.slice(5,7),works:[1],uids:[],d1:tm,d2:tm,note:'',done:false};PLID=id;plEdStart();return true}
 if(!PLED)return false;
 plRd();
 if(d.plq!=null){plEdEnd();return true}
 if(d.plx!=null){const p=plPoles(plCur())[+d.plx];if(p)PLE.splice(PLE.indexOf(p.uid),1);plDraw();plUI();return true}
 if(d.plu!=null||d.pldn!=null){const Ps=plPoles(plCur()),i=+(d.plu??d.pldn),j=d.plu!=null?i-1:i+1;if(Ps[i]&&Ps[j]){const a=PLE.indexOf(Ps[i].uid),c=PLE.indexOf(Ps[j].uid);[PLE[a],PLE[c]]=[PLE[c],PLE[a]]}plDraw();plUI();return true}
 if(d.pla){const p=P.find(o=>o.uid==d.pla);if(p)plTog(p);return true}
 if(d.plo2!=null){const t=plCur(),Ps=plPoles(t),done=Ps.filter(p=>tkPoleDone(p,t)),rest=Ps.filter(p=>!tkPoleDone(p,t));if(rest.length<2)return toast('Нечего пересчитывать'),true;
  const a=plLen(Ps),o=done.length?plOrd([done[done.length-1],...rest]).slice(1):plOrd(rest);PLE=[...done,...o].map(p=>p.uid);plDraw();plUI();toast('Порядок пересчитан: ≈ '+plKm(plLen(plPoles(plCur())))+' (было '+plKm(a)+')');return true}
 if(d.pls!=null){const t=plCur();if(!PLE.length)return alert('В плане нет опор. Нажмите на опоры на карте.'),true;if(!String(t.name||'').trim())return alert('Впишите название плана.'),true;
  const r={id:t.id,name:String(t.name).trim(),works:t.works,uids:PLE.slice(),d1:t.d1||null,d2:t.d2||null,note:t.note||'',done:!!t.done};
  tkPut(r).then(()=>{toast('План «'+r.name+'» сохранён');PLNEW=null;PLED=false;PLE=[];PLN={};try{localStorage.setItem(KEY+'_pl',r.id)}catch(e){}plDraw();plUI()}).catch(er=>alert('План не сохранился: '+(er.message||er)));return true}
 return false}""", 1)

open(path, 'w', encoding='utf-8').write(s)
print('ok', path)
