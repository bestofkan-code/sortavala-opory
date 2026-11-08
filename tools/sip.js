/* ---- СИП-карта: как пойдёт СИП по опорам, длины пролётов, ответвления, расчёт арматуры ---- */
var SIPL=L.layerGroup(),SIPLB=L.layerGroup(),SIPRG=L.layerGroup(),SIPC=null,SIPT=0;
/* нормы (на что умножаем) и количества по РД (уч. 1 + уч. 2) для сверки */
var SIPN={sipK:1.02,an:1,sus:1,slL:2,slB:4,tape:1.5,skr:1.5,vvg:2.04,cap:4};
var SIPRD={sip:16998,an:197,br:197,sus:577,sliw:2314,tape:1244,skr:1244,vvg:1224};
var SIPR={root:'ввод от ТП',end:'концевая',anchor:'анкерная',corner:'угловая (поворот ≥45°)',branch:'ответвительная',mid:'промежуточная'};
function sipPath(e){return epath(e[0],e[1],e.pts)}
function sipLen(e){const pt=sipPath(e);let d=0;for(let i=1;i<pt.length;i++)d+=map.distance(pt[i-1],pt[i]);return d}
function sipMid(pt){if(pt.length==2)return[(pt[0][0]+pt[1][0])/2,(pt[0][1]+pt[1][1])/2];let t=0;const s=[];for(let i=1;i<pt.length;i++){const d=map.distance(pt[i-1],pt[i]);s.push(d);t+=d}let h=t/2;for(let i=0;i<s.length;i++){if(h<=s[i]){const f=s[i]?h/s[i]:0;return[pt[i][0]+(pt[i+1][0]-pt[i][0])*f,pt[i][1]+(pt[i+1][1]-pt[i][1])*f]}h-=s[i]}return pt[pt.length-1]}
function sipCalc(){
 const N=NETC||netEdges(),U=new Map(P.map(p=>[p.uid,p])),isC=p=>!p.x&&!isG(p),kk=(a,b)=>a<b?a+'|'+b:b+'|'+a;
 const adj=new Map(),ad=(a,b,e)=>{if(!adj.has(a.uid))adj.set(a.uid,[]);adj.get(a.uid).push({o:b,e})};
 N.E.forEach(e=>{ad(e[0],e[1],e);ad(e[1],e[0],e)});
 const roots=new Set();CABS.forEach(z=>{if(z.p)roots.add(z.p.uid)});
 /* тупиковые отрезки, ведущие только к опорам не по контракту (гравитационный фундамент, исключённые) — следующий этап */
 const A=new Map([...adj].map(([k,v])=>[k,v.slice()]));let ch=true;
 while(ch){ch=false;for(const [u,l] of [...A]){const p=U.get(u);if(l.length<=1&&!isC(p)&&!roots.has(u)){l.forEach(x=>{const o=A.get(x.o.uid);if(o)A.set(x.o.uid,o.filter(y=>y.o.uid!=u))});A.delete(u);ch=true}}}
 const keep=new Set();A.forEach((l,u)=>l.forEach(x=>keep.add(kk(u,x.o.uid))));
 /* магистраль: от опоры ввода до самой дальней опоры сети; остальное — ответвления */
 const trunk=new Set(),seen=new Set();
 A.forEach((l0,u0)=>{if(seen.has(u0))return;const nodes=[],q=[u0];seen.add(u0);while(q.length){const v=q.shift();nodes.push(v);(A.get(v)||[]).forEach(x=>{if(!seen.has(x.o.uid)){seen.add(x.o.uid);q.push(x.o.uid)}})}
  const r=nodes.find(v=>roots.has(v))||nodes.find(v=>(A.get(v)||[]).length==1)||nodes[0],dist=new Map([[r,0]]),par=new Map(),st=[r];
  while(st.length){const v=st.pop();(A.get(v)||[]).forEach(x=>{const w=x.o.uid;if(!dist.has(w)){dist.set(w,dist.get(v)+sipLen(x.e));par.set(w,v);st.push(w)}})}
  let far=r;dist.forEach((d,v)=>{if(d>dist.get(far))far=v});for(let v=far;par.has(v);v=par.get(v))trunk.add(kk(v,par.get(v)))});
 const ED=N.E.map(e=>{const k=kk(e[0].uid,e[1].uid);return{e,a:e[0],b:e[1],len:sipLen(e),k,kind:keep.has(k)?(trunk.has(k)?'t':'b'):'n'}});
 const dirTo=(p,x)=>{const pts=x.e.pts;let q=x.o;if(pts&&pts.length){const s=x.e[0].uid==p.uid?pts[0]:pts[pts.length-1];q={lat:s[0],lon:s[1]}}return Math.atan2((q.lat-p.lat)*K2,(q.lon-p.lon)*K1)};
 const ND=new Map();
 A.forEach((l,u)=>{const p=U.get(u),deg=l.length,root=roots.has(u),an=p.t=='A';let turn=null;
  if(deg==2){let d=Math.abs(dirTo(p,l[0])-dirTo(p,l[1]))*180/Math.PI;if(d>180)d=360-d;turn=Math.round(180-d)}
  let role,anc=0,sus=0,con=0,ends=0;
  if(root){role='root';anc=deg;con=deg;ends=deg}
  else if(deg==1){role='end';anc=1;ends=1}
  else if(deg>=3){role='branch';if(an)anc=deg;else{anc=deg-2;sus=1}con=deg-2}
  else if(an||turn>=45){role=an?'anchor':'corner';anc=2}
  else{role='mid';sus=1}
  const lum=isC(p)?((+p.kr||0)==2?2:(+p.kr||0)==1?1:0):0;
  ND.set(u,{p,deg,turn,role,anc,sus,con,ends,lum,root,nb:l.map(x=>({o:x.o,len:sipLen(x.e),k:kk(u,x.o.uid)}))})});
 return{ED,ND,trunk}}
