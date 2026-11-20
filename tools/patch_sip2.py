# СИП «2-я цепь»: линия одного ТП по опорам другого ТП (таблица sip2). Рисуется сплошной оранжевой линией
# рядом с линией опор (смещение ~2,5 м там, где на пролёте уже есть СИП), метки «2ц ТП97»;
# точки {hook:'arch'} — значок «крепление к своду арки» (вариант В). В редакторе значок можно перетащить.
# Также: в PDF-плане (линия + значок + строки легенды), длина 2-й цепи в окне линии.
import sys
p=sys.argv[1];s=open(p,encoding='utf-8').read()
def R(a,b,n=1):
    global s
    assert s.count(a)==n,(a[:90],s.count(a));s=s.replace(a,b)
JS=r"""
/* ---- СИП 2-я цепь (таблица sip2) ---- */
var S2=[],S2J='',S2LY=L.layerGroup().addTo(map);
const S2C='#f97316';
function s2Pts(z){const U=new Map(P.map(p=>[p.uid,p]));return (z.path||[]).map(q=>{if(q.p){const p=U.get(q.p);return p?{lat:+p.lat,lon:+p.lon,p}:null}return {lat:+q.lat,lon:+q.lon,hook:q.hook,q}}).filter(Boolean)}
function s2Has(a,b){if(!a.p||!b.p)return false;const k=a.p.uid<b.p.uid?a.p.uid+'|'+b.p.uid:b.p.uid+'|'+a.p.uid;try{return SPANS.has(k)}catch(e){return false}}
function s2Geo(z){const pts=s2Pts(z),K=111320*Math.cos(61.71*Math.PI/180),OF=2.5,out=[];
 for(let i=0;i<pts.length-1;i++){const a=pts[i],b=pts[i+1],sh=s2Has(a,b);let dx=(b.lon-a.lon)*K,dy=(b.lat-a.lat)*110574;const l=Math.hypot(dx,dy)||1;dx/=l;dy/=l;const ox=sh?-dy*OF:0,oy=sh?dx*OF:0;
  out.push([[a.lat+oy/110574,a.lon+ox/K],[b.lat+oy/110574,b.lon+ox/K],l,sh])}
 return {pts,seg:out,len:out.reduce((s,x)=>s+x[2],0)}}
function s2Hook(){return '<svg width="46" height="46" viewBox="-20 -20 40 40" style="overflow:visible"><path d="M-14-6H14" stroke="#111" stroke-width="3"/><path d="M-12-6l-5-6M-6-6l-5-6M0-6l-5-6M6-6l-5-6M12-6l-5-6" stroke="#111" stroke-width="1.6"/><path d="M-4-6V2a4 4 0 0 0 8 0" fill="none" stroke="#dc2626" stroke-width="2.6" stroke-linecap="round"/><circle cy="6" r="3.2" fill="'+S2C+'" stroke="#fff" stroke-width="1.2"/></svg>'}
function s2Popup(z,ll){const g=s2Geo(z),ps=g.pts.filter(x=>x.p),h=g.pts.filter(x=>x.hook).length;
 L.popup().setLatLng(ll).setContent('<div class="pp"><div><b>СИП ТП'+esc(z.tp)+' — 2-я цепь</b></div><div>'+esc(ps[0]?ps[0].p.id:'')+' → '+esc(ps.length?ps[ps.length-1].p.id:'')+' · ≈ <b>'+Math.round(g.len)+' м</b> по карте</div><div>по опорам: '+ps.slice(1,-1).map(x=>esc(x.p.id)).join(', ')+'</div>'+(h?'<div>крюк в своде арки: '+h+'</div>':'')+(z.note?'<small>'+esc(z.note)+'</small>':'')+'</div>').openOn(map)}
function s2Draw(){S2LY.clearLayers();const zm=map.getZoom();
 S2.forEach(z=>{const g=s2Geo(z);g.seg.forEach((sg,i)=>{const ll=[sg[0],sg[1]];L.polyline(ll,{color:'#fff',weight:7,opacity:.85,interactive:false}).addTo(S2LY);const ln=L.polyline(ll,{color:S2C,weight:4}).addTo(S2LY);ln.on('click',e=>{L.DomEvent.stop(e);s2Popup(z,e.latlng)});
   if(zm>=17&&i%2==0)L.marker([(sg[0][0]+sg[1][0])/2,(sg[0][1]+sg[1][1])/2],{interactive:false,icon:L.divIcon({className:'',iconSize:[0,0],html:'<div style="position:absolute;left:0;top:0;transform:translate(-50%,-50%);white-space:nowrap;font:600 11px Commissioner,Arial;padding:1px 5px;border-radius:5px;background:'+S2C+';color:#fff">2ц ТП'+esc(z.tp)+'</div>'})}).addTo(S2LY)});
  g.pts.forEach((q,i)=>{if(!q.hook)return;const m=L.marker([q.lat,q.lon],{draggable:!RO,icon:L.divIcon({className:'',iconSize:[0,0],html:'<div style="position:absolute;left:0;top:0;transform:translate(-50%,-50%)">'+s2Hook()+'</div>'+(zm>=17?'<div style="position:absolute;left:0;top:20px;transform:translate(-50%,0);white-space:nowrap;font:600 11px Commissioner,Arial;padding:1px 5px;border-radius:5px;background:#111827;color:#fff">крюк в своде арки</div>':'')})}).addTo(S2LY);
   m.on('click',e=>{L.DomEvent.stop(e);s2Popup(z,e.latlng)});
   if(!RO)m.on('dragend',async()=>{const ll=m.getLatLng();q.q.lat=+ll.lat.toFixed(7);q.q.lon=+ll.lng.toFixed(7);s2Draw();try{const r=await fetch(CF.u+'/rest/v1/sip2?uid=eq.'+encodeURIComponent(z.uid),{method:'PATCH',headers:{...H(),Prefer:'return=minimal'},body:JSON.stringify({path:z.path,ed:WHO||null})});if(!r.ok)throw new Error(await r.text());S2J=JSON.stringify(S2);toast('Крюк в арке перенесён')}catch(e){toast('Не сохранилось: '+(e.message||e))}})})})}
async function s2Load(){try{if(!CF)return;const r=await fetch(CF.u+'/rest/v1/sip2?select=*&order=uid',{headers:H()});const j=await r.json();if(!Array.isArray(j))return;const js=JSON.stringify(j);if(js===S2J)return;S2J=js;S2=j;s2Draw()}catch(e){}}
map.on('zoomend',()=>{if(S2.length)s2Draw()});
setTimeout(s2Load,1500);setInterval(()=>{if(!document.hidden)s2Load()},30000);
"""
R("async function sync(){LSYNC=Date.now();",JS+"\nasync function sync(){LSYNC=Date.now();")
# PDF: линия и значок
R("const r=.95*u;window.DPK=!!o.bigk;SH.forEach(p=>dpole(g,...C",
  "try{S2.forEach(z=>{const gg=s2Geo(z);g.save();g.lineCap='round';gg.seg.forEach(sg=>{const a=C(sg[0][0],sg[0][1]),b=C(sg[1][0],sg[1][1]);g.strokeStyle='#fff';g.lineWidth=lw*4.2;g.beginPath();g.moveTo(...a);g.lineTo(...b);g.stroke();g.strokeStyle=S2C;g.lineWidth=lw*2.4;g.beginPath();g.moveTo(...a);g.lineTo(...b);g.stroke()});g.restore();"
  "gg.pts.filter(q=>q.hook).forEach(q=>{const [x,y]=C(q.lat,q.lon),k=u*.12;g.save();g.translate(x,y);g.strokeStyle='#111';g.lineWidth=3*k;g.beginPath();g.moveTo(-14*k,-6*k);g.lineTo(14*k,-6*k);g.stroke();g.lineWidth=1.6*k;for(let t=-12;t<=12;t+=6){g.beginPath();g.moveTo(t*k,-6*k);g.lineTo((t-5)*k,-12*k);g.stroke()}g.strokeStyle='#dc2626';g.lineWidth=2.6*k;g.lineCap='round';g.beginPath();g.moveTo(-4*k,-6*k);g.lineTo(-4*k,2*k);g.arc(0,2*k,4*k,Math.PI,0,true);g.stroke();g.fillStyle=S2C;g.strokeStyle='#fff';g.lineWidth=1.2*k;g.beginPath();g.arc(0,6*k,3.2*k,0,7);g.fill();g.stroke();g.restore()})})}catch(e){}\n"
  "const r=.95*u;window.DPK=!!o.bigk;SH.forEach(p=>dpole(g,...C")
