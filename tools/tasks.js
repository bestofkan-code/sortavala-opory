/* ---- задания бригаде монтажников (таблица crew_tasks): редакторы выделяют опоры, бригада видит их на монтажной карте ---- */
var TK=new Map(),TKS=new Set(),TKE=null,TKA=false,TKPTS=[],TKLY=L.layerGroup().addTo(map),TKONLY=false;
const TKW=[[5,'СИП'],[12,'Кронштейн'],[6,'Светильник'],[14,'Подрезка крон'],[100,'Бронекабель']];
try{(JSON.parse(localStorage.getItem(KEY+'_tk')||'[]')||[]).forEach(r=>TK.set(r.id,r))}catch(e){}
function tkSave(){try{localStorage.setItem(KEY+'_tk',JSON.stringify([...TK.values()]))}catch(e){}}
function fdm(v){return v?String(v).slice(8,10)+'.'+String(v).slice(5,7):''}
function tkPer(t){return t.d1||t.d2?(t.d1?fdm(t.d1):'…')+'–'+(t.d2?fdm(t.d2):'…'):''}
function tkWN(t){return (t.works||[]).map(k=>(TKW.find(w=>w[0]==k)||[0,k])[1]).join(', ')}
function tkAct(){return [...TK.values()].filter(t=>!t.done)}
function tkOf(p){return tkAct().filter(t=>(t.uids||[]).includes(p.uid))}
function tkPoles(t){const U=new Set(t.uids||[]);return P.filter(p=>U.has(p.uid)&&!(p.x&&!p.sx))}
function tkPoleDone(p,t){return (t.works||[]).every(k=>k==100?(!p.vk||cabDone(p.tp)):(p.x&&(k==6||k==12))?true:wdone(p,k))}
function tkProg(t){const Ps=tkPoles(t);let a=0,n=0;(t.works||[]).forEach(k=>{if(k==100){Ps.filter(p=>p.vk).forEach(p=>{n++;if(cabDone(p.tp))a++})}else Ps.forEach(p=>{if(p.x&&(k==6||k==12))return;n++;if(wdone(p,k))a++})});return{a,n,N:Ps.length,pc:n?Math.round(a/n*100):0}}
function tkDraw(){if(typeof TKLY=='undefined')return;TKLY.clearLayers();const sel=mode=='task';if(!TKV&&!sel)return;const U=new Map();tkAct().forEach(t=>(t.uids||[]).forEach(u=>{if(!U.has(u))U.set(u,t)}));
 P.forEach(p=>{const inS=sel&&TKS.has(p.uid),t=U.get(p.uid);if(!inS&&!t)return;if(!vis(p))return;const ok=t&&!inS&&tkPoleDone(p,t);
  L.circleMarker([p.lat,p.lon],{radius:inS?17:15,color:inS?'#22d3ee':ok?'#4ade80':'#06b6d4',weight:inS?4:3,opacity:inS?1:.85,fill:inS,fillColor:'#22d3ee',fillOpacity:.15,dashArray:inS||ok?null:'4 4',interactive:false}).addTo(TKLY)});
 if(TKPTS.length)(TKPTS.length>2?L.polygon:L.polyline)(TKPTS,{color:'#22d3ee',weight:3,dashArray:'6 6',fillColor:'#22d3ee',fillOpacity:.06,interactive:false}).addTo(TKLY)}
function tkShow(id){const t=TK.get(id);if(!t)return;const Ps=tkPoles(t);if(!Ps.length)return toast('В задании нет опор на карте');map.fitBounds(L.latLngBounds(Ps.map(p=>[p.lat,p.lon])).pad(.15))}
function tkRow(t,ed){const g=tkProg(t);return `<div class="tki2${t.done?' dn':''}"><div><b>${esc(t.name||'Без названия')}</b> <small style="display:inline">${tkPer(t)}${t.done?' · закрыто':''}</small></div><small>${esc(tkWN(t))} · опор ${g.N} · выполнено ${g.pc}%</small><div class="tkb"><i style="width:${g.pc}%"></i></div>${t.note?'<small>'+esc(t.note)+'</small>':''}<div class="r"><button data-tks="${t.id}">Показать</button>${ed?`<button data-tke="${t.id}">Изменить</button><button data-tkd="${t.id}">${t.done?'Вернуть':'Закрыть'}</button><button data-tkr="${t.id}" style="color:#f87171">Удалить</button>`:''}</div></div>`}
function tkList(){const L2=[...TK.values()].sort((a,b)=>(a.done-b.done)||String(a.d2||a.d1||'9').localeCompare(String(b.d2||b.d1||'9'))),bind=e=>{e.querySelectorAll('[data-tks]').forEach(b=>b.onclick=()=>tkShow(b.dataset.tks));e.querySelectorAll('[data-tke]').forEach(b=>b.onclick=()=>tkEdit(b.dataset.tke));e.querySelectorAll('[data-tkd]').forEach(b=>b.onclick=()=>{const t=TK.get(b.dataset.tkd);if(t)tkPut(Object.assign({},t,{done:!t.done})).catch(er=>toast('Не сохранилось: '+(er.message||er)))});e.querySelectorAll('[data-tkr]').forEach(b=>b.onclick=()=>{const t=TK.get(b.dataset.tkr);if(t&&confirm('Удалить задание «'+(t.name||'')+'»?'))tkDel(t.id).catch(er=>toast('Не удалилось: '+(er.message||er)))})};
 const c=$('ctk');if(c){const A=L2.filter(t=>!t.done);c.innerHTML=(A.length?A.map(t=>tkRow(t,false)).join(''):'<small>Заданий пока нет — работайте по общему плану.</small>')+(A.length?'<label style="display:block;font-size:12px;margin-top:4px"><input type="checkbox" id="tko"'+(TKONLY?' checked':'')+'> показывать только опоры заданий</label>':'');bind(c);const o=$('tko');if(o)o.onchange=()=>{TKONLY=o.checked;P.forEach(upd);numLabels();tkDraw();stats()}}
 const e=$('tkl');if(e&&!TKV){e.innerHTML=L2.length?'<b style="display:block;margin-top:6px">Задания ('+L2.filter(t=>!t.done).length+' открыто)</b>'+L2.map(t=>tkRow(t,true)).join(''):'';bind(e)}}