function sipSum(C){const E=C.ED.filter(x=>x.kind!='n'&&(tpOk(x.a)||tpOk(x.b))),Nn=[...C.ND.values()].filter(n=>tpOk(n.p)),s=f=>Nn.reduce((a,n)=>a+f(n),0);
 const o={len:E.reduce((a,x)=>a+x.len,0),spans:E.length,nodes:Nn.length,anc:s(n=>n.anc),sus:s(n=>n.sus),con:s(n=>n.con),ends:s(n=>n.ends),lum:s(n=>n.lum),r:{},tp:new Map()};
 Object.keys(SIPR).forEach(k=>o.r[k]=Nn.filter(n=>n.role==k).length);
 const nx=C.ED.filter(x=>x.kind=='n'&&(tpOk(x.a)||tpOk(x.b)));o.nextN=nx.length;o.nextL=nx.reduce((a,x)=>a+x.len,0);
 const T=t=>{t=String(t||'—');if(!o.tp.has(t))o.tp.set(t,{sp:0,len:0,tr:0,br:0,anc:0,sus:0,brn:0,nd:0});return o.tp.get(t)};
 E.forEach(x=>{const r=T(x.a.tp);r.sp++;r.len+=x.len;if(x.kind=='t')r.tr+=x.len;else r.br+=x.len});
 Nn.forEach(n=>{const r=T(n.p.tp);r.nd++;r.anc+=n.anc;r.sus+=n.sus;if(n.role=='branch')r.brn++});
 return o}
function sipRows(o){const n=SIPN;return[
 ['СИП-4 4×25','м','длина пролётов по карте, м',Math.round(o.len),n.sipK,'длина × 1,02 на провис','sip'],
 ['Зажим анкерный SO250.01','шт','анкерных креплений СИП',o.anc,n.an,'по 1 на каждый конец СИП, закреплённый анкерно','an'],
 ['Кронштейн анкерный SO253','шт','анкерных креплений СИП',o.anc,n.an,'по 1 на анкерный зажим','br'],
 ['Подвеска промежуточная SO260','шт','промежуточных креплений',o.sus,n.sus,'по 1 на промежуточную опору','sus'],
 ['Зажим прокалывающий SLIW 50 (светильники)','шт','светильников на линии',o.lum,n.slL,'по 2 на светильник: фаза и ноль','sliw'],
 ['Зажим прокалывающий SLIW 50 (ответвления, вводы)','шт','подключений ответвлений и вводов',o.con,n.slB,'по 4 на подключение: 4 жилы',''],
 ['Лента бандажная СОТ 37','м','кронштейнов SO253 + SO260',o.anc+o.sus,n.tape,'1,5 м на кронштейн','tape'],
 ['Скрепа СОТ 36','шт','кронштейнов SO253 + SO260',o.anc+o.sus,n.skr,'1,5 шт. на кронштейн','skr'],
 ['Провод ВВГнг(А)-LS 3×1,5','м','светильников на линии',o.lum,n.vvg,'2 м на светильник × 1,02','vvg'],
 ['Колпачок изолирующий','шт','концов СИП',o.ends,n.cap,'по 4 на конец СИП: 4 жилы','']]}