# PDF легенда (чертёж)
R("['l','Бронекабель от ТП (КЛ)','#c026d3',[2*u,1*u]],['t','Трансформаторная подстанция']];",
  "['l','Бронекабель от ТП (КЛ)','#c026d3',[2*u,1*u]],...(S2.length?[['l','СИП 2-я цепь (по опорам другого ТП)','#f97316',[]],['h','Крюк в своде арки']]:[]),['t','Трансформаторная подстанция']];")
R(" else{g.fillStyle='#1f2937';g.strokeStyle='#9ca3af';g.lineWidth=.35*u;g.fillRect(xx+1*u,yy-1.6*u,7*u,3.2*u);",
  " else if(it[0]=='h'){const k=u*.11,x0=xx+4.5*u,y0=yy;g.save();g.translate(x0,y0);g.strokeStyle='#111';g.lineWidth=3*k;g.beginPath();g.moveTo(-14*k,-6*k);g.lineTo(14*k,-6*k);g.stroke();g.lineWidth=1.6*k;for(let t=-12;t<=12;t+=6){g.beginPath();g.moveTo(t*k,-6*k);g.lineTo((t-5)*k,-12*k);g.stroke()}g.strokeStyle='#dc2626';g.lineWidth=2.6*k;g.lineCap='round';g.beginPath();g.moveTo(-4*k,-6*k);g.lineTo(-4*k,2*k);g.arc(0,2*k,4*k,Math.PI,0,true);g.stroke();g.fillStyle='#f97316';g.beginPath();g.arc(0,6*k,3.2*k,0,7);g.fill();g.restore()}\n else{g.fillStyle='#1f2937';g.strokeStyle='#9ca3af';g.lineWidth=.35*u;g.fillRect(xx+1*u,yy-1.6*u,7*u,3.2*u);")
# старая легенда
R("['#c026d3','Бронекабель от ТП (КЛ)',[2*u,1*u]]].forEach(","['#c026d3','Бронекабель от ТП (КЛ)',[2*u,1*u]],...(S2.length?[['#f97316','СИП 2-я цепь (по опорам другого ТП)',[]]]:[])].forEach(")
open(p,'w',encoding='utf-8').write(s);print('ok sip2',p)
