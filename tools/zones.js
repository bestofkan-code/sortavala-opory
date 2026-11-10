/* ---- участки работ: BEGIN ---- */
/* Страница uchastki.html: выделяем опоры участка (нажатием или обводом), даты и время работ, что нужно
   (освободить места у опор, отключение ВЛ 0,4 кВ, автовышка на проезжей части) → архив: схема участка (PDF)
   и письма в пресс-службу (с объявлением для жителей), в Россети, в ГИБДД (DOCX). Таблица work_zones. */
var ZN=new Map(),ZNS=new Set(),ZNE=null,ZNA=false,ZNPTS=[],ZNLY=L.layerGroup().addTo(map),ZNSRV=null;
const ZNW=[[1,'бурение котлованов и установка фундаментов опор'],[4,'установка опор освещения'],[12,'монтаж кронштейнов и светильников'],[5,'монтаж самонесущего провода (СИП)'],[20,'перенос проводов совместной подвески на новые опоры'],[21,'демонтаж старых опор'],[11,'устройство повторного заземления']];
const ZND={org:'ООО «БИК»',orgDet:'',signPos:'Генеральный директор',signName:'Е.К. Сек',exec:'',contract:'договор подряда № КАР/00230/26 от 08.09.2026',
 customer:'Карельский филиал ПАО «Россети Северо-Запад»',customerGen:'Карельского филиала ПАО «Россети Северо-Запад»',obj:'«Модернизация (капитальный ремонт) уличного освещения г. Сортавала (1 этап)»',
 press:'В пресс-службу\nАдминистрации Сортавальского муниципального округа\n(уточнить адресата)',
 ros:'Первому заместителю директора —\nглавному инженеру\nКарельского филиала ПАО «Россети Северо-Запад»\nО.А. Козлову',
 gibdd:'Начальнику отделения Госавтоинспекции\nОМВД России по Сортавальскому району\n(уточнить адресата)',
 tech:'автогидроподъёмник (автовышка) АГП-17Т',r:10};
var ZNC=Object.assign({},ZND);try{Object.assign(ZNC,JSON.parse(localStorage.getItem(KEY+'_znc')||'{}'))}catch(e){}
try{(JSON.parse(localStorage.getItem(KEY+'_zn')||'[]')||[]).forEach(r=>ZN.set(r.id,r))}catch(e){}
function znSave(){try{localStorage.setItem(KEY+'_zn',JSON.stringify([...ZN.values()]))}catch(e){}}
const znM=['января','февраля','марта','апреля','мая','июня','июля','августа','сентября','октября','ноября','декабря'];
function znDay(v){return v?(+v.slice(8,10))+' '+znM[+v.slice(5,7)-1]+' '+v.slice(0,4)+' г.':''}
function znPer(z){const a=z.d1,b=z.d2||z.d1;if(!a)return '';if(a==b)return znDay(a);if(a.slice(0,7)==b.slice(0,7))return 'с '+(+a.slice(8,10))+' по '+znDay(b);if(a.slice(0,4)==b.slice(0,4))return 'с '+(+a.slice(8,10))+' '+znM[+a.slice(5,7)-1]+' по '+znDay(b);return 'с '+znDay(a)+' по '+znDay(b)}
function znPerS(z){const a=z.d1,b=z.d2||z.d1;return a?(a==b?rd(a):rd(a).slice(0,5)+'–'+rd(b)):''}
function znTime(z){return z.t1||z.t2?'с '+(z.t1||'8:00')+' до '+(z.t2||'18:00'):''}
function znPoles(z){const U=new Set(z.uids||[]);return P.filter(p=>U.has(p.uid)&&p.lat&&p.lon)}
function znWN(z){return (z.works||[]).map(k=>(ZNW.find(w=>w[0]==k)||[0,''])[1]).filter(Boolean)}
const znRu=(a,b)=>String(a).localeCompare(String(b),'ru',{numeric:true});
function znTps(L2){return [...new Set(L2.map(p=>String(p.tp||'')).filter(Boolean))].sort(znRu)}
async function znStreets(L2){let RD=null;try{RD=await sqRoads()}catch(e){}const m=new Map();L2.forEach(p=>{let s='';try{s=sqStreet(p,RD)||''}catch(e){}if(/не определ/i.test(s))s='';p._zst=s;if(s)m.set(s,(m.get(s)||0)+1)});return [...m].sort((a,b)=>b[1]-a[1]).map(x=>x[0])}
/* ---- рисование на карте ---- */
function znDraw(){if(typeof ZNLY=='undefined')return;ZNLY.clearLayers();if(mode!='zone')return;const U=new Map();[...ZN.values()].filter(z=>!z.done).forEach(z=>(z.uids||[]).forEach(u=>{if(!U.has(u))U.set(u,z)}));
 P.forEach(p=>{const inS=ZNS.has(p.uid),z=U.get(p.uid);if(!inS&&!z)return;L.circleMarker([p.lat,p.lon],{radius:inS?17:14,color:inS?'#f59e0b':'#a855f7',weight:inS?4:3,opacity:inS?1:.8,fill:inS,fillColor:'#f59e0b',fillOpacity:.18,dashArray:inS?null:'4 4',interactive:false}).addTo(ZNLY)});
 [...ZN.values()].filter(z=>!z.done&&z.id!=ZNE).forEach(z=>{const Ps=znPoles(z);if(!Ps.length)return;const la=Ps.reduce((a,p)=>a+p.lat,0)/Ps.length,lo=Ps.reduce((a,p)=>a+p.lon,0)/Ps.length;
  L.marker([la,lo],{interactive:false,icon:L.divIcon({className:'',html:'<div class="znlb">'+esc(z.name)+(z.d1?' · '+znPerS(z):'')+'</div>',iconSize:[0,0]})}).addTo(ZNLY)});
 if(ZNPTS.length)(ZNPTS.length>2?L.polygon:L.polyline)(ZNPTS,{color:'#f59e0b',weight:3,dashArray:'6 6',fillColor:'#f59e0b',fillOpacity:.06,interactive:false}).addTo(ZNLY)}
