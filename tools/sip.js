/* ---- СИП-карта: как пойдёт СИП по опорам, длины пролётов, ответвления, отрезки и раскрой, расчёт арматуры ---- */
var SIPL=L.layerGroup(),SIPLB=L.layerGroup(),SIPRG=L.layerGroup(),SIPC=null,SIPT=0,SIPDO=false;
/* нормы (на что умножаем) и количества по РД (уч. 1 + уч. 2) для сверки */
var SIPN={sipK:1.02,tail:1.5,an:1,sus:1,slL:3,slP:1,ss:4,inl:1,cap:4,tape:1.5,skr:1.5,vvg:2.04,pen:1.5};
var SIPRD={sip:16998,an:197,br:197,sus:577,sliw:2314,tape:1244,skr:1244,vvg:1224};
var SIPR={root:'ввод от ТП',end:'концевая',anchor:'анкерная',corner:'угловая (поворот ≥45°)',branch:'ответвительная',mid:'промежуточная'};
var SIPK={t:'магистраль',b:'ответвление',n:'к опорам на гравитационном фундаменте — следующий этап',x:'между сетями разных ТП — нужен разрыв, уточнить',c:'замыкает кольцо — для радиальной сети лишний, уточнить',u:'не связан с вводом от ТП — уточнить'};
var SIPCOL={t:'#1d4ed8',b:'#ea580c',n:'#9ca3af',x:'#dc2626',c:'#dc2626',u:'#c026d3'};
var SIPDR=1000;try{SIPDR=+localStorage.getItem(KEY+'_sipdr')||1000}catch(e){}
function sipPath(e){return epath(e[0],e[1],e.pts)}
function sipLen(e){const pt=sipPath(e);let d=0;for(let i=1;i<pt.length;i++)d+=map.distance(pt[i-1],pt[i]);return d}
function sipMid(pt){if(pt.length==2)return[(pt[0][0]+pt[1][0])/2,(pt[0][1]+pt[1][1])/2];let t=0;const s=[];for(let i=1;i<pt.length;i++){const d=map.distance(pt[i-1],pt[i]);s.push(d);t+=d}let h=t/2;for(let i=0;i<s.length;i++){if(h<=s[i]){const f=s[i]?h/s[i]:0;return[pt[i][0]+(pt[i+1][0]-pt[i][0])*f,pt[i][1]+(pt[i+1][1]-pt[i][1])*f]}h-=s[i]}return pt[pt.length-1]}
function sipCalc(){
 const N=NETC||netEdges(),U=new Map(P.map(p=>[p.uid,p])),isC=p=>!p.x&&!isG(p),kk=(a,b)=>a<b?a+'|'+b:b+'|'+a;
 const adj=new Map(),ad=(a,b,e)=>{if(!adj.has(a.uid))adj.set(a.uid,[]);adj.get(a.uid).push({o:b,e})};
 N.E.forEach(e=>{ad(e[0],e[1],e);ad(e[1],e[0],e)});
 const LEN=new Map();N.E.forEach(e=>LEN.set(kk(e[0].uid,e[1].uid),sipLen(e)));
 const roots=new Set();CABS.forEach(z=>{if(z.p&&adj.has(z.p.uid))roots.add(z.p.uid)});
 /* тупиковые отрезки, ведущие только к опорам не по контракту (гравитационный фундамент, исключённые) — следующий этап */
 const A=new Map([...adj].map(([k,v])=>[k,v.slice()]));let ch=true;
 while(ch){ch=false;for(const [u,l] of [...A]){const p=U.get(u);if(l.length<=1&&!isC(p)&&!roots.has(u)){l.forEach(x=>{const o=A.get(x.o.uid);if(o)A.set(x.o.uid,o.filter(y=>y.o.uid!=u))});A.delete(u);ch=true}}}
 const keep=new Set();A.forEach((l,u)=>l.forEach(x=>keep.add(kk(u,x.o.uid))));
 /* каждую опору — к ближайшему (по числу пролётов) вводу от ТП: получаем отдельные сети ТП без колец */
 const own=new Map(),par=new Map(),order=[],nofeed=new Set();let q=[];
 const bfs=()=>{while(q.length){const u=q.shift();order.push(u);A.get(u).forEach(x=>{const v=x.o.uid;if(own.has(v))return;own.set(v,own.get(u));par.set(v,u);q.push(v)})}};
 roots.forEach(r=>{if(A.has(r)){own.set(r,r);par.set(r,null);q.push(r)}});bfs();
 [...A.keys()].forEach(u=>{if(own.has(u))return;const comp=[],st=[u],sn=new Set([u]);while(st.length){const v=st.pop();comp.push(v);A.get(v).forEach(x=>{if(!sn.has(x.o.uid)){sn.add(x.o.uid);st.push(x.o.uid)}})}
  comp.forEach(v=>nofeed.add(v));const s=comp.find(v=>A.get(v).length==1)||u;own.set(s,s);par.set(s,null);q=[s];bfs()});
 const kids=new Map(order.map(u=>[u,[]]));order.forEach(u=>{const p=par.get(u);if(p!=null)kids.get(p).push(u)});
 const plen=u=>LEN.get(kk(u,par.get(u)));
 const dep=new Map();for(let i=order.length-1;i>=0;i--){const u=order[i];let m=0;kids.get(u).forEach(v=>m=Math.max(m,plen(v)+dep.get(v)));dep.set(u,m)}
 const tree=new Set();order.forEach(u=>{if(par.get(u)!=null)tree.add(kk(u,par.get(u)))});
 /* магистраль: от ввода до самой дальней опоры своей сети; остальное — ответвления */
 const dist=new Map();order.forEach(u=>{const p=par.get(u);dist.set(u,p==null?0:dist.get(p)+plen(u))});
 const far=new Map();order.forEach(u=>{const r=own.get(u);if(!far.has(r)||dist.get(u)>dist.get(far.get(r)))far.set(r,u)});
 const trunk=new Set();far.forEach(v=>{for(let x=v;par.get(x)!=null;x=par.get(x))trunk.add(kk(x,par.get(x)))});
 const ED=N.E.map(e=>{const k=kk(e[0].uid,e[1].uid);let kind;if(!keep.has(k))kind='n';else if(tree.has(k))kind=nofeed.has(e[0].uid)?'u':(trunk.has(k)?'t':'b');else kind=own.get(e[0].uid)!==own.get(e[1].uid)?'x':'c';return{e,a:e[0],b:e[1],len:LEN.get(k),k,kind}});
 /* опоры */
 const ND=new Map();
 order.forEach(u=>{const p=U.get(u);ND.set(u,{p,deg:(par.get(u)!=null?1:0)+kids.get(u).length,root:roots.has(u)&&par.get(u)==null,nofeed:nofeed.has(u),net:own.get(u),anc:0,sus:0,ends:0,brs:0,inl:0,turn:null,role:'',lum:isC(p)?((+p.kr||0)==2?2:(+p.kr||0)==1?1:0):0,bond:isC(p)?1:0,nb:[]})});
 order.forEach(u=>{const p=par.get(u);if(p!=null){const l=plen(u),k=kk(u,p);ND.get(u).nb.push({o:U.get(p),len:l,k});ND.get(p).nb.push({o:U.get(u),len:l,k})}});
 ED.forEach(x=>{if(x.kind=='x'||x.kind=='c'){[[x.a,x.b],[x.b,x.a]].forEach(([s,o])=>{const n=ND.get(s.uid);if(n)n.nb.push({o,len:x.len,k:x.k,kind:x.kind})})}});
 /* отрезки СИП: идём по самой длинной ветке, остальные ветки — новые отрезки (ответвления);
    на опоре ввода СИП в каждую сторону анкерится отдельно: кабель от ТП подключается к первому отрезку, остальные — проколом СИП–СИП */
 const eOf=(u,v)=>{const x=A.get(u).find(y=>y.o.uid==v);return x?x.e:null};
 const dirTo=(p,o,e)=>{let t=o;const pts=e&&e.pts;if(pts&&pts.length){const s=e[0].uid==p.uid?pts[0]:pts[pts.length-1];t={lat:s[0],lon:s[1]}}return Math.atan2((t.lat-p.lat)*K2,(t.lon-p.lon)*K1)};
 const turnAt=(u,a,b)=>{const p=U.get(u);let d=Math.abs(dirTo(p,U.get(a),eOf(u,a))-dirTo(p,U.get(b),eOf(u,b)))*180/Math.PI;if(d>180)d=360-d;return Math.round(180-d)};
 const byDep=u=>kids.get(u).slice().sort((x,y)=>(plen(y)+dep.get(y))-(plen(x)+dep.get(x)));
 const pend=[],PCS=[];
 const run=(start,first)=>{const nodes=[start];let cur=first,len=plen(first);while(true){nodes.push(cur);const c=byDep(cur);if(!c.length)break;c.slice(1).forEach(v=>{ND.get(cur).brs++;pend.push([cur,v])});cur=c[0];len+=plen(cur)}return{nodes,len}};
 order.filter(u=>par.get(u)==null).forEach(r=>{const c=byDep(r);if(!c.length)return;const rt=roots.has(r);
  if(rt){PCS.push(run(r,c[0]));c.slice(1).forEach(v=>{ND.get(r).brs++;pend.push([r,v])})}
  else{const p1=run(r,c[0]);let pc=p1;if(c.length>=2){const p2=run(r,c[1]);pc={nodes:p2.nodes.slice().reverse().concat(p1.nodes.slice(1)),len:p1.len+p2.len}}c.slice(2).forEach(v=>{ND.get(r).brs++;pend.push([r,v])});PCS.push(pc)}
  while(pend.length){const[a,v]=pend.pop();PCS.push(run(a,v))}});
 PCS.forEach(pc=>{const n=pc.nodes;pc.a=U.get(n[0]);pc.b=U.get(n[n.length-1]);pc.spans=n.length-1;pc.nofeed=nofeed.has(n[0]);
  [n[0],n[n.length-1]].forEach(u=>{const d=ND.get(u);d.ends++;d.anc++});
  for(let i=1;i<n.length-1;i++){const d=ND.get(n[i]),t=turnAt(n[i],n[i-1],n[i+1]);d.turn=t;if(d.p.t=='A'||t>=45){d.anc+=2;d.ia=true}else{d.sus++;d.ia=false}}});
 ND.forEach(d=>{if(d.root)d.inl=1;d.role=d.root?'root':d.deg>=3?'branch':d.deg<=1?'end':d.ia?(d.p.t=='A'?'anchor':'corner'):'mid'});
 return{ED,ND,PCS,U}}
