import sys,json
src,remf,dst=sys.argv[1:4]
s=open(src,encoding='utf-8').read()
R=json.load(open(remf,encoding='utf-8'))
keep=['n','k','title','work','fix','src','chk','ids','uids','lat','lon','map','conf']
R=[{k:e.get(k,'') for k in keep} for e in R]
def rep(a,b):
    global s
    assert s.count(a)==1,(a,s.count(a));s=s.replace(a,b)
rep('<a href="prosmotr.html" style="font-size:13px">Открыть только просмотр','<a href="zamechaniya-prosmotr.html" style="font-size:13px">Открыть только просмотр')
rep('<title>Карта опор — Сортавала','<title>Замечания технадзора — карта опор')
rep('<b style="font-size:15px">Опоры освещения, Сортавала</b>','<b style="font-size:15px">Замечания технадзора · исп. схемы 22.10.2026</b><div style="font-size:12px;margin:2px 0 4px"><a href="redaktor.html" style="color:#9db4ff">← основная карта</a></div>')
HTML='''<details class="sec" id="tnsec" open><summary>Замечания технадзора <span id="tncnt"></span></summary>
<div id="tnsum" style="font-size:12px;margin:4px 0"></div>
<div class="r" style="flex-wrap:wrap;gap:4px"><select id="tnk" style="width:100%;min-width:0"><option value="">все виды</option></select><select id="tns"><option value="">любой статус</option><option value="open">не устранено</option><option value="work">в работе</option><option value="done">устранено</option><option value="chk">⚠ требуют уточнения</option></select><label style="font-size:12px"><input type="checkbox" id="tnonly" checked> на карте только опоры с замечаниями</label></div>
<div id="tnl" style="max-height:42vh;overflow:auto;margin-top:6px"></div>
<div class="r" style="margin-top:6px"><button id="tnx">Отчёт Excel</button></div></details>
<h3>Ход работ</h3>'''
rep('<h3>Ход работ</h3>',HTML)
CSS='''.tnb{display:inline-block;min-width:18px;padding:0 4px;border-radius:8px;font:700 10px system-ui;color:#fff;text-align:center;margin-right:2px}
.tnr{border:1px solid #2c3346;border-radius:8px;padding:6px 8px;margin:4px 0;cursor:pointer;font-size:12px;background:#161a24}.tnr:hover{border-color:#4f7cff}
.tnr .h{display:flex;justify-content:space-between;gap:6px}.tnr small{display:block;color:#9aa3b5}
.tnm{transform:translate(-50%,-50%);display:flex;gap:1px;pointer-events:auto;cursor:pointer}
.tnpr{display:flex;flex-wrap:wrap;gap:4px;margin-top:2px}.tnpt{position:relative}.tnpt img{width:58px;height:58px;object-fit:cover;border-radius:6px;border:1px solid #2c3346;cursor:zoom-in;display:block}
.tnpt b{position:absolute;top:-6px;right:-6px;width:18px;height:18px;border-radius:50%;background:#ef4444;color:#fff;font:700 12px/18px system-ui;text-align:center;cursor:pointer}
.tnpa{width:58px;height:58px;border:1px dashed #4f7cff;border-radius:6px;display:flex;align-items:center;justify-content:center;color:#9db4ff;font-size:22px;cursor:pointer}
.tnlb{position:fixed;inset:0;background:rgba(0,0,0,.88);z-index:3000;display:flex;flex-direction:column;align-items:center;justify-content:center;color:#eef1f7;font:13px system-ui}
.tnlb img{max-width:96vw;max-height:84vh;object-fit:contain}.tnlb div{margin-top:8px;text-align:center;padding:0 12px}
.tnlb b{position:absolute;top:50%;font-size:44px;cursor:pointer;padding:10px;user-select:none}.tnlb b[data-p]{left:6px}.tnlb b[data-n]{right:6px}.tnlb b[data-c]{top:10px;right:14px;font-size:26px}
.tng{font-weight:600;margin:8px 0 2px;font-size:12px;color:#c3cad8}
.tnst-open{color:#f87171}.tnst-work{color:#fbbf24}.tnst-done{color:#4ade80}
'''
rep('details.sec{margin:12px 0 0}',CSS+'details.sec{margin:12px 0 0}')
JS=r'''
/* ---- замечания технадзора (исполнительные схемы 22.10.2026) ---- */
var TNR=__REMS__;
var TNK={'К1':['#ef4444','Бетонирование: нет бетона в полости закладной'],'К2':['#f97316','Отклонение от горизонтали > 1,5 см'],'К3':['#a855f7','Пролёт между опорами > 45 м'],'АНК':['#eab308','Должна стоять анкерная закладная'],'АНК-факт':['#84cc16','Фактически стоит анкерная — исправить ИД'],'КАН':['#06b6d4','Бетон залил канаву'],'ПУЭ':['#ec4899','Расстояние < 1,0 м (п. 2.4.57 ПУЭ)'],'НИЗ':['#14b8a6','Слишком низко в канаве'],'НЕТ':['#64748b','На месте нет закладной/опоры']};
var TNST={},TNQ={},TNL=L.layerGroup().addTo(map),TNSTN={open:'не устранено',work:'в работе',done:'устранено'};
try{TNST=JSON.parse(localStorage.getItem(KEY+'_tn')||'{}')||{}}catch(e){}
try{TNQ=JSON.parse(localStorage.getItem(KEY+'_tnq')||'{}')||{}}catch(e){}
function tnSave(){try{localStorage.setItem(KEY+'_tn',JSON.stringify(TNST));localStorage.setItem(KEY+'_tnq',JSON.stringify(TNQ))}catch(e){}}
function tnS(r){return (TNST[r.n]&&TNST[r.n].st)||'open'}
function tnPole(u){return P.find(p=>p.uid==u)}
function tnPos(r){const ps=r.uids.map(tnPole).filter(Boolean);if(!ps.length)return[r.lat,r.lon];return[ps.reduce((a,p)=>a+p.lat,0)/ps.length,ps.reduce((a,p)=>a+p.lon,0)/ps.length]}
function tnOwn(r){const k=$('tnk').value,st=$('tns').value;return(!k||r.k==k)&&(!st||(st=='chk'?!!r.chk:tnS(r)==st))}
function tnWork(r){return r.uids.some(u=>{const p=tnPole(u);return p&&VIS0(p)})}
function tnVis(r){return tnOwn(r)&&tnWork(r)}
var VIS0=vis,TNU=new Set(),TNT=null;vis=function(p){return VIS0(p)&&(!$('tnonly').checked||TNU.has(p.uid))};
function tnU(){TNU=new Set();TNR.filter(tnVis).forEach(r=>r.uids.forEach(u=>TNU.add(u)))}
var ST0=stats;stats=function(){ST0.apply(this,arguments);clearTimeout(TNT);TNT=setTimeout(()=>{const a=[...TNU].sort().join();tnU();if([...TNU].sort().join()!=a&&$('tnonly').checked){P.forEach(upd);numLabels()}tnAll()},120)};
function tnFilt(){const a=[];if(FTS.size)a.push(tpLbl());if(wsel().length)a.push('работы: '+wsel().map(k=>(WK.find(w=>w[0]==k)||[0,k])[1]).join(', ')+($('wm').value=='1'?'':' (не выполнены)'));if($('wdf').value||$('wdt').value)a.push('даты '+($('wdf').value||'…')+' – '+($('wdt').value||'…'));if(ftyTxt())a.push('опоры: '+ftyTxt());if(!$('fd').checked||!$('fr').checked)a.push(!$('fd').checked?'без готовых':'только готовые');return a}
function tnDraw(){TNL.clearLayers();const groups=new Map();
TNR.filter(tnVis).forEach(r=>{if(r.k=='К3'){const ps=r.uids.map(tnPole).filter(Boolean);const c=tnS(r)=='done'?'#4ade80':TNK[r.k][0];
 L.polyline(ps.map(p=>[p.lat,p.lon]),{color:c,weight:7,opacity:.55,dashArray:'2 8',lineCap:'round'}).on('click',e=>{SPCLK=Date.now();tnPop([r],e.latlng)}).addTo(TNL)}
 const key=r.k=='К3'?'s'+r.n:r.uids[0];if(!groups.has(key))groups.set(key,[]);groups.get(key).push(r)});
groups.forEach((rs,key)=>{const pos=tnPos(rs[0]),all=rs.every(r=>tnS(r)=='done'),any=rs.some(r=>tnS(r)=='work');
 if(rs[0].k!='К3')L.circleMarker(pos,{radius:17,color:all?'#4ade80':any?'#fbbf24':'#ef4444',weight:3,fill:false,dashArray:all?null:'5 4',interactive:false}).addTo(TNL);
 const html='<div class="tnm">'+rs.map(r=>'<span class="tnb" style="background:'+(tnS(r)=='done'?'#16a34a':TNK[r.k][0])+'">'+esc(r.k)+'</span>').join('')+'</div>';
 L.marker(pos,{icon:L.divIcon({className:'',iconSize:[0,0],iconAnchor:[0,rs[0].k=='К3'?0:-26],html}),zIndexOffset:900}).on('click',()=>{SPCLK=Date.now();tnPop(rs,pos)}).addTo(TNL)});
}
function tnOnly(){tnU();P.forEach(upd);numLabels();stats()}
function tnPop(rs,ll0){const d=document.createElement('div');d.className='pp';
d.innerHTML=rs.map(r=>{const t=TNST[r.n]||{};return '<div style="border-bottom:1px solid #2c3346;padding:4px 0"><div><span class="tnb" style="background:'+TNK[r.k][0]+'">'+esc(r.k)+'</span><b>№'+r.n+' · '+esc(r.title)+'</b></div>'
+'<div><small>Опоры: '+r.ids.map(esc).join(' — ')+' · в схеме: «'+esc(r.src)+'»</small></div>'

+'<div style="margin-top:3px"><small>Карта: '+esc(r.map)+'</small></div><div class="tnph" data-tnph="'+r.n+'"></div>'
+(r.chk?'<div style="color:#fbbf24;font-size:12px">⚠ '+esc(r.chk)+'</div>':'')
+(RO?'<div>Статус: <b class="tnst-'+tnS(r)+'">'+TNSTN[tnS(r)]+'</b>'+(t.note?' · '+esc(t.note):'')+'</div>':
'<div class="r" style="margin-top:4px;flex-wrap:wrap"><select data-tns="'+r.n+'">'+['open','work','done'].map(k=>'<option value="'+k+'"'+(tnS(r)==k?' selected':'')+'>'+TNSTN[k]+'</option>').join('')+'</select><input type="date" data-tnd="'+r.n+'" value="'+(t.dt||'')+'"></div>'
+'<input type="text" data-tnn="'+r.n+'" placeholder="Что сделано / примечание" value="'+esc(t.note||'')+'">'
+(t.ed?'<small>'+esc(t.ed)+(t.updated_at?' · '+String(t.updated_at).slice(0,16).replace('T',' '):'')+'</small>':''))+'</div>'}).join('')
+(RO?'':'<div class="r" style="margin-top:6px"><button data-tnsv>Сохранить</button>'+(rs[0].uids[0]?'<button data-tnp>Открыть опору</button>':'')+'</div>');
if(!RO){d.querySelectorAll('[data-tns]').forEach(sel=>sel.onchange=()=>{PSEL=Date.now();const i=d.querySelector('[data-tnd="'+sel.dataset.tns+'"]');if(sel.value=='done'&&!i.value)i.value=LD()});
d.querySelector('[data-tnsv]').onclick=()=>{if(!AUTH())return alert('Войдите, чтобы менять статус замечаний.');const nf=rs.filter(r=>d.querySelector('[data-tns="'+r.n+'"]').value=='done'&&!tnPh(r.n,'after').length);if(nf.length&&!confirm('Нет фото «после» для замечания №'+nf.map(r=>r.n).join(', №')+'. Всё равно отметить устранённым?'))return;rs.forEach(r=>{const row={n:r.n,st:d.querySelector('[data-tns="'+r.n+'"]').value,dt:d.querySelector('[data-tnd="'+r.n+'"]').value||null,note:d.querySelector('[data-tnn="'+r.n+'"]').value.trim()||null,ed:WHO||null};TNST[r.n]={...TNST[r.n],...row};TNQ[r.n]=row});tnSave();map.closePopup();tnAll();tnSend();toast('Статус замечаний сохранён')};
const b=d.querySelector('[data-tnp]');if(b)b.onclick=()=>{const p=tnPole(rs[0].uids[0]);map.closePopup();if(p)qgo(p)}}
d.querySelectorAll('[data-tnph]').forEach(tnPhR);L.popup(PO()).setLatLng(ll0).setContent(d).openOn(map)}
function tnList(){const V=TNR.filter(tnVis),B=TNR.filter(tnWork),c={open:0,work:0,done:0};B.forEach(r=>c[tnS(r)]++);const F=tnFilt();
$('tncnt').innerHTML='<small>'+c.done+'/'+TNR.length+'</small>';
$('tnsum').innerHTML=(F.length?'<div style="color:#9db4ff">С учётом фильтров работ ('+esc(F.join('; '))+'): '+B.length+' из '+TNR.length+' <a href="#" id="tnfx" style="color:#9db4ff">сбросить</a></div>':'')+'<span class="tnst-open">не устранено '+c.open+'</span> · <span class="tnst-work">в работе '+c.work+'</span> · <span class="tnst-done">устранено '+c.done+'</span>'+(B.some(r=>r.chk)?' · <span style="color:#fbbf24">⚠ уточнить '+B.filter(r=>r.chk).length+'</span>':'')+(V.length!=B.length?'<div>Показано: '+V.length+'</div>':'');
const fx=$('tnfx');if(fx)fx.onclick=e=>{e.preventDefault();document.querySelectorAll('#wf input').forEach(x=>x.checked=false);$('wdf').value=$('wdt').value='';ftyReset();$('fd').checked=$('fr').checked=true;if(FTS.size){FTS.clear();ftChange(false);try{tps()}catch(e){}}P.forEach(upd);stats();numLabels()};
const byK=new Map();Object.keys(TNK).forEach(k=>{if(V.some(r=>r.k==k))byK.set(k,[])});V.forEach(r=>{if(!byK.has(r.k))byK.set(r.k,[]);byK.get(r.k).push(r)});
$('tnl').innerHTML=[...byK].map(([k,rs])=>'<div class="tng"><span class="tnb" style="background:'+TNK[k][0]+'">'+esc(k)+'</span>'+esc(TNK[k][1])+' — '+rs.length+'</div>'+rs.map(r=>'<div class="tnr" data-tn="'+r.n+'"><div class="h"><b>№'+r.n+' · '+r.ids.map(esc).join(' — ')+'</b><span class="tnst-'+tnS(r)+'">'+TNSTN[tnS(r)]+'</span></div><small>'+esc(r.map)+'</small>'+tnPhC(r.n)+(r.chk?'<small style="color:#fbbf24">⚠ '+esc(r.chk)+'</small>':'')+'</div>').join('')).join('')||'<small>Нет замечаний по фильтру.</small>'}
function tnAll(){tnOpts();tnDraw();tnList()}
function tnOpts(){const v=$('tnk').value,B=TNR.filter(r=>tnWork(r)&&(!$('tns').value||($('tns').value=='chk'?!!r.chk:tnS(r)==$('tns').value)));$('tnk').innerHTML='<option value="">все виды ('+B.length+')</option>'+Object.keys(TNK).map(k=>'<option value="'+k+'">'+k+' · '+TNK[k][1]+' ('+B.filter(r=>r.k==k).length+')</option>').join('');$('tnk').value=v}
$('tnk').onchange=$('tns').onchange=()=>{tnOnly();tnAll()};$('tnonly').onchange=tnOnly;
$('tnl').onclick=e=>{const b=e.target.closest('[data-tn]');if(!b)return;const r=TNR.find(x=>x.n==+b.dataset.tn),pos=tnPos(r);map.setView(pos,Math.max(map.getZoom(),19));setTimeout(()=>tnPop(TNR.filter(x=>x.k!='К3'&&r.k!='К3'?x.uids[0]==r.uids[0]&&tnVis(x):x.n==r.n),pos),350)};
$('tnx').onclick=()=>{const rows=[['№','Код','Замечание','Вид работ','Опоры','Текст в схеме','Способ устранения','Сопоставление с картой','Уточнить','Статус','Дата','Примечание','Кто','Фото до','Фото после']];
TNR.forEach(r=>{const t=TNST[r.n]||{};rows.push([r.n,r.k,r.title,r.work,r.ids.join(' — '),r.src,r.fix,r.map,r.chk||'',TNSTN[tnS(r)],t.dt||'',t.note||'',t.ed||'',tnPh(r.n,'before').map(tnPhU).join('\n'),tnPh(r.n,'after').map(tnPhU).join('\n')])});
const wb=XLSX.utils.book_new(),ws=XLSX.utils.aoa_to_sheet(rows);ws['!cols']=[{wch:4},{wch:9},{wch:34},{wch:24},{wch:30},{wch:22},{wch:60},{wch:50},{wch:40},{wch:13},{wch:11},{wch:30},{wch:10},{wch:50},{wch:50}];XLSX.utils.book_append_sheet(wb,ws,'Замечания');
const sm=[['Код','Замечание','Способ устранения','Всего','Не устранено','В работе','Устранено']];Object.keys(TNK).forEach(k=>{const a=TNR.filter(r=>r.k==k);if(a.length)sm.push([k,TNK[k][1],a[0].fix,a.length,a.filter(r=>tnS(r)=='open').length,a.filter(r=>tnS(r)=='work').length,a.filter(r=>tnS(r)=='done').length])});
const w2=XLSX.utils.aoa_to_sheet(sm);w2['!cols']=[{wch:9},{wch:40},{wch:70},{wch:7},{wch:12},{wch:9},{wch:10}];XLSX.utils.book_append_sheet(wb,w2,'Сводка');XLSX.writeFile(wb,'Замечания_технадзора_'+LD()+'.xlsx')};
async function tnSend(){if(!CF||RO)return;const ks=Object.keys(TNQ);if(!ks.length)return;try{await authFresh()}catch(e){}
try{const r=await fetch(CF.u+'/rest/v1/tn_remarks?on_conflict=n',{method:'POST',headers:{...H(),Prefer:'resolution=merge-duplicates,return=minimal'},body:JSON.stringify(ks.map(k=>({...TNQ[k],updated_at:new Date().toISOString()})))});if(!r.ok)throw new Error(await r.text());ks.forEach(k=>delete TNQ[k]);tnSave()}catch(e){tnSave();ss('Статусы замечаний не отправлены: '+(e instanceof TypeError?'нет связи':e.message||e)+', отправлю позже')}}
async function tnPull(){if(!CF)return;try{const r=await fetch(CF.u+'/rest/v1/tn_remarks?select=*',{headers:H()}),j=await r.json();if(!Array.isArray(j))return;const m={};j.forEach(x=>m[x.n]=x);Object.keys(TNQ).forEach(k=>m[k]={...m[k],...TNQ[k]});if(JSON.stringify(m)!=JSON.stringify(TNST)){TNST=m;tnSave();if(!document.querySelector('.leaflet-popup [data-tns]'))tnAll()}}catch(e){}}

/* ---- фото до/после по замечаниям ---- */
var TNP=[];try{TNP=JSON.parse(localStorage.getItem(KEY+'_tnp')||'[]')||[]}catch(e){}
function tnPh(n,k){return TNP.filter(x=>x.n==n&&(!k||x.kind==k))}
function tnPhU(x){return CF.u+'/storage/v1/object/public/tn-photos/'+x.path.split('/').map(encodeURIComponent).join('/')}
function tnPhC(n){const b=tnPh(n,'before').length,a=tnPh(n,'after').length;return (a||b)?'<small style="color:#9db4ff">📷 до '+b+' · после '+a+'</small>':''}
function tnPhR(box){const n=+box.dataset.tnph;const row=(k,t)=>{const L2=tnPh(n,k);return '<div style="margin-top:4px"><small>'+t+(L2.length?' ('+L2.length+')':'')+'</small><div class="tnpr">'+L2.map(x=>'<span class="tnpt"><img src="'+tnPhU(x)+'" loading="lazy" data-tnpv="'+x.id+'" alt="">'+(RO?'':'<b data-tnpd="'+x.id+'" title="Удалить">×</b>')+'</span>').join('')+(RO?(L2.length?'':'<small style="color:#6b7280">нет</small>'):'<label class="tnpa" title="Добавить фото">＋<input type="file" accept="image/*" multiple data-tnpk="'+k+'" hidden></label>')+'</div></div>'};
box.innerHTML=row('before','Фото до')+row('after','Фото после');
box.querySelectorAll('[data-tnpv]').forEach(i=>i.onclick=()=>tnPhView(i.dataset.tnpv));
box.querySelectorAll('[data-tnpd]').forEach(b=>b.onclick=async()=>{PSEL=Date.now();if(!AUTH())return alert('Войдите, чтобы удалять фото.');if(!confirm('Удалить фото?'))return;const x=TNP.find(o=>o.id==b.dataset.tnpd);if(!x)return;try{await authFresh()}catch(e){}
 try{let r=await fetch(CF.u+'/rest/v1/tn_photos?id=eq.'+x.id,{method:'DELETE',headers:H()});if(!r.ok)throw new Error(await r.text());await fetch(CF.u+'/storage/v1/object/tn-photos/'+x.path.split('/').map(encodeURIComponent).join('/'),{method:'DELETE',headers:H()});TNP=TNP.filter(o=>o.id!=x.id);tnPhSave();tnPhRefresh()}catch(e){alert('Не удалось удалить: '+(e.message||e))}});
box.querySelectorAll('[data-tnpk]').forEach(inp=>{inp.onclick=()=>{PSEL=Date.now()};inp.onchange=async()=>{PSEL=Date.now();if(!AUTH()){inp.value='';return alert('Войдите, чтобы добавлять фото.')}const fs=[...inp.files];inp.value='';if(!fs.length)return;const lab=inp.parentNode;lab.textContent='…';let ok=0;
 for(const f of fs){try{await tnPhUp(n,inp.dataset.tnpk,f);ok++}catch(e){alert('Фото не загружено: '+(e instanceof TypeError?'нет связи':e.message||e))}}
 tnPhRefresh();if(ok)toast('Загружено фото: '+ok)}})}
function tnPhRefresh(){document.querySelectorAll('.leaflet-popup [data-tnph]').forEach(tnPhR);tnList()}
function tnPhSave(){try{localStorage.setItem(KEY+'_tnp',JSON.stringify(TNP))}catch(e){}}
function tnShrink(f){return new Promise((ok,no)=>{const u=URL.createObjectURL(f),im=new Image();im.onload=()=>{const M=1600,k=Math.min(1,M/Math.max(im.width,im.height)),c=document.createElement('canvas');c.width=Math.round(im.width*k);c.height=Math.round(im.height*k);c.getContext('2d').drawImage(im,0,0,c.width,c.height);URL.revokeObjectURL(u);c.toBlob(b=>b?ok(b):no(new Error('не удалось сжать')),'image/jpeg',.82)};im.onerror=()=>{URL.revokeObjectURL(u);no(new Error('файл не похож на фото'))};im.src=u})}
async function tnPhUp(n,kind,f){try{await authFresh()}catch(e){}const b=await tnShrink(f),path=n+'/'+kind+'/'+LD()+'_'+Date.now()+'_'+Math.random().toString(36).slice(2,7)+'.jpg';
let r=await fetch(CF.u+'/storage/v1/object/tn-photos/'+path,{method:'POST',headers:{...H(),'Content-Type':'image/jpeg','x-upsert':'false'},body:b});if(!r.ok)throw new Error(await r.text());
r=await fetch(CF.u+'/rest/v1/tn_photos',{method:'POST',headers:{...H(),Prefer:'return=representation'},body:JSON.stringify({n,kind,path,ed:WHO||null})});if(!r.ok)throw new Error(await r.text());const j=await r.json();TNP.push(...j);tnPhSave()}
function tnPhView(id){const x=TNP.find(o=>o.id==id);if(!x)return;const L2=tnPh(x.n),i0=L2.indexOf(x);let i=i0;const o=document.createElement('div');o.className='tnlb';
const show=()=>{const y=L2[i];o.innerHTML='<img src="'+tnPhU(y)+'" alt=""><div>Замечание №'+y.n+' · '+(y.kind=='before'?'до':'после')+' · '+(y.created_at?new Date(y.created_at).toLocaleString('ru',{day:'2-digit',month:'2-digit',year:'numeric',hour:'2-digit',minute:'2-digit'}):'')+(y.ed?' · '+esc(y.ed):'')+(L2.length>1?' · '+(i+1)+'/'+L2.length:'')+'</div>'+(L2.length>1?'<b data-p>‹</b><b data-n>›</b>':'')+'<b data-c>✕</b>';
 const p=o.querySelector('[data-p]'),nx=o.querySelector('[data-n]');if(p)p.onclick=e=>{e.stopPropagation();i=(i-1+L2.length)%L2.length;show()};if(nx)nx.onclick=e=>{e.stopPropagation();i=(i+1)%L2.length;show()}};
show();o.onclick=e=>{if(e.target.tagName!='IMG')o.remove()};document.body.appendChild(o)}
async function tnPhPull(){if(!CF)return;try{const r=await fetch(CF.u+'/rest/v1/tn_photos?select=*&order=created_at&limit=5000',{headers:H()}),j=await r.json();if(!Array.isArray(j))return;if(JSON.stringify(j)!=JSON.stringify(TNP)){TNP=j;tnPhSave();tnPhRefresh()}}catch(e){}}
setTimeout(()=>{tnOnly();tnAll();tnSend();tnPull();tnPhPull()},1200);setInterval(()=>{tnSend();tnPull();tnPhPull()},20000);
'''.replace('__REMS__',json.dumps(R,ensure_ascii=False))
rep('\nredraw();stats();map.fitBounds','\nredraw();stats();'+JS+'\nmap.fitBounds')
open(dst,'w',encoding='utf-8').write(s);print('ok',len(s))