function znShow(id){const z=ZN.get(id);if(!z)return;const Ps=znPoles(z);if(!Ps.length)return toast('На участке нет опор на карте');map.fitBounds(L.latLngBounds(Ps.map(p=>[p.lat,p.lon])).pad(.2))}
/* ---- список участков ---- */
const ZNSN=[['press','Пресс-служба'],['ros','Россети'],['gibdd','ГИБДД']];
function znNeed(z){const n=[];if(z.park!==false)n.push('press');if(z.outage)n.push('ros');if(z.lift&&z.road)n.push('gibdd');return n}
function znRow(z){const Ps=znPoles(z),need=znNeed(z),sent=z.sent||{};
 const st=ZNSN.map(([k,n])=>`<label class="zns${sent[k]?' ok':''}" title="Отметить: письмо отправлено"><input type="checkbox" data-zsn="${z.id}" data-k="${k}"${sent[k]?' checked':''}${need.includes(k)?'':' disabled'}> ${n}${sent[k]?' '+esc(rd(sent[k]).slice(0,5)):''}</label>`).join('');
 return `<div class="zni${z.done?' dn':''}"><div><b>${esc(z.name||'Без названия')}</b> <small style="display:inline">${znPerS(z)}${z.t1||z.t2?' · '+esc((z.t1||'8:00')+'–'+(z.t2||'18:00')):''}${z.done?' · закрыт':''}</small></div>
 <small>опор ${Ps.length} · ${esc(znTps(Ps).map(tpn).join(', '))}${z.lift?' · автовышка':''}${z.road?' на проезжей части':''}${z.outage?' · отключение ВЛ':''}</small>
 <div class="r zsr">${st}</div>
 <div class="r"><button data-zns="${z.id}">Показать</button><button data-znd="${z.id}" class="zdoc">Документы</button><button data-zne="${z.id}">Изменить</button><button data-znc="${z.id}">${z.done?'Вернуть':'Закрыть'}</button><button data-znr="${z.id}" style="color:#f87171">Удалить</button></div><div class="zdl" id="zdl_${z.id}"></div></div>`}
function znList(){const e=$('znl');if(!e)return;const A=[...ZN.values()].sort((a,b)=>(a.done-b.done)||String(a.d1||'9').localeCompare(String(b.d1||'9')));
 e.innerHTML=(A.length?'<b style="display:block;margin-top:8px">Участки ('+A.filter(z=>!z.done).length+' открыто)</b>'+A.map(znRow).join(''):'<small style="display:block;margin-top:6px">Участков пока нет.</small>')+(ZNSRV===false?'<small style="display:block;color:#fbbf24;margin-top:4px">Общей таблицы участков в базе пока нет — участки сохраняются только в этом браузере.</small>':'');
 e.querySelectorAll('[data-zns]').forEach(b=>b.onclick=()=>znShow(b.dataset.zns));
 e.querySelectorAll('[data-zne]').forEach(b=>b.onclick=()=>znEdit(b.dataset.zne));
 e.querySelectorAll('[data-znd]').forEach(b=>b.onclick=()=>znDocUI(b.dataset.znd));
 e.querySelectorAll('[data-znc]').forEach(b=>b.onclick=()=>{const z=ZN.get(b.dataset.znc);if(z)znPut(Object.assign({},z,{done:!z.done}))});
 e.querySelectorAll('[data-znr]').forEach(b=>b.onclick=()=>{const z=ZN.get(b.dataset.znr);if(z&&confirm('Удалить участок «'+(z.name||'')+'»?'))znDel(z.id)});
 e.querySelectorAll('[data-zsn]').forEach(c=>c.onchange=()=>{const z=ZN.get(c.dataset.zsn);if(!z)return;const s=Object.assign({},z.sent||{});if(c.checked)s[c.dataset.k]=LD();else delete s[c.dataset.k];znPut(Object.assign({},z,{sent:s}))})}
/* ---- сервер: таблица work_zones (если её нет — только этот браузер) ---- */
async function znPull(){if(!CF)return;try{const r=await fetch(CF.u+'/rest/v1/work_zones?select=*',{headers:H()}),j=await r.json();if(!Array.isArray(j)){ZNSRV=false;znList();return}
 const first=ZNSRV!==true;ZNSRV=true;const m=new Map(j.map(x=>[x.id,x]));
 if(first){const loc=[...ZN.values()].filter(z=>!m.has(z.id));for(const z of loc){try{await znSend(z);m.set(z.id,z)}catch(e){}}}
 const a=JSON.stringify([...ZN.entries()].sort()),b=JSON.stringify([...m.entries()].sort());if(a!=b){ZN=m;znSave();znDraw();znList()}else if(first)znList()}catch(e){}}