function sipCut(pcs,drum){const it=[];pcs.forEach(pc=>{const need=pc.len*SIPN.sipK+2*SIPN.tail;if(need<=drum)it.push({pc,need,part:1,parts:1});else{const k=Math.ceil(need/drum);for(let i=1;i<=k;i++)it.push({pc,need:need/k,part:i,parts:k})}});
 it.sort((a,b)=>b.need-a.need);const bins=[];it.forEach(x=>{let b=bins.find(b=>b.free>=x.need-1e-6);if(!b){b={free:drum,items:[]};bins.push(b)}b.items.push(x);b.free-=x.need});
 return{bins,joints:it.filter(x=>x.part>1).length,waste:bins.reduce((a,b)=>a+b.free,0),items:it}}
function sipSum(C){const Nn=[...C.ND.values()].filter(n=>tpOk(n.p)),s=f=>Nn.reduce((a,n)=>a+f(n),0);
 const E=C.ED.filter(x=>(x.kind=='t'||x.kind=='b'||x.kind=='u')&&(tpOk(x.a)||tpOk(x.b)));
 const o={len:E.reduce((a,x)=>a+x.len,0),spans:E.length,nodes:Nn.length,anc:s(n=>n.anc),sus:s(n=>n.sus),ends:s(n=>n.ends),brs:s(n=>n.brs),inl:s(n=>n.inl),lum:s(n=>n.lum),bond:s(n=>n.bond),r:{},tp:new Map()};
 Object.keys(SIPR).forEach(k=>o.r[k]=Nn.filter(n=>n.role==k).length);
 o.pcs=C.PCS.filter(pc=>tpOk(pc.a));o.cut=sipCut(o.pcs,SIPDR);
 const nx=C.ED.filter(x=>x.kind=='n'&&(tpOk(x.a)||tpOk(x.b)));o.nextN=nx.length;o.nextL=nx.reduce((a,x)=>a+x.len,0);
 o.xs=C.ED.filter(x=>(x.kind=='x'||x.kind=='c')&&(tpOk(x.a)||tpOk(x.b)));
 const nfc=new Map();Nn.filter(n=>n.nofeed).forEach(n=>{if(!nfc.has(n.net))nfc.set(n.net,[]);nfc.get(n.net).push(n.p)});o.nf=[...nfc.values()];
 const T=t=>{t=String(t||'—');if(!o.tp.has(t))o.tp.set(t,{sp:0,len:0,br:0,brs:0,anc:0,sus:0,nd:0,pcs:0});return o.tp.get(t)};
 E.forEach(x=>{const r=T(x.a.tp);r.sp++;r.len+=x.len;if(x.kind!='t')r.br+=x.len});
 Nn.forEach(n=>{const r=T(n.p.tp);r.nd++;r.anc+=n.anc;r.sus+=n.sus;r.brs+=n.brs});o.pcs.forEach(pc=>T(pc.a.tp).pcs++);
 return o}