function sipQ(r){return Math.ceil(r[3]*r[4]-1e-9)}
function sipStats(){const e=$('sips');if(!e||$('sipp').hidden||!SIPC)return;const o=sipSum(SIPC),f=x=>Math.round(x).toLocaleString('ru'),ALL=!FTS.size,
 miss=ALL?Math.max(0,592-P.filter(p=>!p.x&&!isG(p)).length):0,avg=o.spans?o.len/o.spans:0,R=sipRows(o),sl=sipQ(R[4])+sipQ(R[5]);
 let h=`<div>Пролётов <b>${o.spans}</b> · <b>${f(o.len)}</b> м по карте · средний пролёт ${f(avg)} м</div>`;
 if(miss)h+=`<div>Ещё ${miss} опор контракта нет на карте: ≈ ${f(miss*avg)} м СИП</div>`;
 h+=`<div>Опор на линии <b>${o.nodes}</b>: ввод от ТП ${o.r.root}, концевых ${o.r.end}, анкерных ${o.r.anchor}, угловых ${o.r.corner}, ответвительных ${o.r.branch}, промежуточных ${o.r.mid}</div>`;
 if(o.nextN)h+=`<div style="opacity:.75">В расчёт не входят ${o.nextN} пролётов, ${f(o.nextL)} м: они ведут только к опорам на гравитационном фундаменте (следующий этап).</div>`;
 h+='<table id="sipt"><tr><th>Арматура и провод</th><th>По карте</th><th>'+(ALL?'По РД':'')+'</th></tr>';
 R.forEach((r,i)=>{if(i==5)return;const q=i==4?sl:sipQ(r),rd=ALL&&r[6]?SIPRD[r[6]]:'';h+=`<tr><td>${esc(i==4?'Зажим прокалывающий SLIW 50':r[0])}<small>${esc(i==4?'2 на светильник + 4 на ответвление или ввод':r[5])}</small></td><td>${f(q)}${r[1]=='м'?' м':''}</td><td>${rd===''?'':f(rd)}</td></tr>`});
 h+='</table>';
 if(miss)h+=`<small style="display:block;opacity:.75">Без ${miss} опор, которых нет на карте. По РД — спецификации участков 1 и 2 на 592 опоры.</small>`;
 const tps=[...o.tp.entries()].sort((a,b)=>a[0].localeCompare(b[0],'ru',{numeric:true}));
 h+='<details id="sipd"'+(SIPDO?' open':'')+'><summary>По ТП</summary><table id="siptp"><tr><th>ТП</th><th>пролётов</th><th>м</th><th>из них ответвл., м</th><th>анкер. крепл.</th><th>подвесок</th></tr>'+tps.map(([t,r])=>`<tr><td>${esc(tpn(t))}</td><td>${r.sp}</td><td>${f(r.len)}</td><td>${f(r.br)}</td><td>${r.anc}</td><td>${r.sus}</td></tr>`).join('')+'</table></details>';
 e.innerHTML=h;const d=$('sipd');if(d)d.ontoggle=()=>{SIPDO=d.open}}
var SIPDO=false;
function sipLabels(){SIPLB.clearLayers();if(mode!='sip'||!SIPC||map.getZoom()<17)return;const b=map.getBounds().pad(.2);
 SIPC.ED.forEach(x=>{if(!(tpOk(x.a)||tpOk(x.b)))return;const m=sipMid(sipPath(x.e));if(!b.contains(m))return;
  L.marker(m,{pane:'sipLb',icon:L.divIcon({className:'',html:'<div class="sipl'+(x.kind=='n'?' n':'')+'">'+Math.round(x.len)+' м</div>',iconSize:[0,0]}),interactive:false,keyboard:false}).addTo(SIPLB)})}
function sipSpanPop(x){const k={t:'магистраль',b:'ответвление',n:'к опоре на гравитационном фундаменте — следующий этап'}[x.kind];
 return `<div class="pp"><b>${esc(x.a.id)} — ${esc(x.b.id)}</b><div>Пролёт ≈ <b>${Math.round(x.len)} м</b> (СИП с запасом ≈ ${Math.ceil(x.len*SIPN.sipK)} м)</div><small>${k}</small></div>`}