async function tkPull(){if(!CF)return;try{const r=await fetch(CF.u+'/rest/v1/crew_tasks?select=*',{headers:H()}),j=await r.json();if(!Array.isArray(j))return;const m=new Map(j.map(x=>[x.id,x])),a=JSON.stringify([...TK.entries()].sort()),b=JSON.stringify([...m.entries()].sort());if(a!=b){TK=m;tkSave();if(TKONLY)P.forEach(upd);tkDraw();tkList()}}catch(e){}}
async function tkPut(r){r.ed=WHO||null;r.updated_at=new Date().toISOString();TK.set(r.id,r);tkSave();tkDraw();tkList();try{await authFresh()}catch(e){}const x=await fetch(CF.u+'/rest/v1/crew_tasks?on_conflict=id',{method:'POST',headers:{...H(),Prefer:'resolution=merge-duplicates,return=minimal'},body:JSON.stringify(r)});if(!x.ok)throw new Error(await x.text())}
async function tkDel(id){TK.delete(id);tkSave();tkDraw();tkList();try{await authFresh()}catch(e){}const x=await fetch(CF.u+'/rest/v1/crew_tasks?id=eq.'+encodeURIComponent(id),{method:'DELETE',headers:H()});if(!x.ok)throw new Error(await x.text())}
function tkInfo(){const e=$('tki');if(!e)return;if(TKA){e.textContent='Нажимайте по карте углы участка. Точек: '+TKPTS.length+(TKPTS.length>2?'. Нажмите «Готово».':'');return}e.textContent='Выбрано опор: '+TKS.size+(TKE&&TK.get(TKE)?' · правка задания «'+(TK.get(TKE).name||'')+'»':'')}
function tkTog(p){if(TKS.has(p.uid))TKS.delete(p.uid);else TKS.add(p.uid);tkDraw();tkInfo()}
function tkPt(ll){TKPTS.push([ll.lat,ll.lng]);tkDraw();tkInfo()}
function tkBtns(){$('tka').hidden=TKA;$('tkok').hidden=$('tkun').hidden=!TKA;map.getContainer().style.cursor=TKA?'crosshair':''}
function tkForm(t){$('tkn').value=t?t.name||'':'';$('tk1').value=t?t.d1||'':LD();$('tk2').value=t?t.d2||'':'';$('tkt').value=t?t.note||'':'';document.querySelectorAll('#tkw input').forEach(c=>c.checked=t?(t.works||[]).includes(+c.dataset.k):false);$('tkx').hidden=!t;$('tks').textContent=t?'Сохранить изменения':'Сохранить задание'}
function tkEdit(id){const t=TK.get(id);if(!t)return;if(mode!='task'){const b=document.querySelector('#modes [data-m="task"]');if(b)b.click()}TKE=id;TKS=new Set(t.uids||[]);tkForm(t);tkDraw();tkInfo();tkShow(id)}
if(!RO&&$('tka')){
 $('tka').onclick=()=>{map.closePopup();TKA=true;TKPTS=[];tkBtns();tkDraw();tkInfo()};
 $('tkun').onclick=()=>{TKPTS.pop();tkDraw();tkInfo()};
 $('tkok').onclick=()=>{if(TKPTS.length>2){const pts=TKPTS.map(a=>lm(a[0],a[1]));let n=0;P.forEach(p=>{if(!vis(p)||(p.x&&!p.sx))return;const q=lm(p.lat,p.lon);if(inpoly(q[0],q[1],pts)&&!TKS.has(p.uid)){TKS.add(p.uid);n++}});toast('Добавлено опор: '+n)}TKA=false;TKPTS=[];tkBtns();tkDraw();tkInfo()};
 $('tkc').onclick=()=>{TKS.clear();TKE=null;TKA=false;TKPTS=[];tkBtns();tkForm(null);tkDraw();tkInfo()};
 $('tkx').onclick=()=>$('tkc').onclick();
 $('tks').onclick=async()=>{const works=[...document.querySelectorAll('#tkw input:checked')].map(c=>+c.dataset.k),name=$('tkn').value.trim();if(!TKS.size)return alert('Выберите опоры: нажимайте на опоры или обведите участок.');if(!works.length)return alert('Отметьте виды работ для бригады.');if(!name)return alert('Впишите название задания, например «ул. Победы, ТП90».');
  const old=TKE&&TK.get(TKE),r={id:old?old.id:'tk'+Date.now().toString(36)+Math.random().toString(36).slice(2,6),name,works,uids:[...TKS],d1:$('tk1').value||null,d2:$('tk2').value||null,note:$('tkt').value.trim(),done:old?!!old.done:false};
  try{await tkPut(r);toast('Задание «'+name+'» сохранено — бригада увидит его на монтажной карте');TKS.clear();TKE=null;tkForm(null);tkDraw();tkInfo()}catch(e){alert('Задание не сохранилось: '+(e.message||e))}};
 map.on('click',e=>{if(mode=='task'&&TKA)tkPt(e.latlng)});tkForm(null)}
setTimeout(()=>{tkPull();tkList();tkDraw()},1400);setInterval(tkPull,30000);