function sipRows(o){const n=SIPN,pr=o.lum*n.slL+o.bond*n.slP+o.brs*n.ss+o.inl*n.inl;return[
 ['СИП-4 4×25','м','длина пролётов по карте, м',Math.round(o.len),n.sipK,'длина × 1,02 на провис','sip'],
 ['Зажим анкерный для СИП-4 4×25 (в РД — SO250.01)','шт','анкерных креплений',o.anc,n.an,'по 1 на каждый конец отрезка СИП и по 2 на анкерную или угловую опору в линии','an'],
 ['Кронштейн анкерный SO253','шт','анкерных креплений',o.anc,n.an,'по 1 на анкерный зажим','br'],
 ['Зажим поддерживающий для СИП-4 4×25 (в РД — SO260)','шт','промежуточных опор',o.sus,n.sus,'по 1 на промежуточную опору','sus'],
 ['Зажим прокалывающий SLIW 50 — светильники','шт','светильников',o.lum,n.slL,'по 3 на светильник: фаза, N и PE на PEN','sliw'],
 ['Зажим прокалывающий SLIW 50 — опора к PEN','шт','опор контракта на линии',o.bond,n.slP,'по 1 на опору',''],
 ['Зажим прокалывающий СИП–СИП (ответвление до 25 мм²)','шт','ответвлений СИП',o.brs,n.ss,'по 4 на ответвление: 4 жилы. SLIW 50 не подходит — у него ответвление 1,5–10 мм²',''],
 ['Муфта переходная бронекабель — СИП (ввод от ТП)','шт','вводов от ТП',o.inl,n.inl,'по 1 на ввод: кабель от ТП соединяется с СИП в муфте на опоре ввода; N и PE кабеля — на PEN (нулевую несущую) СИП',''],
 ['Колпачок изолирующий','шт','концов отрезков СИП',o.ends,n.cap,'по 4 на конец: 4 жилы',''],
 ['Гильза соединительная изолированная (стык по длине)','шт','стыков при барабанах по '+SIPDR+' м',o.cut.joints,4,'по 4 на стык: 4 жилы; стык — в шлейфе на анкерной опоре',''],
 ['Ремешок (стяжка) для СИП','шт','креплений и проколов',2*o.sus+o.anc+pr,1,'2 у подвески, 1 у анкерного зажима, 1 у каждого прокола',''],
 ['Лента бандажная СОТ 37','м','анкерных и поддерживающих кронштейнов',o.anc+o.sus,n.tape,'1,5 м на кронштейн','tape'],
 ['Скрепа СОТ 36','шт','анкерных и поддерживающих кронштейнов',o.anc+o.sus,n.skr,'1,5 шт. на кронштейн','skr'],
 ['Провод ВВГнг(А)-LS 3×1,5','м','светильников',o.lum,n.vvg,'2 м на светильник × 1,02','vvg'],
 ['Провод перемычки PEN — опора (марку уточнить)','м','опор контракта на линии',o.bond,n.pen,'1,5 м на опору','']]}