async function znSend(r){if(RO||!CF)throw new Error('нет связи с базой');try{await authFresh()}catch(e){}const x=await fetch(CF.u+'/rest/v1/work_zones?on_conflict=id',{method:'POST',headers:{...H(),Prefer:'resolution=merge-duplicates,return=minimal'},body:JSON.stringify(r)});if(!x.ok)throw new Error(await x.text())}
async function znPut(r){r.ed=WHO||null;r.updated_at=new Date().toISOString();ZN.set(r.id,r);znSave();znDraw();znList();if(ZNSRV===false)return;try{await znSend(r)}catch(e){if(/work_zones|PGRST205|404/.test(String(e.message||e))){ZNSRV=false;znList()}else toast('В базу не сохранилось: '+(e.message||e))}}
async function znDel(id){ZN.delete(id);znSave();znDraw();znList();if(ZNSRV!==true)return;try{await authFresh()}catch(e){}try{await fetch(CF.u+'/rest/v1/work_zones?id=eq.'+encodeURIComponent(id),{method:'DELETE',headers:H()})}catch(e){}}
/* ---- выделение и форма ---- */
function znInfo(){const e=$('zni');if(!e)return;if(ZNA){e.textContent='Нажимайте по карте углы участка. Точек: '+ZNPTS.length+(ZNPTS.length>2?'. Нажмите «Готово».':'');return}e.textContent='Выбрано опор: '+ZNS.size+(ZNE&&ZN.get(ZNE)?' · правка участка «'+(ZN.get(ZNE).name||'')+'»':'')}
function znWind(x,y,pts){let w=0;for(let i=0,j=pts.length-1;i<pts.length;j=i++){const[xi,yi]=pts[j],[xj,yj]=pts[i];if(yi<=y){if(yj>y&&(xj-xi)*(y-yi)-(x-xi)*(yj-yi)>0)w++}else if(yj<=y&&(xj-xi)*(y-yi)-(x-xi)*(yj-yi)<0)w--}return w!=0}
function znApply(){if(ZNPTS.length<3)return null;const pts=ZNPTS.map(a=>lm(a[0],a[1]));let n=0;P.forEach(p=>{if(!p.lat||!p.lon||(p.x&&!p.sx))return;const q=lm(p.lat,p.lon);if(znWind(q[0],q[1],pts)&&!ZNS.has(p.uid)){ZNS.add(p.uid);n++}});return n}
function znTog(p){if(ZNS.has(p.uid))ZNS.delete(p.uid);else ZNS.add(p.uid);znDraw();znInfo()}
function znPt(ll){ZNPTS.push([ll.lat,ll.lng]);znDraw();znInfo()}
function znBtns(){$('zna').hidden=ZNA;$('znok').hidden=$('znun').hidden=!ZNA;map.getContainer().style.cursor=ZNA?'crosshair':''}
function znForm(z){$('znn').value=z?z.name||'':'';$('zn1').value=z?z.d1||'':LD();$('zn2').value=z?z.d2||'':'';$('znt1').value=z?z.t1||'08:00':'08:00';$('znt2').value=z?z.t2||'18:00':'18:00';$('znt').value=z?z.note||'':'';
 document.querySelectorAll('#znw input').forEach(c=>c.checked=z?(z.works||[]).includes(+c.dataset.k):false);
 $('znpk').checked=z?z.park!==false:true;$('znlf').checked=z?!!z.lift:false;$('znrd').checked=z?!!z.road:false;$('znof').checked=z?!!z.outage:false;
 $('znx').hidden=!z;$('zns').textContent=z?'Сохранить изменения':'Сохранить участок'}
function znEdit(id){const z=ZN.get(id);if(!z)return;ZNE=id;ZNS=new Set(z.uids||[]);znForm(z);znDraw();znInfo();znShow(id);$('znp').scrollIntoView({block:'start',behavior:'smooth'})}
/* ---- реквизиты писем ---- */
function znCfgUI(){const F=[['org','Организация'],['orgDet','Реквизиты (адрес, телефон, e-mail)',1],['signPos','Должность подписанта'],['signName','Подписант (И.О. Фамилия)'],['exec','Ответственный за работы (ФИО, телефон)'],['contract','Договор'],['customer','Заказчик'],['customerGen','Заказчик в родительном падеже (по заказу кого)'],['obj','Объект'],['press','Адресат: пресс-служба',1],['ros','Адресат: Россети',1],['gibdd','Адресат: ГИБДД',1],['tech','Спецтехника на проезжей части'],['r','Радиус освобождения места у опоры, м']];
 $('zncf').innerHTML=F.map(([k,n,ml])=>`<label>${n}${ml?`<textarea data-zc="${k}" rows="3">${esc(ZNC[k])}</textarea>`:`<input type="text" data-zc="${k}" value="${esc(ZNC[k])}">`}</label>`).join('')+'<div class="r"><button id="zncr">Вернуть по умолчанию</button></div><small>Хранится в этом браузере.</small>';
 $('zncf').querySelectorAll('[data-zc]').forEach(i=>i.oninput=()=>{ZNC[i.dataset.zc]=i.dataset.zc=='r'?(+i.value||10):i.value;try{localStorage.setItem(KEY+'_znc',JSON.stringify(ZNC))}catch(e){}});
 $('zncr').onclick=()=>{if(!confirm('Вернуть реквизиты писем по умолчанию?'))return;ZNC=Object.assign({},ZND);try{localStorage.removeItem(KEY+'_znc')}catch(e){}znCfgUI()}}
