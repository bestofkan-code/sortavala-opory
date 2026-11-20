# Крюки в своде арки на обычных пролётах СИП (таблица hooks: uid, sp = ключ пролёта "uidA|uidB", lat, lon).
# Значок как у 2-й цепи (вариант В). В окне пролёта (редактор/монтаж) — кнопка «Крюк в арке» (ставит крюк в точку клика),
# в окне крюка — «Удалить крюк»; в редакторе крюк можно перетащить. В PDF-плане — значок и строка легенды «Крюк в своде арки».
import sys
p=sys.argv[1];s=open(p,encoding='utf-8').read()
def R(a,b,n=1):
    global s
    assert s.count(a)==n,(a[:90],s.count(a));s=s.replace(a,b)
JS=r"""
/* ---- Крюки в своде арки (таблица hooks) ---- */
var HK=[],HKJ='',HKLY=L.layerGroup().addTo(map);
function hkName(z){const k=String(z.sp||'').split('|');return (typeof pname=='function'?k.map(pname).join(' — '):z.sp)}
function hkCv(g,x,y,k,ball){g.save();g.translate(x,y);g.strokeStyle='#111';g.lineWidth=3*k;g.beginPath();g.moveTo(-14*k,-6*k);g.lineTo(14*k,-6*k);g.stroke();g.lineWidth=1.6*k;for(let t=-12;t<=12;t+=6){g.beginPath();g.moveTo(t*k,-6*k);g.lineTo((t-5)*k,-12*k);g.stroke()}g.strokeStyle='#dc2626';g.lineWidth=2.6*k;g.lineCap='round';g.beginPath();g.moveTo(-4*k,-6*k);g.lineTo(-4*k,2*k);g.arc(0,2*k,4*k,Math.PI,0,true);g.stroke();g.fillStyle=ball||'#f97316';g.strokeStyle='#fff';g.lineWidth=1.2*k;g.beginPath();g.arc(0,6*k,3.2*k,0,7);g.fill();g.stroke();g.restore()}
async function hkReq(m,q,body){const r=await fetch(CF.u+'/rest/v1/hooks'+q,{method:m,headers:{...H(),Prefer:'return=minimal'},body:body?JSON.stringify(body):undefined});if(!r.ok)throw new Error(await r.text())}
function hkPopup(z,ll){const d=document.createElement('div');d.className='pp';d.innerHTML='<div><b>Крюк в своде арки</b></div><div>пролёт '+esc(hkName(z))+'</div>'+(z.note?'<small>'+esc(z.note)+'</small>':'')+(RO?'':'<div class="r" style="margin-top:6px"><button data-hd style="color:#f87171">Удалить крюк</button></div><small>Крюк можно перетащить на место арки.</small>');
 if(!RO)d.querySelector('[data-hd]').onclick=async()=>{if(!confirm('Удалить крюк на пролёте '+hkName(z)+'?'))return;map.closePopup();try{await hkReq('DELETE','?uid=eq.'+encodeURIComponent(z.uid));HK=HK.filter(x=>x!==z);HKJ=JSON.stringify(HK);hkDraw();toast('Крюк удалён')}catch(e){toast('Не удалилось: '+(e.message||e))}};
 L.popup().setLatLng(ll).setContent(d).openOn(map)}
function hkDraw(){HKLY.clearLayers();const zm=map.getZoom();
 HK.forEach(z=>{const m=L.marker([+z.lat,+z.lon],{draggable:!RO,zIndexOffset:900,icon:L.divIcon({className:'',iconSize:[0,0],html:'<div style="position:absolute;left:0;top:0;transform:translate(-50%,-50%)">'+s2Hook()+'</div>'+(zm>=17?'<div style="position:absolute;left:0;top:20px;transform:translate(-50%,0);white-space:nowrap;font:600 11px Commissioner,Arial;padding:1px 5px;border-radius:5px;background:#111827;color:#fff">крюк в своде арки</div>':'')})}).addTo(HKLY);
  m.on('click',e=>{L.DomEvent.stop(e);hkPopup(z,e.latlng)});
  if(!RO)m.on('dragend',async()=>{const ll=m.getLatLng();z.lat=+ll.lat.toFixed(7);z.lon=+ll.lng.toFixed(7);try{await hkReq('PATCH','?uid=eq.'+encodeURIComponent(z.uid),{lat:z.lat,lon:z.lon,ed:WHO||null,updated_at:new Date().toISOString()});HKJ=JSON.stringify(HK);toast('Крюк перенесён')}catch(e){toast('Не сохранилось: '+(e.message||e))}})})}
async function hkAdd(k,ll){const z={uid:'hk'+Date.now().toString(36)+Math.random().toString(36).slice(2,5),sp:k,lat:+ll.lat.toFixed(7),lon:+ll.lng.toFixed(7),kind:'arch',ed:WHO||null};
 try{await hkReq('POST','',z);HK.push(z);HKJ=JSON.stringify(HK);hkDraw();toast('Крюк в арке добавлен — можно перетащить точнее')}catch(e){toast('Не сохранилось: '+(e.message||e))}}
async function hkLoad(){try{if(!CF)return;const r=await fetch(CF.u+'/rest/v1/hooks?select=*&order=uid',{headers:H()});const j=await r.json();if(!Array.isArray(j))return;const js=JSON.stringify(j);if(js===HKJ)return;HKJ=js;HK=j;hkDraw()}catch(e){}}
map.on('zoomend',()=>{if(HK.length)hkDraw()});
setTimeout(hkLoad,1600);setInterval(()=>{if(!document.hidden)hkLoad()},30000);
"""
R("async function sync(){LSYNC=Date.now();",JS+"\nasync function sync(){LSYNC=Date.now();")
# кнопка в окне пролёта
R("<button data-ld style=\"color:#f87171\">Удалить линию</button>'+(LE.has(k)?",
  "<button data-hk>Крюк в арке</button><button data-ld style=\"color:#f87171\">Удалить линию</button>'+(LE.has(k)?")