function sipQ(r){return Math.ceil(r[3]*r[4]-1e-9)}
function sipZ(a,b){return [a.lat,a.lon,b.lat,b.lon].map(v=>v.toFixed(6)).join(',')}
function sipWarn(o){const w=[],f=x=>Math.round(x);
 o.xs.forEach(x=>{const na=SIPC.ND.get(x.a.uid),nb=SIPC.ND.get(x.b.uid),ra=na&&SIPC.U.get(na.net),rb=nb&&SIPC.U.get(nb.net);
  w.push([x.kind=='x'?`Сети ${esc(tpn(String(ra?ra.tp:x.a.tp)))} и ${esc(tpn(String(rb?rb.tp:x.b.tp)))} сомкнуты: пролёт ${esc(x.a.id)} — ${esc(x.b.id)} (${f(x.len)} м). Нужен разрыв — где?`:`Кольцо в сети ${esc(tpn(String(x.a.tp)))}: пролёт ${esc(x.a.id)} — ${esc(x.b.id)} (${f(x.len)} м).`,sipZ(x.a,x.b)])});
 o.nf.forEach(g=>{const la=g.map(p=>p.lat),lo=g.map(p=>p.lon),ids=g.map(p=>p.id).sort((a,b)=>a.localeCompare(b,'ru',{numeric:true}));
  w.push([`${g.length} опор не связаны с вводом от ТП: ${esc(ids.slice(0,6).join(', '))}${ids.length>6?' и ещё '+(ids.length-6):''}. Не нарисован пролёт или нужен второй ввод?`,[Math.min(...la),Math.min(...lo),Math.max(...la),Math.max(...lo)].map(v=>v.toFixed(6)).join(',')])});
 return w}