/* ---- схема участка (PDF, A4 альбом) ---- */
async function znPage(z,L2,streets,base,onp){const u=250/25.4,CW=Math.round(297*u),CH=Math.round(210*u),cv=document.createElement('canvas');cv.width=CW;cv.height=CH;const g=cv.getContext('2d');g.fillStyle='#fff';g.fillRect(0,0,CW,CH);
 const F='Arial, Helvetica, sans-serif',pad=9*u,top=27*u,mx=pad,my=top,mw=CW-2*pad,mh=CH-top-pad-3*u;
 const wX=lo=>(lo+180)/360*256,wY=la=>{const s=Math.sin(la*Math.PI/180);return(.5-Math.log((1+s)/(1-s))/(4*Math.PI))*256};
 const lat=L2.map(p=>p.lat),lon=L2.map(p=>p.lon);let bb={s:Math.min(...lat),n:Math.max(...lat),w:Math.min(...lon),e:Math.max(...lon)};
 {const dl=Math.max(0,.0018-(bb.n-bb.s))/2,dw=Math.max(0,.0038-(bb.e-bb.w))/2,ml=(bb.n-bb.s)*.1+.0003,mwd=(bb.e-bb.w)*.1+.0006;bb={s:bb.s-dl-ml,n:bb.n+dl+ml,w:bb.w-dw-mwd,e:bb.e+dw+mwd}}
 const x0=wX(bb.w),x1=wX(bb.e),y0=wY(bb.n),y1=wY(bb.s),f0=Math.min(mw/(x1-x0),mh/(y1-y0));
 const cnt=zz=>{const s=2**zz,k=f0/s,hw=mw/2/k,hh=mh/2/k,cx=(x0+x1)/2*s,cy=(y0+y1)/2*s;return(Math.floor((cx+hw)/256)-Math.floor((cx-hw)/256)+1)*(Math.floor((cy+hh)/256)-Math.floor((cy-hh)/256)+1)};
 let zm=Math.min(19,Math.ceil(Math.log2(f0)));while(zm>8&&cnt(zm)>140)zm--;
 const s=2**zm,k=f0/s,cwx=(x0+x1)/2*s,cwy=(y0+y1)/2*s,C=(la,lo)=>[mx+mw/2+(wX(lo)*s-cwx)*k,my+mh/2+(wY(la)*s-cwy)*k];
 const jobs=[];for(let a=Math.floor((cwx-mw/2/k)/256);a<=Math.floor((cwx+mw/2/k)/256);a++)for(let b=Math.floor((cwy-mh/2/k)/256);b<=Math.floor((cwy+mh/2/k)/256);b++)jobs.push([a,b]);
 const url=(a,b)=>base=='esri'?`https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/${zm}/${b}/${a}`:`https://tile.openstreetmap.org/${Math.min(zm,19)}/${a}/${b}.png`;
 g.save();g.beginPath();g.rect(mx,my,mw,mh);g.clip();g.fillStyle='#eef0f2';g.fillRect(mx,my,mw,mh);let ok=0,n=0,q=0;
 await Promise.all(Array.from({length:6},async()=>{while(q<jobs.length){const [a,b]=jobs[q++],im=await loadTile(url(a,b));n++;if(im){ok++;g.drawImage(im,mx+mw/2+(a*256-cwx)*k,my+mh/2+(b*256-cwy)*k,256*k+.6,256*k+.6)}onp&&onp(n,jobs.length)}}));
 g.fillStyle=base=='esri'?'rgba(255,255,255,.1)':'rgba(255,255,255,.2)';g.fillRect(mx,my,mw,mh);
 const mpp=156543.03392*Math.cos(((bb.s+bb.n)/2)*Math.PI/180)/s/k,inb=(la,lo)=>la>=bb.s-.002&&la<=bb.n+.002&&lo>=bb.w-.004&&lo<=bb.e+.004,lw=.3*u;
 try{g.lineCap='round';const NT=netEdges();g.strokeStyle='rgba(29,78,216,.5)';g.lineWidth=lw*1.3;NT.E.filter(e=>(e[2]!='d'||e.pts)&&(inb(e[0].lat,e[0].lon)||inb(e[1].lat,e[1].lon))).forEach(e=>{g.setLineDash(e[2]=='n'||e[2]=='r'?[lw*4,lw*3]:[]);g.beginPath();epath(e[0],e[1],e.pts).forEach((c,i)=>i?g.lineTo(...C(c[0],c[1])):g.moveTo(...C(c[0],c[1])));g.stroke()});g.setLineDash([])}catch(e){}
 const SEL=new Set(L2);P.forEach(p=>{if(SEL.has(p)||!inb(p.lat,p.lon)||(p.x&&!p.sx))return;const[x,y]=C(p.lat,p.lon);g.beginPath();g.arc(x,y,.7*u,0,7);g.fillStyle='rgba(255,255,255,.9)';g.fill();g.strokeStyle='#6b7280';g.lineWidth=.25*u;g.stroke()});
 const PT=L2.map(p=>({p,xy:C(p.lat,p.lon)})),R=1.35*u,rz=Math.max(2.2*u,(+ZNC.r||10)/mpp);
 if(z.park!==false)PT.forEach(({xy:[x,y]})=>{g.beginPath();g.arc(x,y,rz,0,7);g.fillStyle='rgba(239,68,68,.16)';g.fill();g.setLineDash([.9*u,.6*u]);g.strokeStyle='rgba(220,38,38,.85)';g.lineWidth=.3*u;g.stroke();g.setLineDash([])});
 PT.forEach(({xy:[x,y]})=>{g.beginPath();g.arc(x,y,R,0,7);g.fillStyle='#f59e0b';g.fill();g.strokeStyle='#fff';g.lineWidth=.45*u;g.stroke();g.beginPath();g.arc(x,y,R+.25*u,0,7);g.strokeStyle='#111';g.lineWidth=.2*u;g.stroke()});
 const many=L2.length>60,placed=[],obst=PT.map(({xy:[x,y]})=>[x-R-.5*u,y-R-.5*u,x+R+.5*u,y+R+.5*u]),hit=(b,A)=>A.some(c=>b[0]<c[2]&&b[2]>c[0]&&b[1]<c[3]&&b[3]>c[1]),f1=(many?2.1:2.6)*u,lh=(many?2.5:3)*u;
 PT.slice().sort((a,b)=>a.xy[1]-b.xy[1]||a.xy[0]-b.xy[0]).forEach(({p,xy:[x,y]})=>{const t=String(p.id||'');g.font=`bold ${f1}px ${F}`;const bw=g.measureText(t).width+1.6*u,bh=lh+.6*u;
  const cand=[];[1,2,3.4,5].forEach(m=>{const d=(R+1*u)*m;[[d,-bh/2],[-d-bw,-bh/2],[-bw/2,-d-bh],[-bw/2,d],[d*.75,-d*.75-bh],[-d*.75-bw,-d*.75-bh],[d*.75,d*.75],[-d*.75-bw,d*.75]].forEach(([dx,dy])=>cand.push([x+dx,y+dy]))});
  let bx=null;for(const c of cand){const b=[c[0],c[1],c[0]+bw,c[1]+bh];if(b[0]<mx+1*u||b[2]>mx+mw-1*u||b[1]<my+1*u||b[3]>my+mh-1*u)continue;if(hit(b,placed)||hit(b,obst))continue;bx=c;break}
  if(!bx){if(many)return;bx=cand[0]}const b=[bx[0],bx[1],bx[0]+bw,bx[1]+bh];placed.push(b);const cx=Math.max(b[0],Math.min(x,b[2])),cy=Math.max(b[1],Math.min(y,b[3]));if(Math.hypot(cx-x,cy-y)>R+1.4*u){g.beginPath();g.moveTo(x,y);g.lineTo(cx,cy);g.strokeStyle='#111';g.lineWidth=.2*u;g.stroke()}
  g.fillStyle='rgba(255,255,255,.93)';g.fillRect(b[0],b[1],bw,bh);g.strokeStyle='#d97706';g.lineWidth=.3*u;g.strokeRect(b[0],b[1],bw,bh);g.fillStyle='#111';g.textAlign='left';g.textBaseline='middle';g.font=`bold ${f1}px ${F}`;g.fillText(t,b[0]+.8*u,b[1]+bh/2)});
 /* масштаб, север, подложка */
 let m=[10,20,25,50,100,200,250,500,1000].find(v=>v/mpp>=22*u)||1000;g.fillStyle='rgba(255,255,255,.88)';g.fillRect(mx+3*u,my+mh-12*u,m/mpp+10*u,9*u);g.strokeStyle='#111';g.lineWidth=.4*u;const sx=mx+8*u,sy=my+mh-5.5*u;g.beginPath();g.moveTo(sx,sy);g.lineTo(sx+m/mpp,sy);g.moveTo(sx,sy-1.1*u);g.lineTo(sx,sy+1.1*u);g.moveTo(sx+m/mpp,sy-1.1*u);g.lineTo(sx+m/mpp,sy+1.1*u);g.stroke();g.fillStyle='#111';g.font=`${2.8*u}px ${F}`;g.textAlign='left';g.textBaseline='alphabetic';g.fillText(m+' м',sx,sy-2.6*u);
 const nx=mx+mw-9*u,ny=my+12*u;g.fillStyle='rgba(255,255,255,.88)';g.fillRect(nx-5*u,ny-9*u,10*u,18*u);g.strokeStyle='#111';g.lineWidth=.4*u;g.beginPath();g.moveTo(nx,ny+7*u);g.lineTo(nx,ny-4*u);g.stroke();g.beginPath();g.moveTo(nx,ny-8*u);g.lineTo(nx-1.8*u,ny-3*u);g.lineTo(nx+1.8*u,ny-3*u);g.fillStyle='#111';g.fill();g.font=`bold ${3*u}px ${F}`;g.textAlign='center';g.fillText('С',nx,ny+6.5*u);
 /* условные обозначения */
 const lg=[['op','Опора, у которой ведутся работы']];if(z.park!==false)lg.push(['zone','Освободить от автомобилей (≈'+(+ZNC.r||10)+' м от опоры)']);lg.push(['line','Линия уличного освещения']);
 g.font=`${2.7*u}px ${F}`;const lw2=Math.max(...lg.map(x=>g.measureText(x[1]).width))+11*u,lh2=4.6*u,lx=mx+mw-lw2-2*u,ly=my+mh-lg.length*lh2-9*u;g.fillStyle='rgba(255,255,255,.92)';g.fillRect(lx,ly,lw2,lg.length*lh2+2*u);g.strokeStyle='#999';g.lineWidth=.2*u;g.strokeRect(lx,ly,lw2,lg.length*lh2+2*u);
 lg.forEach(([t,s2],i)=>{const cy=ly+1*u+lh2*(i+.5),cx=lx+4*u;if(t=='op'){g.beginPath();g.arc(cx,cy,R,0,7);g.fillStyle='#f59e0b';g.fill();g.strokeStyle='#111';g.lineWidth=.2*u;g.stroke()}else if(t=='zone'){g.beginPath();g.arc(cx,cy,2*u,0,7);g.fillStyle='rgba(239,68,68,.16)';g.fill();g.setLineDash([.9*u,.6*u]);g.strokeStyle='rgba(220,38,38,.85)';g.lineWidth=.3*u;g.stroke();g.setLineDash([])}else{g.beginPath();g.moveTo(cx-3*u,cy);g.lineTo(cx+3*u,cy);g.strokeStyle='rgba(29,78,216,.7)';g.lineWidth=.5*u;g.stroke()}g.fillStyle='#111';g.textAlign='left';g.textBaseline='middle';g.fillText(s2,lx+9*u,cy)});
 g.font=`${2.2*u}px ${F}`;g.textAlign='right';g.textBaseline='alphabetic';const at=ok?(base=='esri'?'Подложка: Esri World Imagery':'© участники OpenStreetMap'):'Подложка не загрузилась (нет интернета)',aw=g.measureText(at).width+3*u;g.fillStyle='rgba(255,255,255,.85)';g.fillRect(mx+mw-aw,my+mh-4.6*u,aw,4.6*u);g.fillStyle='#222';g.fillText(at,mx+mw-1.5*u,my+mh-1.4*u);
 g.restore();g.strokeStyle='#666';g.lineWidth=.3*u;g.strokeRect(mx,my,mw,mh);
 g.textAlign='left';g.textBaseline='alphabetic';g.fillStyle='#111';g.font=`bold ${7*u}px ${F}`;g.fillText('Схема участка работ: '+(z.name||''),pad,top-15*u);
 g.font=`${3.6*u}px ${F}`;const l2=[znPer(z),znTime(z)].filter(Boolean).join(', ')+(streets.length?' · '+streets.slice(0,4).join(', '):'');g.fillText(l2,pad,top-9.5*u);
 const W=znWN(z);g.fillText('Опор: '+L2.length+(W.length?' · '+W.join(', '):'')+(z.lift?' · '+ZNC.tech:''),pad,top-4*u);
 return cv}