function sipPop(p){const d=document.createElement('div');d.className='pp';const n=SIPC&&SIPC.ND.get(p.uid);
 let h=`<div><b>${esc(p.id)}</b> <small>${p.t=='A'?'анкерная':'стандартная'} ${+p.h==9?9:8} м</small></div>`;
 if(!n)h+='<div style="margin:4px 0">Опора не на линии СИП'+(SIPC&&SIPC.ED.some(x=>x.kind=='n'&&(x.a===p||x.b===p))?' этого этапа (тупиковый отрезок к опорам на гравитационном фундаменте)':'')+'.</div>';
 else{const it=[];if(n.anc)it.push('анкерных зажимов SO250.01 и кронштейнов SO253 — по '+n.anc);if(n.sus)it.push('подвеска SO260 — '+n.sus);const sl=n.lum*SIPN.slL+n.con*SIPN.slB;if(sl)it.push('прокалывающих зажимов SLIW 50 — '+sl+(n.lum?' (светильников '+n.lum+(n.con?', подключений '+n.con:'')+')':''));if(n.ends)it.push('колпачков — '+n.ends*SIPN.cap);
  h+=`<div style="margin:3px 0"><b>${SIPR[n.role]}</b>${n.turn!=null?' · поворот линии '+n.turn+'°':''}${n.role=='corner'?' — подвеска не держит такой угол, крепление анкерное':''}</div>`;
  h+='<div><small>Пролёты:</small> '+n.nb.map(b=>esc(b.o.id)+' — '+Math.round(b.len)+' м'+(SIPC.trunk.has(b.k)?'':' <small>(ответвл.)</small>')).join('; ')+'</div>';
  if(it.length)h+='<div style="margin-top:3px"><small>Арматура на опоре:</small> '+it.join('; ')+'</div>'}
 h+='<div class="r" style="margin-top:6px"><button data-card>Карточка опоры</button></div>';
 d.innerHTML=h;d.querySelector('[data-card]').onclick=()=>{const m=mk.get(p);L.popup(PO()).setLatLng(m?m.getLatLng():[p.lat,p.lon]).setContent(popup(p)).openOn(map)};return d}
function sipPanes(){if(map.getPane('sipP'))return;const a=map.createPane('sipP'),b=map.createPane('sipLb');a.style.zIndex=640;b.style.zIndex=645;a.style.pointerEvents='none';b.style.pointerEvents='none'}
function sipDraw(){SIPL.clearLayers();SIPLB.clearLayers();SIPRG.clearLayers();if(mode!='sip'){map.removeLayer(SIPL);map.removeLayer(SIPLB);map.removeLayer(SIPRG);return}
 sipPanes();SIPC=sipCalc();if(!map.hasLayer(SIPL))SIPL.addTo(map);if(!map.hasLayer(SIPLB))SIPLB.addTo(map);
 const col={t:'#1d4ed8',b:'#ea580c',n:'#9ca3af'};
 /* линии и кольца — поверх опор (без нажатий); невидимая широкая копия линии под опорами ловит нажатие на пролёт */
 SIPC.ED.forEach(x=>{if(!(tpOk(x.a)||tpOk(x.b)))return;const pt=sipPath(x.e);L.polyline(pt,{pane:'sipP',interactive:false,color:col[x.kind],weight:x.kind=='t'?6:x.kind=='b'?4:3,opacity:.9,dashArray:x.kind=='n'?'6 6':null,lineCap:'round'}).addTo(SIPL);
  const hit=L.polyline(pt,{color:'#000',opacity:0,weight:16}).addTo(SIPL);
  hit.on('click',ev=>{L.DomEvent.stopPropagation(ev);SPCLK=Date.now();PSEL=Date.now();L.popup({maxWidth:280}).setLatLng(ev.latlng).setContent(sipSpanPop(x)).openOn(map)})});
 sipRings();sipLabels();sipStats()}
/* кольца: анкерное крепление — красное, ответвление — фиолетовое; на мелком масштабе меньше */
function sipRings(){SIPRG.clearLayers();if(mode!='sip'||!SIPC)return;if(!map.hasLayer(SIPRG))SIPRG.addTo(map);const z=map.getZoom(),k=z>=17?1:z>=16?.75:z>=15?.5:.35;
 SIPC.ND.forEach(n=>{if(!tpOk(n.p))return;const br=n.role=='branch',c=br?'#a21caf':(n.anc>0?'#dc2626':null);if(!c)return;
  L.circleMarker([n.p.lat,n.p.lon],{pane:'sipP',radius:(br?15:13)*k,color:c,weight:Math.max(1.5,(br?4:3)*k),fill:false,interactive:false}).addTo(SIPRG)})}