function sipStats(){const e=$('sips');if(!e||$('sipp').hidden||!SIPC)return;const o=sipSum(SIPC),f=x=>Math.round(x).toLocaleString('ru'),ALL=!FTS.size,
 miss=ALL?Math.max(0,592-P.filter(p=>!p.x&&!isG(p)).length):0,avg=o.spans?o.len/o.spans:0,R=sipRows(o),c=o.cut,lp=o.pcs.reduce((a,p)=>Math.max(a,p.len),0);
 let h=`<div>Пролётов <b>${o.spans}</b> · <b>${f(o.len)}</b> м по карте · средний пролёт ${f(avg)} м</div>`;
 if(miss)h+=`<div>Ещё ${miss} опор контракта нет на карте: ≈ ${f(miss*avg)} м СИП</div>`;
 h+=`<div>Отрезков СИП без соединений: <b>${o.pcs.length}</b>, самый длинный ${f(lp)} м. На барабанах по ${SIPDR} м: барабанов <b>${c.bins.length}</b>, стыков <b>${c.joints}</b>, в остатках ${f(c.waste)} м.</div>`;
 h+=`<div>Опор на линии <b>${o.nodes}</b>: ввод от ТП ${o.r.root}, концевых ${o.r.end}, анкерных ${o.r.anchor}, угловых ${o.r.corner}, ответвительных ${o.r.branch}, промежуточных ${o.r.mid}</div>`;
 if(o.nextN)h+=`<div style="opacity:.75">В расчёт не входят ${o.nextN} пролётов, ${f(o.nextL)} м: они ведут только к опорам на гравитационном фундаменте (следующий этап).</div>`;
 const W=sipWarn(o);if(W.length)h+='<div class="sipw"><b>Требует решения</b>'+W.map(x=>`<a href="#" data-z="${x[1]}">${x[0]}</a>`).join('')+(o.xs.length?'<small>Эти пролёты в длину СИП не включены.</small>':'')+'</div>';
 h+='<table id="sipt"><tr><th>Арматура и провод</th><th>По карте</th><th>'+(ALL?'По РД':'')+'</th></tr>';
 const sl=sipQ(R[4])+sipQ(R[5]);
 R.forEach((r,i)=>{if(i==5)return;if(i==9&&!c.joints)return;const q=i==4?sl:sipQ(r),rd=!ALL?'':r[6]?f(SIPRD[r[6]]):'—';
  h+=`<tr><td>${esc(i==4?'Зажим прокалывающий SLIW 50':r[0])}<small>${esc(i==4?'3 на светильник (фаза, N и PE на PEN) + 1 на опору к PEN':r[5])}</small></td><td>${f(q)}${r[1]=='м'?' м':''}</td><td>${rd}</td></tr>`});
 h+='</table>';
 h+=`<small style="display:block;opacity:.75">${miss?'Без '+miss+' опор, которых нет на карте. ':''}По РД — спецификации участков 1 и 2 на 592 опоры; «—» — в РД нет. Анкерные SO250.01 и подвески SO260 в РД рассчитаны на несущую нулевую жилу, а у СИП-4 4×25 её нет: зажимы нужны на 4-жильный жгут — уточнить у проектировщика или поставщика.</small>`;
 const tps=[...o.tp.entries()].sort((a,b)=>a[0].localeCompare(b[0],'ru',{numeric:true}));
 h+='<details id="sipd"'+(SIPDO?' open':'')+'><summary>По ТП</summary><table id="siptp"><tr><th>ТП</th><th>пролётов</th><th>м</th><th>из них ответвл., м</th><th>отрезков</th><th>ответвл.</th><th>анкер. крепл.</th><th>подвесок</th></tr>'+tps.map(([t,r])=>`<tr><td>${esc(tpn(t))}</td><td>${r.sp}</td><td>${f(r.len)}</td><td>${f(r.br)}</td><td>${r.pcs}</td><td>${r.brs}</td><td>${r.anc}</td><td>${r.sus}</td></tr>`).join('')+'</table></details>';
 e.innerHTML=h;const d=$('sipd');if(d)d.ontoggle=()=>{SIPDO=d.open};
 e.querySelectorAll('[data-z]').forEach(a=>a.onclick=ev=>{ev.preventDefault();const z=a.dataset.z.split(',').map(Number);map.fitBounds([[z[0],z[1]],[z[2],z[3]]],{padding:[60,60],maxZoom:18})});
 const sd=$('sipdr');if(sd)sd.value=String(SIPDR)}