async function znPdf(z,L2,streets,base,st){const cv=await znPage(z,L2,streets,base,(a,b)=>st('Схема: подложка '+a+'/'+b));if(!window.jspdf)await loadScript('https://cdnjs.cloudflare.com/ajax/libs/jspdf/2.5.1/jspdf.umd.min.js');
 const{jsPDF}=window.jspdf,doc=new jsPDF({orientation:'landscape',unit:'mm',format:'a4',compress:true});doc.addImage(cv.toDataURL('image/jpeg',.9),'JPEG',0,0,297,210);return doc.output('blob')}
/* ---- DOCX (минимальный: абзацы и таблицы), A4, Times New Roman ---- */
const zx=t=>String(t==null?'':t).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');
function zRun(t,o){o=o||{};const pr=(o.b?'<w:b/>':'')+(o.i?'<w:i/>':'')+(o.sz?'<w:sz w:val="'+o.sz*2+'"/><w:szCs w:val="'+o.sz*2+'"/>':'');return String(t).split('\n').map((x,i)=>(i?'<w:r>'+(pr?'<w:rPr>'+pr+'</w:rPr>':'')+'<w:br/></w:r>':'')+'<w:r>'+(pr?'<w:rPr>'+pr+'</w:rPr>':'')+'<w:t xml:space="preserve">'+zx(x)+'</w:t></w:r>').join('')}
function zP(t,o){o=o||{};const ppr='<w:pPr>'+(o.keep?'<w:keepNext/>':'')+'<w:spacing w:before="'+(o.before||0)+'" w:after="'+(o.after==null?120:o.after)+'" w:line="'+(o.line||264)+'" w:lineRule="auto"/>'+(o.ind?'<w:ind w:firstLine="709"/>':'')+(o.left?'<w:ind w:left="'+o.left+'"/>':'')+'<w:jc w:val="'+(o.al||'both')+'"/></w:pPr>';
 const runs=Array.isArray(t)?t.map(x=>typeof x=='string'?zRun(x,o):zRun(x.t,Object.assign({},o,x))).join(''):zRun(t,o);return '<w:p>'+ppr+runs+'</w:p>'}