R("if(!RO){d.querySelector('[data-lp]').onclick=()=>{map.closePopup();leEdit(k)};",
  "if(!RO){d.querySelector('[data-lp]').onclick=()=>{map.closePopup();leEdit(k)};{const hb=d.querySelector('[data-hk]');if(hb)hb.onclick=()=>{map.closePopup();hkAdd(k,ll0||map.getCenter())}};")
# PDF: значки крюков
R("const r=.95*u;window.DPK=!!o.bigk;SH.forEach(p=>dpole(g,...C",
  "try{HK.forEach(z=>{const [x,y]=C(+z.lat,+z.lon);hkCv(g,x,y,u*.12)})}catch(e){}\nconst r=.95*u;window.DPK=!!o.bigk;SH.forEach(p=>dpole(g,...C")
# PDF: строка легенды
R("...(S2.length?[['l','СИП 2-я цепь (по опорам другого ТП)','#f97316',[]],['h','Крюк в своде арки']]:[])",
  "...(S2.length?[['l','СИП 2-я цепь (по опорам другого ТП)','#f97316',[]]]:[]),...(S2.length||HK.length?[['h','Крюк в своде арки']]:[])")
# PDF: строка легенды (обычная легенда)
R("g.fillStyle='#111';g.fillText(tx,px+8*u,y);y+=4.6*u})}\nconst ST=L=>",
  "g.fillStyle='#111';g.fillText(tx,px+8*u,y);y+=4.6*u});if(S2.length||HK.length){try{hkCv(g,px+3*u,y+.6*u,u*.11)}catch(e){}g.fillStyle='#111';g.fillText('Крюк в своде арки',px+8*u,y);y+=4.6*u}}\nconst ST=L=>")
open(p,'w',encoding='utf-8').write(s);print('ok hooks',p)