function sipLabels(){SIPLB.clearLayers();if(mode!='sip'||!SIPC||map.getZoom()<17)return;const b=map.getBounds().pad(.2);
 SIPC.ED.forEach(x=>{if(!(tpOk(x.a)||tpOk(x.b)))return;const m=sipMid(sipPath(x.e));if(!b.contains(m))return;const ex=x.kind=='x'?' · разрыв?':x.kind=='c'?' · кольцо':'';
  L.marker(m,{pane:'sipLb',icon:L.divIcon({className:'',html:'<div class="sipl'+(x.kind=='n'?' n':x.kind=='x'||x.kind=='c'?' w':'')+'">'+Math.round(x.len)+' м'+ex+'</div>',iconSize:[0,0]}),interactive:false,keyboard:false}).addTo(SIPLB)})}
function sipSpanPop(x){return `<div class="pp"><b>${esc(x.a.id)} — ${esc(x.b.id)}</b><div>Пролёт ≈ <b>${Math.round(x.len)} м</b> (СИП с запасом ≈ ${Math.ceil(x.len*SIPN.sipK)} м)</div><small>${SIPK[x.kind]}</small></div>`}
function sipPop(p){const d=document.createElement('div');d.className='pp';const n=SIPC&&SIPC.ND.get(p.uid);
 let h=`<div><b>${esc(p.id)}</b> <small>${p.t=='A'?'анкерная':'стандартная'} ${+p.h==9?9:8} м</small></div>`;
 if(!n)h+='<div style="margin:4px 0">Опора не на линии СИП'+(SIPC&&SIPC.ED.some(x=>x.kind=='n'&&(x.a===p||x.b===p))?' этого этапа (тупиковый отрезок к опорам на гравитационном фундаменте)':'')+'.</div>';
 else{const it=[],sl=n.lum*SIPN.slL+n.bond*SIPN.slP;
  if(n.anc)it.push('анкерных зажимов и кронштейнов SO253 — по '+n.anc);if(n.sus)it.push('поддерживающий зажим — 1');
  if(sl)it.push('SLIW 50 — '+sl+(n.lum?' ('+n.lum+' светильн. × 3'+(n.bond?' + 1 опора к PEN':'')+')':''));
  if(n.brs)it.push('прокалывающих СИП–СИП — '+n.brs*SIPN.ss+' ('+n.brs+' ответвл.)');if(n.inl)it.push('муфта переходная бронекабель — СИП — '+SIPN.inl);if(n.ends)it.push('колпачков — '+n.ends*SIPN.cap);
  h+=`<div style="margin:3px 0"><b>${SIPR[n.role]}</b>${n.turn!=null&&n.role!='end'?' · поворот линии '+n.turn+'°':''}${n.role=='corner'?' — поддерживающий зажим такой угол не держит, крепление анкерное':''}</div>`;
  if(n.nofeed)h+='<div style="color:#e879f9">Не связана с вводом от ТП — уточнить, откуда питание.</div>';
  h+='<div><small>Пролёты:</small> '+n.nb.map(b=>esc(b.o.id)+' — '+Math.round(b.len)+' м'+(b.kind=='x'?' <small>(между сетями ТП)</small>':b.kind=='c'?' <small>(кольцо)</small>':'')).join('; ')+'</div>';
  if(it.length)h+='<div style="margin-top:3px"><small>Арматура на опоре:</small> '+it.join('; ')+'</div>'}
 h+='<div class="r" style="margin-top:6px"><button data-card>Карточка опоры</button></div>';
 d.innerHTML=h;d.querySelector('[data-card]').onclick=()=>{const m=mk.get(p);L.popup(PO()).setLatLng(m?m.getLatLng():[p.lat,p.lon]).setContent(popup(p)).openOn(map)};return d}
function sipPanes(){if(map.getPane('sipP'))return;const a=map.createPane('sipP'),b=map.createPane('sipLb');a.style.zIndex=640;b.style.zIndex=645;a.style.pointerEvents='none';b.style.pointerEvents='none'}
function sipDraw(){SIPL.clearLayers();SIPLB.clearLayers();SIPRG.clearLayers();if(mode!='sip'){map.removeLayer(SIPL);map.removeLayer(SIPLB);map.removeLayer(SIPRG);return}
 sipPanes();SIPC=sipCalc();if(!map.hasLayer(SIPL))SIPL.addTo(map);if(!map.hasLayer(SIPLB))SIPLB.addTo(map);
 /* линии и кольца — поверх опор (без нажатий); невидимая широкая копия линии под опорами ловит нажатие на пролёт */
 SIPC.ED.forEach(x=>{if(!(tpOk(x.a)||tpOk(x.b)))return;const pt=sipPath(x.e),k=x.kind,w=k=='t'?6:k=='b'||k=='u'?4:k=='x'||k=='c'?5:3;
  L.polyline(pt,{pane:'sipP',interactive:false,color:SIPCOL[k],weight:w,opacity:.9,dashArray:k=='n'?'6 6':k=='x'||k=='c'?'9 6':null,lineCap:'round'}).addTo(SIPL);
  const hit=L.polyline(pt,{color:'#000',opacity:0,weight:16}).addTo(SIPL);
  hit.on('click',ev=>{L.DomEvent.stopPropagation(ev);SPCLK=Date.now();PSEL=Date.now();L.popup({maxWidth:280}).setLatLng(ev.latlng).setContent(sipSpanPop(x)).openOn(map)})});
 sipRings();sipLabels();sipStats()}