function zT(rows,W,o){o=o||{};const bd=o.nob?'<w:tblBorders><w:top w:val="nil"/><w:left w:val="nil"/><w:bottom w:val="nil"/><w:right w:val="nil"/><w:insideH w:val="nil"/><w:insideV w:val="nil"/></w:tblBorders>':'<w:tblBorders><w:top w:val="single" w:sz="4"/><w:left w:val="single" w:sz="4"/><w:bottom w:val="single" w:sz="4"/><w:right w:val="single" w:sz="4"/><w:insideH w:val="single" w:sz="4"/><w:insideV w:val="single" w:sz="4"/></w:tblBorders>';
 return '<w:tbl><w:tblPr><w:tblW w:w="'+W.reduce((a,b)=>a+b,0)+'" w:type="dxa"/>'+bd+'<w:tblLayout w:type="fixed"/><w:tblCellMar><w:left w:w="70" w:type="dxa"/><w:right w:w="70" w:type="dxa"/></w:tblCellMar></w:tblPr><w:tblGrid>'+W.map(w=>'<w:gridCol w:w="'+w+'"/>').join('')+'</w:tblGrid>'+
 rows.map((r,ri)=>'<w:tr>'+(ri==0&&o.head?'<w:trPr><w:tblHeader/></w:trPr>':'')+r.map((c,ci)=>'<w:tc><w:tcPr><w:tcW w:w="'+W[ci]+'" w:type="dxa"/></w:tcPr>'+(typeof c=='string'&&c.startsWith('<w:')?c:zP(c,{after:0,line:240,al:(o.al&&o.al[ci])||'left',b:ri==0&&o.head,sz:o.sz||11}))+'</w:tc>').join('')+'</w:tr>').join('')+'</w:tbl>'}
async function zDocx(body){if(!window.JSZip)await loadScript('https://cdnjs.cloudflare.com/ajax/libs/jszip/3.10.1/jszip.min.js');const Z=new JSZip();
 Z.file('[Content_Types].xml','<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="xml" ContentType="application/xml"/><Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/><Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/></Types>');
 Z.file('_rels/.rels','<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/></Relationships>');
 Z.file('word/_rels/document.xml.rels','<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/></Relationships>');
 Z.file('word/styles.xml','<?xml version="1.0" encoding="UTF-8" standalone="yes"?><w:styles xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"><w:docDefaults><w:rPrDefault><w:rPr><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman" w:cs="Times New Roman" w:eastAsia="Times New Roman"/><w:sz w:val="26"/><w:szCs w:val="26"/><w:lang w:val="ru-RU"/></w:rPr></w:rPrDefault><w:pPrDefault><w:pPr><w:spacing w:after="0"/></w:pPr></w:pPrDefault></w:docDefaults><w:style w:type="paragraph" w:default="1" w:styleId="a"><w:name w:val="Normal"/></w:style></w:styles>');
 Z.file('word/document.xml','<?xml version="1.0" encoding="UTF-8" standalone="yes"?><w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"><w:body>'+body+'<w:sectPr><w:pgSz w:w="11906" w:h="16838"/><w:pgMar w:top="1134" w:right="850" w:bottom="1134" w:left="1701" w:header="709" w:footer="709" w:gutter="0"/></w:sectPr></w:body></w:document>');
 return Z.generateAsync({type:'blob',mimeType:'application/vnd.openxmlformats-officedocument.wordprocessingml.document'})}
/* ---- тексты писем ---- */
function zHead(to,subj){const c=ZNC,today=znDay(LD());
 const left=zP([{t:c.org,b:true}],{al:'left',after:0})+(c.orgDet?zP(c.orgDet,{al:'left',after:0,sz:11}):'')+zP('Исх. № ______ от '+today,{al:'left',before:200,after:0,sz:12});
 return zT([[left,zP(to,{al:'left',after:0})]],[4400,4955],{nob:true})+zP('',{after:240})+zP([{t:subj,b:true}],{al:'center',after:240})}