function sipSoon(){if(mode!='sip')return;clearTimeout(SIPT);SIPT=setTimeout(()=>{try{sipDraw()}catch(e){console.error(e)}},150)}
map.on('zoomend',()=>{if(mode=='sip')sipRings()});map.on('zoomend moveend',()=>{if(mode=='sip')sipLabels()});
$('sipb').onclick=()=>{const t=document.querySelector('#modes [data-m="'+(mode=='sip'?'view':'sip')+'"]');if(t)t.click()};
function sipXl(){const C=SIPC||sipCalc(),o=sipSum(C),R=sipRows(o),wb=XLSX.utils.book_new(),ALL=!FTS.size,f1=x=>Math.round(x*10)/10;
 const H=['Позиция','Ед.','Основание','Кол-во основания','Норма','Итого','По РД (592 опоры)','Как считали'];
 const aoa=[H,...R.map(r=>[r[0],r[1],r[2],r[3],r[4],sipQ(r),ALL&&r[6]?SIPRD[r[6]]:'',r[5]])];
 const ws=XLSX.utils.aoa_to_sheet(aoa);R.forEach((r,i)=>{ws['F'+(i+2)]={t:'n',v:sipQ(r),f:`ROUNDUP(D${i+2}*E${i+2},0)`}});
 ws['!cols']=[{wch:44},{wch:5},{wch:32},{wch:16},{wch:8},{wch:10},{wch:16},{wch:44}];
 XLSX.utils.sheet_add_aoa(ws,[[],['Нормы в столбце «Норма» можно менять — «Итого» пересчитается.'],['Без опор, которых ещё нет на карте; без пролётов к опорам на гравитационном фундаменте, которые никуда дальше не ведут (следующий этап).']],{origin:'A'+(R.length+3)});
 XLSX.utils.book_append_sheet(wb,ws,'Арматура');
 const sp=C.ED.filter(x=>tpOk(x.a)||tpOk(x.b)).map(x=>[tpn(String(x.a.tp||'')),x.a.id,x.b.id,f1(x.len),{t:'магистраль',b:'ответвление',n:'следующий этап'}[x.kind]]).sort((a,b)=>String(a[0]).localeCompare(String(b[0]),'ru',{numeric:true})||String(a[1]).localeCompare(String(b[1]),'ru',{numeric:true}));
 const w2=XLSX.utils.aoa_to_sheet([['ТП','Опора','Опора','Длина пролёта, м','Участок'],...sp]);w2['!cols']=[{wch:16},{wch:18},{wch:18},{wch:16},{wch:16}];XLSX.utils.book_append_sheet(wb,w2,'Пролёты');
 const nd=[...C.ND.values()].filter(n=>tpOk(n.p)).sort((a,b)=>String(a.p.id).localeCompare(String(b.p.id),'ru',{numeric:true})).map(n=>[n.p.id,tpn(String(n.p.tp||'')),(n.p.t=='A'?'анкерная':'стандартная')+' '+(+n.p.h==9?9:8)+' м',SIPR[n.role],n.deg,n.turn==null?'':n.turn,n.anc,n.sus,n.lum*SIPN.slL+n.con*SIPN.slB,n.lum,n.ends*SIPN.cap,isG(n.p)?'гравит. фундамент':n.p.x?'исключена':'']);
 const w3=XLSX.utils.aoa_to_sheet([['Опора','ТП','Тип опоры','Роль на линии СИП','Пролётов','Поворот линии, °','Анкерных зажимов SO250.01 (и кронштейнов SO253)','Подвесок SO260','Прокалывающих SLIW 50','Светильников','Колпачков','Примечание'],...nd]);w3['!cols']=[{wch:18},{wch:14},{wch:18},{wch:24},{wch:9},{wch:10},{wch:18},{wch:10},{wch:12},{wch:11},{wch:10},{wch:18}];XLSX.utils.book_append_sheet(wb,w3,'Опоры на линии');
 const tps=[...o.tp.entries()].sort((a,b)=>a[0].localeCompare(b[0],'ru',{numeric:true}));
 const w4=XLSX.utils.aoa_to_sheet([['ТП','Пролётов','Длина, м','Магистраль, м','Ответвления, м','СИП с запасом 1,02, м','Опор на линии','Ответвительных опор','Анкерных креплений','Подвесок SO260'],...tps.map(([t,r])=>[tpn(t),r.sp,f1(r.len),f1(r.tr),f1(r.br),Math.ceil(r.len*SIPN.sipK),r.nd,r.brn,r.anc,r.sus])]);w4['!cols']=[{wch:16},{wch:9},{wch:10},{wch:13},{wch:14},{wch:18},{wch:12},{wch:16},{wch:16},{wch:14}];XLSX.utils.book_append_sheet(wb,w4,'По ТП');
 XLSX.writeFile(wb,'СИП_арматура_'+LD()+'.xlsx')}
$('sipx').onclick=()=>{try{sipXl()}catch(e){alert('Ошибка расчёта: '+(e.message||e))}};