/* кольца: анкерное крепление — красное, ответвление — фиолетовое; на мелком масштабе меньше */
function sipRings(){SIPRG.clearLayers();if(mode!='sip'||!SIPC)return;if(!map.hasLayer(SIPRG))SIPRG.addTo(map);const z=map.getZoom(),k=z>=17?1:z>=16?.75:z>=15?.5:.35;
 SIPC.ND.forEach(n=>{if(!tpOk(n.p))return;const br=n.role=='branch'||n.brs>0,c=br?'#a21caf':(n.anc>0?'#dc2626':null);if(!c)return;
  L.circleMarker([n.p.lat,n.p.lon],{pane:'sipP',radius:(br?15:13)*k,color:c,weight:Math.max(1.5,(br?4:3)*k),fill:false,interactive:false}).addTo(SIPRG)})}
function sipSoon(){if(mode!='sip')return;clearTimeout(SIPT);SIPT=setTimeout(()=>{try{sipDraw()}catch(e){console.error(e)}},150)}
map.on('zoomend',()=>{if(mode=='sip')sipRings()});map.on('zoomend moveend',()=>{if(mode=='sip')sipLabels()});
$('sipb').onclick=()=>{const t=document.querySelector('#modes [data-m="'+(mode=='sip'?'view':'sip')+'"]');if(t)t.click()};
$('sipdr').onchange=e=>{SIPDR=+e.target.value||1000;try{localStorage.setItem(KEY+'_sipdr',String(SIPDR))}catch(er){}sipStats()};
function sipXl(){const C=SIPC||sipCalc(),o=sipSum(C),R=sipRows(o),wb=XLSX.utils.book_new(),ALL=!FTS.size,f1=x=>Math.round(x*10)/10,ru=(a,b)=>String(a).localeCompare(String(b),'ru',{numeric:true});
 const H=['Позиция','Ед.','Основание','Кол-во основания','Норма','Итого','По РД (592 опоры)','Как считали'];
 const ws=XLSX.utils.aoa_to_sheet([H,...R.map(r=>[r[0],r[1],r[2],r[3],r[4],sipQ(r),ALL?(r[6]?SIPRD[r[6]]:'нет в РД'):'',r[5]])]);
 R.forEach((r,i)=>{ws['F'+(i+2)]={t:'n',v:sipQ(r),f:`ROUNDUP(D${i+2}*E${i+2},0)`}});
 ws['!cols']=[{wch:50},{wch:5},{wch:34},{wch:16},{wch:8},{wch:10},{wch:16},{wch:60}];
 XLSX.utils.sheet_add_aoa(ws,[[],['Нормы в столбце «Норма» можно менять — «Итого» пересчитается.'],['Без опор, которых ещё нет на карте, и без пролётов к опорам на гравитационном фундаменте, которые никуда дальше не ведут (следующий этап).'],['В РД SO250.01 и SO260 — арматура под несущую нулевую жилу; у СИП-4 4×25 её нет, нужны зажимы на 4-жильный жгут — уточнить у проектировщика или поставщика.']],{origin:'A'+(R.length+3)});
 XLSX.utils.book_append_sheet(wb,ws,'Арматура');
 const pcs=o.pcs.slice().sort((a,b)=>ru(a.a.tp,b.a.tp)||b.len-a.len);
 const w1=XLSX.utils.aoa_to_sheet([['№','ТП','От опоры','До опоры','Пролётов','Длина, м','С запасом (×1,02 + 2×1,5 м), м','Примечание'],...pcs.map((pc,i)=>[i+1,tpn(String(pc.a.tp||'')),pc.a.id,pc.b.id,pc.spans,f1(pc.len),Math.ceil(pc.len*SIPN.sipK+2*SIPN.tail),pc.nofeed?'не связан с вводом от ТП':''])]);
 w1['!cols']=[{wch:5},{wch:16},{wch:18},{wch:18},{wch:9},{wch:10},{wch:24},{wch:24}];XLSX.utils.book_append_sheet(wb,w1,'Отрезки СИП');
 const cr=[['Барабан','ТП','От опоры','До опоры','Часть','Отрезать, м','Остаток на барабане, м']];
 o.cut.bins.forEach((b,i)=>b.items.forEach((x,j)=>cr.push([i+1,tpn(String(x.pc.a.tp||'')),x.pc.a.id,x.pc.b.id,x.parts>1?x.part+' из '+x.parts:'',Math.ceil(x.need),j==b.items.length-1?Math.floor(b.free):''])));
 const w5=XLSX.utils.aoa_to_sheet([['Раскрой на барабаны по '+SIPDR+' м: барабанов '+o.cut.bins.length+', стыков '+o.cut.joints+', в остатках '+Math.round(o.cut.waste)+' м'],[],...cr]);w5['!cols']=[{wch:9},{wch:16},{wch:18},{wch:18},{wch:9},{wch:12},{wch:20}];XLSX.utils.book_append_sheet(wb,w5,'Раскрой');
 const sp=C.ED.filter(x=>tpOk(x.a)||tpOk(x.b)).map(x=>[tpn(String(x.a.tp||'')),x.a.id,x.b.id,f1(x.len),SIPK[x.kind]]).sort((a,b)=>ru(a[0],b[0])||ru(a[1],b[1]));
 const w2=XLSX.utils.aoa_to_sheet([['ТП','Опора','Опора','Длина пролёта, м','Участок'],...sp]);w2['!cols']=[{wch:16},{wch:18},{wch:18},{wch:16},{wch:50}];XLSX.utils.book_append_sheet(wb,w2,'Пролёты');
 const nd=[...C.ND.values()].filter(n=>tpOk(n.p)).sort((a,b)=>ru(a.p.id,b.p.id)).map(n=>[n.p.id,tpn(String(n.p.tp||'')),(n.p.t=='A'?'анкерная':'стандартная')+' '+(+n.p.h==9?9:8)+' м',SIPR[n.role],n.deg,n.turn==null?'':n.turn,n.anc,n.sus,n.lum,n.lum*SIPN.slL+n.bond*SIPN.slP,n.brs*SIPN.ss,n.inl*SIPN.inl,n.ends*SIPN.cap,isG(n.p)?'гравит. фундамент':n.p.x?'исключена':n.nofeed?'не связана с вводом от ТП':'']);
 const w3=XLSX.utils.aoa_to_sheet([['Опора','ТП','Тип опоры','Роль на линии СИП','Пролётов','Поворот линии, °','Анкерных зажимов','Поддерживающих зажимов','Светильников','SLIW 50','Проколов СИП–СИП','Муфт на вводе','Колпачков','Примечание'],...nd]);
 w3['!cols']=[{wch:18},{wch:14},{wch:18},{wch:22},{wch:9},{wch:10},{wch:10},{wch:12},{wch:11},{wch:9},{wch:12},{wch:10},{wch:10},{wch:22}];XLSX.utils.book_append_sheet(wb,w3,'Опоры на линии');
 const tps=[...o.tp.entries()].sort((a,b)=>ru(a[0],b[0]));
 const w4=XLSX.utils.aoa_to_sheet([['ТП','Пролётов','Длина, м','Ответвления, м','СИП с запасом 1,02, м','Отрезков СИП','Ответвлений','Опор на линии','Анкерных креплений','Поддерживающих зажимов'],...tps.map(([t,r])=>[tpn(t),r.sp,f1(r.len),f1(r.br),Math.ceil(r.len*SIPN.sipK),r.pcs,r.brs,r.nd,r.anc,r.sus])]);
 w4['!cols']=[{wch:16},{wch:9},{wch:10},{wch:14},{wch:18},{wch:12},{wch:11},{wch:12},{wch:16},{wch:18}];XLSX.utils.book_append_sheet(wb,w4,'По ТП');
 const W=sipWarn(o);if(W.length){const w6=XLSX.utils.aoa_to_sheet([['Требует решения'],...W.map(x=>[x[0].replace(/&quot;/g,'"').replace(/&lt;/g,'<').replace(/&gt;/g,'>').replace(/&amp;/g,'&')])]);w6['!cols']=[{wch:110}];XLSX.utils.book_append_sheet(wb,w6,'Требует решения')}
 XLSX.writeFile(wb,'СИП_арматура_'+LD()+'.xlsx')}
$('sipx').onclick=()=>{try{sipXl()}catch(e){alert('Ошибка расчёта: '+(e.message||e))}};