function zSign(attach){const c=ZNC;let h='';if(attach&&attach.length)h+=zP('Приложение: '+(attach.length==1?attach[0]:attach.map((a,i)=>(i+1)+') '+a).join('; ')).replace(/\.$/,'')+'.',{before:120,after:240});
 h+=zP('',{after:240})+zT([[zP(c.signPos,{al:'left',after:0}),zP('',{al:'center',after:0}),zP(c.signName,{al:'right',after:0})]],[4200,2500,2655],{nob:true});
 if(c.exec)h+=zP('',{after:480})+zP('Исп.: '+c.exec,{al:'left',sz:10,after:0});return h}
function zPoleTab(L2){const rows=[['№','Опора','ТП','Улица / ориентир']];L2.slice().sort((a,b)=>znRu(a.id,b.id)).forEach((p,i)=>rows.push([String(i+1),String(p.id||''),tpn(String(p.tp||'')),(p.ad&&p.ad.trim())||p._zst||'—']));return zT(rows,[700,1900,1700,5055],{head:true,al:['center','left','left','left'],sz:11})}
function zWhere(z,streets){return streets.length?(streets.length==1?'на '+streets[0]:'на улицах: '+streets.join(', ')):'на участке «'+z.name+'»'}
function zWorksTxt(z){const W=znWN(z);return W.length?W.join(', '):'работы по модернизации уличного освещения'}
function znNotice(z,L2,streets){const c=ZNC,when=[znPer(z),znTime(z)].filter(Boolean).join(' ');
 let b=zP([{t:'Уважаемые жители!',b:true}],{al:'center',after:200,sz:14});
 b+=zP(when.charAt(0).toUpperCase()+when.slice(1)+' '+zWhere(z,streets)+' будут проводиться работы по модернизации уличного освещения: '+zWorksTxt(z)+'.',{ind:true,sz:14});
 if(z.park!==false)b+=zP([{t:'Просим освободить от автомобилей места около опор освещения',b:true},' (примерно '+(+c.r||10)+' м от опоры) на время работ. Опоры, у которых будут вестись работы, отмечены на схеме.'],{ind:true,sz:14});
 if(z.lift)b+=zP('Работы ведутся с применением спецтехники'+(z.road?' на проезжей части — возможны временные ограничения движения. Будьте внимательны, соблюдайте указания работников и временных дорожных знаков.':'.'),{ind:true,sz:14});
 if(z.outage)b+=zP('На время работ возможно временное отключение электроснабжения на этих улицах.',{ind:true,sz:14});
 b+=zP('Приносим извинения за временные неудобства. Работы выполняет '+c.org+' по заказу '+(c.customerGen||c.customer)+'.'+(c.exec?' Контактное лицо: '+c.exec+'.':''),{ind:true,sz:14});
 return b}
function znLetter(kind,z,L2,streets){const c=ZNC,when=[znPer(z),znTime(z)].filter(Boolean).join(' '),tps=znTps(L2).map(tpn).join(', '),intro=c.org+' выполняет работы по объекту '+c.obj+' ('+c.contract+', заказчик — '+c.customer+').';
 if(kind=='press'){let b=zHead(c.press,'О размещении информации для жителей о проведении работ');
  b+=zP(intro,{ind:true});
  b+=zP('Просим разместить на официальном сайте и в социальных сетях информацию для жителей: '+when+' '+zWhere(z,streets)+' будут проводиться работы: '+zWorksTxt(z)+'.',{ind:true});
  if(z.park!==false)b+=zP('На время работ жителям необходимо освободить от автомобилей места около опор освещения (примерно '+(+c.r||10)+' м от опоры). Количество опор на участке — '+L2.length+'; их расположение показано на схеме.',{ind:true});
  b+=zP('Текст объявления для жителей приведён ниже.',{ind:true});
  b+=zP('',{after:120})+zT([[znNotice(z,L2,streets)]],[9355],{sz:12});
  return b+zSign(['схема участка работ на 1 л.'])}
 if(kind=='ros'){let b=zHead(c.ros,'Об отключении ВЛ 0,4 кВ на время производства работ');
  b+=zP(intro,{ind:true});
  b+=zP('Для безопасного производства работ ('+zWorksTxt(z)+') '+zWhere(z,streets)+' просим отключить (вывести в ремонт) воздушные линии 0,4 кВ'+(tps?' в зоне работ (питание от '+tps+')':'')+', проходящие по опорам участка, '+when+'.',{ind:true});
  b+=zP('Работы выполняются в охранной зоне ВЛ по наряду-допуску в соответствии с Правилами по охране труда при эксплуатации электроустановок (приказ Минтруда России от 15.12.2020 № 903н) и Правилами установления охранных зон объектов электросетевого хозяйства (постановление Правительства РФ от 24.02.2009 № 160).'+(c.exec?' Ответственный руководитель работ — '+c.exec+'.':''),{ind:true});
  b+=zP('Просим сообщить о согласовании отключения и заблаговременно уведомить потребителей, электроснабжение которых будет прекращено.',{ind:true});
  b+=zP('Перечень опор участка ('+L2.length+' шт.):',{before:120,keep:true})+zPoleTab(L2);
  return b+zSign(['схема участка работ на 1 л.'])}
 if(kind=='gibdd'){let b=zHead(c.gibdd,'О проведении работ на проезжей части с применением автовышки');
  b+=zP(intro,{ind:true});
  b+=zP('Уведомляем, что '+when+' '+zWhere(z,streets)+' будут проводиться работы ('+zWorksTxt(z)+') с размещением на проезжей части спецтехники: '+c.tech+'.',{ind:true});
  b+=zP('Места производства работ будут обозначены временными дорожными знаками и ограждениями в соответствии с ОДМ 218.6.019-2016 и проектом организации дорожного движения. Движение транспорта будет ограничиваться только на время работы техники у конкретной опоры, без полного перекрытия улицы.'+(c.exec?' Ответственный за производство работ — '+c.exec+'.':''),{ind:true});
  b+=zP('Перечень опор, у которых будет работать техника ('+L2.length+' шт.):',{before:120,keep:true})+zPoleTab(L2);
  return b+zSign(['схема участка работ на 1 л.'])}
 if(kind=='notice')return znNotice(z,L2,streets)}
