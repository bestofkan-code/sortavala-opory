#!/usr/bin/env python3
"""Заливка участков 1 и 2 по смете вместо отметок границы (после patch_uch.py).
- Убирает пунктирные отметки границы участков.
- Под кнопкой «№» (номера опор) — кнопка «1|2»: включает и выключает заливку вдоль линий:
  синим — участок 1, оранжевым — участок 2 (ТП22, 29, 89, 90, 97 и 7 опор «у2»).
  Пролёт между опорами разных участков делится пополам — там и видна граница.
Применение:
  for f in redaktor.html prosmotr.html zamechaniya.html zamechaniya-prosmotr.html montazh.html uchastki.html; do python3 tools/patch_uch_fill.py $f; done
"""
import sys
path = sys.argv[1]
s = open(path, encoding='utf-8').read()
if 'id="ufbtn"' in s:
    print('already applied', path); sys.exit(0)
def R(old, new, cnt=1):
    global s
    n = s.count(old); assert n == cnt, (path, old[:80], n); s = s.replace(old, new)

# 1) без отметок границы
R("var UCCUT=[['p12','n17927456599451cnp'],['p128','p125']];", "var UCCUT=[];")

# 2) кнопка сразу под «№»
R("new C().addTo(map);setTimeout(()=>{nbtnUI();numLabels()},0)}",
  "new C().addTo(map);setTimeout(()=>{nbtnUI();numLabels()},0)}\n"
  "{const C=L.Control.extend({options:{position:'topleft'},onAdd(){const d=L.DomUtil.create('div','leaflet-bar');"
  "d.innerHTML='<a href=\"#\" id=\"ufbtn\" title=\"Заливка участков 1 и 2 по смете\" style=\"display:flex;align-items:center;justify-content:center;font:800 12px/30px system-ui,sans-serif\">1|2</a>';"
  "L.DomEvent.disableClickPropagation(d);d.querySelector('a').onclick=e=>{e.preventDefault();if(typeof ufToggle=='function')ufToggle()};return d}});new C().addTo(map)}")

JS = r"""
<script>
var UFON=false;try{UFON=localStorage.getItem(KEY+'_ufill')==='1'}catch(e){}
var UFLY=null,UFL=[],UFR=40,UFC={1:'#2563eb',2:'#f97316'};
function ufW(){const z=map.getZoom(),mpp=40075016.686*Math.cos(61.71*Math.PI/180)/Math.pow(2,z+8);return Math.max(14,2*UFR/mpp)}
function ufUI(){const a=document.getElementById('ufbtn');if(a){a.style.background=UFON?'#7c3aed':'';a.style.color=UFON?'#fff':''}let g=document.getElementById('uflg');if(!g){g=document.createElement('div');g.id='uflg';g.style.cssText='position:absolute;left:50%;transform:translateX(-50%);top:10px;z-index:1000;background:rgba(17,24,39,.85);color:#fff;font:600 12px/1.5 system-ui,sans-serif;padding:5px 9px;border-radius:6px;pointer-events:none';g.innerHTML='<span style="display:inline-block;width:12px;height:12px;background:#2563eb;border-radius:3px;vertical-align:-2px"></span> участок 1 &nbsp; <span style="display:inline-block;width:12px;height:12px;background:#f97316;border-radius:3px;vertical-align:-2px"></span> участок 2 (по смете)';map.getContainer().appendChild(g)}g.style.display=UFON?'':'none'}
function ufDraw(){try{
 if(!map.getPane('ucp')){const p=map.createPane('ucp');p.style.zIndex=450;p.style.opacity=.5;p.style.pointerEvents='none'}
 if(!UFLY)UFLY=L.layerGroup().addTo(map);UFLY.clearLayers();UFL=[];ufUI();if(!UFON)return;
 const alive=p=>p&&p.tp&&!(p.x&&!p.sx),w=ufW(),line=(A,B,u)=>{const l=L.polyline([A,B],{pane:'ucp',color:UFC[u],weight:w,opacity:1,lineCap:'round',lineJoin:'round',interactive:false});UFL.push(l);UFLY.addLayer(l)};
 let E=[];try{E=netEdges().E||[]}catch(e){}
 E.forEach(([a,b])=>{if(!alive(a)||!alive(b))return;const ua=ucOf(a),ub=ucOf(b),A=[a.lat,a.lon],B=[b.lat,b.lon];
  if(ua==ub)line(A,B,ua);else{const M=[(a.lat+b.lat)/2,(a.lon+b.lon)/2];line(A,M,ua);line(M,B,ub)}});
 P.forEach(p=>{if(!alive(p))return;UFLY.addLayer(L.circle([p.lat,p.lon],{pane:'ucp',radius:UFR,stroke:false,fillColor:UFC[ucOf(p)],fillOpacity:1,interactive:false}))});
}catch(e){console.log('ufDraw',e)}}
function ufToggle(){UFON=!UFON;try{localStorage.setItem(KEY+'_ufill',UFON?'1':'0')}catch(e){}ufDraw();
 if(typeof toast=='function')toast(UFON?'Участки по смете: синий — участок 1, оранжевый — участок 2':'Заливка участков скрыта')}
(function(){map.on('zoomend',()=>{if(UFON){const w=ufW();UFL.forEach(l=>l.setStyle({weight:w}))}});
 let t=0;const sch=()=>{clearTimeout(t);t=setTimeout(()=>{if(UFON)ufDraw()},300)};
 try{const _s=stats;stats=function(){const r=_s.apply(this,arguments);try{sch()}catch(e){}return r}}catch(e){}
 setTimeout(ufDraw,800);setTimeout(ufDraw,3500)})();
</script>
"""
i = s.rfind('</body>'); assert i > 0, path
s = s[:i] + JS + s[i:]
open(path, 'w', encoding='utf-8').write(s); print('ok', path)
