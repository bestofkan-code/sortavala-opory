#!/usr/bin/env python3
"""Участки 1 и 2 по смете — только обозначение на карте, данные опор не меняются.
- 7 опор, которые по исполнительной схеме и смете отнесены к участку 2, хотя питаются от ТП60 и ТП98:
  ТП60-32…35 и ТП98-41…43 (по uid, номера могут меняться). Рядом с ними всегда виден значок «у2»,
  в карточке опоры — пометка «участок 2 по смете».
- Две отметки границы участков: между ТП60-31 и ТП60-32, между ТП98-40 и ТП98-41.
- Кнопка «Участки 1 / 2 по смете»: у всех опор значок с номером участка
  (участок 2 — ТП22, 29, 89, 90, 97 и эти 7 опор, остальное — участок 1).
Применение:
  for f in redaktor.html prosmotr.html zamechaniya.html zamechaniya-prosmotr.html montazh.html uchastki.html; do python3 tools/patch_uch.py $f; done
"""
import sys
path = sys.argv[1]
s = open(path, encoding='utf-8').read()
if 'id="ucb"' in s:
    print('already applied', path); sys.exit(0)
def R(old, new, cnt=1):
    global s
    n = s.count(old); assert n == cnt, (path, old[:80], n); s = s.replace(old, new)

# кнопка под «Нужен котлован под заземление»
R('<button class="b" id="gzb" style="border-color:#65a30d">Нужен котлован под заземление</button><small id="gzs"></small></div>',
  '<button class="b" id="gzb" style="border-color:#65a30d">Нужен котлован под заземление</button><small id="gzs"></small></div>'
  '<div class="r"><button class="b" id="ucb" style="border-color:#7c3aed">Участки 1 / 2 по смете</button><small id="ucs"></small></div>')

# пометка в карточке опоры (после «был …»)
OLD = "был '+esc(p.oid)+'</small>':''}"
n = s.count(OLD); assert n >= 1, (path, 'oid snippet', n)
s = s.replace(OLD, OLD + "${(typeof UCOV!='undefined'&&UCOV.has(p.uid))?' <small style=\"color:#7c3aed;font-weight:600\" title=\"По смете и исполнительной схеме опора относится к участку 2. На месте и на карте ничего не меняется: питание от своей ТП.\">участок 2 по смете</small>':''}")

JS = r"""
<script>
var UCOV=new Set(['n17927456599451cnp','p503','p504','p501','p125','n1794778042473tnry','p122']);
var UCCUT=[['p12','n17927456599451cnp'],['p128','p125']];
var UC2TP=new Set(['22','29','89','90','97']);
var UCF=false;try{UCF=localStorage.getItem(KEY+'_ucf')==='1'}catch(e){}
function ucOf(p){return UCOV.has(p.uid)?2:(UC2TP.has(String(p.tp))?2:1)}
function ucK(p){return !p.x&&!p.pp&&!isG(p)}
var UCLY=null,UCT=0;function ucSched(){clearTimeout(UCT);UCT=setTimeout(ucDraw,150)}
function ucDraw(){try{
 if(!UCLY)UCLY=L.layerGroup().addTo(map);UCLY.clearLayers();
 const by=new Map(P.map(p=>[p.uid,p])),tip='По смете и исполнительной схеме — участок 2. На месте ничего не меняется, питание от своей ТП.';
 const badge=(p,txt,bg,bd,t)=>{const m=L.marker([p.lat,p.lon],{icon:L.divIcon({className:'',html:'<span style="display:inline-block;min-width:14px;padding:0 3px;font:700 10px/14px sans-serif;color:#fff;background:'+bg+';border:1.5px solid '+bd+';border-radius:7px;text-align:center;white-space:nowrap">'+txt+'</span>',iconSize:null,iconAnchor:[-7,20]}),zIndexOffset:900,keyboard:false});if(t)m.bindTooltip(t,{direction:'top'});UCLY.addLayer(m)};
 if(UCF){P.forEach(p=>{if(!ucK(p)||!vis(p)||UCOV.has(p.uid))return;const u=ucOf(p);badge(p,String(u),u==2?'#ea580c':'#2563eb','#fff','Участок '+u+' по смете')})}
 UCOV.forEach(id=>{const p=by.get(id);if(p&&!p.x&&vis(p))badge(p,'у2','#7c3aed','#fff',p.id+': '+tip)});
 UCCUT.forEach(([a,b])=>{const A=by.get(a),B=by.get(b);if(!A||!B)return;const la=(A.lat+B.lat)/2,lo=(A.lon+B.lon)/2,dx=(B.lon-A.lon)*K1,dy=(B.lat-A.lat)*110950,d=Math.hypot(dx,dy)||1,h=9,px=-dy/d*h,py=dx/d*h;
  UCLY.addLayer(L.polyline([[la-py/110950,lo-px/K1],[la+py/110950,lo+px/K1]],{color:'#7c3aed',weight:5,dashArray:'4 3',opacity:.95}).bindTooltip('Граница участков по смете: '+A.id+' — участок 1 | '+B.id+' — участок 2',{direction:'top'}))});
 const b=$('ucb');if(b){b.style.background=UCF?'#7c3aed':'';b.style.color=UCF?'#fff':'';b.textContent=UCF?'Участки по смете показаны ✕':'Участки 1 / 2 по смете'}
 const K=P.filter(ucK),n2=K.filter(p=>ucOf(p)==2).length;if($('ucs'))$('ucs').innerHTML='участок 1: <b>'+(K.length-n2)+'</b>, участок 2: <b>'+n2+'</b> (из них '+[...UCOV].filter(u=>by.has(u)).length+' «у2» — по смете)';
}catch(e){console.log('ucDraw',e)}}
(function(){const b=document.getElementById('ucb');if(b)b.onclick=()=>{UCF=!UCF;try{localStorage.setItem(KEY+'_ucf',UCF?'1':'0')}catch(e){}ucDraw()};
 try{const _s=stats;stats=function(){const r=_s.apply(this,arguments);try{ucSched()}catch(e){}return r}}catch(e){}
 try{const _n=numLabels;numLabels=function(){const r=_n.apply(this,arguments);try{ucSched()}catch(e){}return r}}catch(e){}
 setTimeout(ucDraw,500);setTimeout(ucDraw,3000)})();
</script>
"""
i = s.rfind('</body>'); assert i > 0, path
s = s[:i] + JS + s[i:]
open(path, 'w', encoding='utf-8').write(s); print('ok', path)