/* ---- архив документов ---- */
const ZNF={scheme:'Схема участка.pdf',press:'Письмо в пресс-службу.docx',notice:'Объявление для жителей.docx',ros:'Письмо в Россети — отключение ВЛ 0,4 кВ.docx',gibdd:'Письмо в ГИБДД — автовышка на проезжей части.docx'};
function znDocUI(id){const z=ZN.get(id),e=$('zdl_'+id);if(!z||!e)return;if(e.innerHTML){e.innerHTML='';return}const need=znNeed(z),def=k=>k=='scheme'||need.includes(k)||(k=='notice'&&need.includes('press'));
 e.innerHTML='<div class="zdb">'+Object.entries(ZNF).map(([k,n])=>`<label><input type="checkbox" data-zf="${k}"${def(k)?' checked':''}> ${esc(n.replace(/\.(pdf|docx)$/,''))}</label>`).join('')+'<div class="r"><select data-zb><option value="osm">подложка: карта</option><option value="esri">подложка: спутник</option></select><button data-zgo>Скачать архив</button></div><small data-zst></small></div>';
 e.querySelector('[data-zgo]').onclick=()=>znMake(z,[...e.querySelectorAll('[data-zf]:checked')].map(c=>c.dataset.zf),e.querySelector('[data-zb]').value,t=>e.querySelector('[data-zst]').textContent=t)}
async function znMake(z,kinds,base,st){const L2=znPoles(z);if(!L2.length)return st('На участке нет опор на карте.');if(!kinds.length)return st('Отметьте, какие документы нужны.');
 try{st('Определяю улицы…');const streets=await znStreets(L2);if(!window.JSZip)await loadScript('https://cdnjs.cloudflare.com/ajax/libs/jszip/3.10.1/jszip.min.js');
  const dir=('Участок '+(z.name||'')+(z.d1?' '+znPerS(z):'')).replace(/[\\/:*?"<>|]+/g,' ').replace(/\s+/g,' ').trim(),Z=new JSZip(),F=Z.folder(dir);
  const save=(blob,name)=>{const a=document.createElement('a');a.href=URL.createObjectURL(blob);a.download=name;document.body.appendChild(a);a.click();setTimeout(()=>{URL.revokeObjectURL(a.href);a.remove()},4000)};
  const files=[];for(const k of kinds){if(k=='scheme'){st('Готовлю схему…');files.push([dir+'.pdf',await znPdf(z,L2,streets,base,st)])}else{st('Готовлю: '+ZNF[k]+'…');files.push([ZNF[k],await zDocx(znLetter(k,z,L2,streets))])}}
  if(files.length==1){save(files[0][1],files[0][0]);st('Готово: '+files[0][0]);return}
  files.forEach(([n,b])=>F.file(n,b));st('Упаковываю…');save(await Z.generateAsync({type:'blob'}),dir+'.zip');
  st('Готово: '+dir+'.zip — '+files.length+' файл(ов) в папке «'+dir+'».')}catch(e){console.error(e);st('Ошибка: '+(e.message||e))}}
/* ---- кнопки ---- */
if(!RO&&$('zna')){
 $('zna').onclick=()=>{map.closePopup();ZNA=true;ZNPTS=[];znBtns();znDraw();znInfo()};
 $('znun').onclick=()=>{ZNPTS.pop();znDraw();znInfo()};
 $('znok').onclick=()=>{const n=znApply();if(n!=null)toast('Добавлено опор: '+n+' · выбрано всего: '+ZNS.size);ZNA=false;ZNPTS=[];znBtns();znDraw();znInfo()};
 $('znc').onclick=()=>{ZNS.clear();ZNE=null;ZNA=false;ZNPTS=[];znBtns();znForm(null);znDraw();znInfo()};
 $('znx').onclick=()=>$('znc').onclick();
 $('zns').onclick=async()=>{if(ZNA){const n=znApply();ZNA=false;ZNPTS=[];znBtns();znDraw();znInfo();if(n!=null)toast('Контур применён: добавлено опор '+n)}const name=$('znn').value.trim(),works=[...document.querySelectorAll('#znw input:checked')].map(c=>+c.dataset.k);if(!ZNS.size)return alert('Выберите опоры: нажимайте на опоры или обведите участок.');if(!name)return alert('Впишите название участка, например «ул. Победы, ТП90».');if(!$('zn1').value)return alert('Укажите дату начала работ.');
  const old=ZNE&&ZN.get(ZNE),r={id:old?old.id:'zn'+Date.now().toString(36)+Math.random().toString(36).slice(2,6),name,works,uids:[...ZNS],d1:$('zn1').value||null,d2:$('zn2').value||$('zn1').value||null,t1:$('znt1').value||null,t2:$('znt2').value||null,
   park:$('znpk').checked,lift:$('znlf').checked,road:$('znrd').checked,outage:$('znof').checked,note:$('znt').value.trim(),sent:old?old.sent||{}:{},done:old?!!old.done:false};
  await znPut(r);toast('Участок «'+name+'» сохранён');ZNS.clear();ZNE=null;znForm(null);znDraw();znInfo()};
 $('zncb').onclick=()=>{const e=$('zncf');e.hidden=!e.hidden;if(!e.hidden)znCfgUI()};
 map.on('click',e=>{if(mode=='zone'&&ZNA)znPt(e.latlng)});znForm(null)}
try{const h=document.querySelector('#s>small');if(h&&$('znp'))h.after($('znp'))}catch(e){}
setTimeout(()=>{znPull();znList();znDraw();const b=document.querySelector('#modes [data-m="zone"]');if(b&&mode!='zone')b.click()},1200);setInterval(znPull,30000);
/* ---- участки работ: END ---- */
