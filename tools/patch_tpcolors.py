# Линии СИП: ярче и различимее по ТП. Палитра из 10 контрастных цветов, соседние ТП (опоры в пределах 150 м)
# получают разные цвета; белая окантовка под линией, линии толще; метки «ТП29» на линиях при zoom ≥ 17.
# PDF-план: линии тоже в цвет ТП, в легенде — строки «ТПxx» с цветом.
import sys
p=sys.argv[1];s=open(p,encoding='utf-8').read()
def R(a,b,n=1):
    global s
    assert s.count(a)==n,(a[:90],s.count(a));s=s.replace(a,b)
R("var TPCL=['#2563eb','#16a34a','#9333ea','#db2777','#0891b2','#ca8a04','#4f46e5','#059669','#c2410c','#0d9488','#0284c7','#65a30d','#1e40af','#a21caf','#b45309','#7c3aed','#0e7490','#15803d'],TPCM=null,PBU=null;",
  "var TPCL=['#0057ff','#00a651','#8b2cf5','#00b4d8','#d4a300','#8b4513','#ff4f9a','#66bb00','#00695c','#1f1f99'],TPCM=null,PBU=null;")
R("function tpCol(t){t=String(t||'');if(!TPCM||!TPCM.has(t)){TPCM=new Map(tpList().map((x,i)=>[x,TPCL[i%TPCL.length]]))}return TPCM.get(t)||'#475569'}",
  "function tpCol(t){t=String(t||'');if(!TPCM||!TPCM.has(t)){const L0=tpList(),K=111320*Math.cos(61.71*Math.PI/180),A=new Map(L0.map(x=>[x,new Set()])),Q=P.filter(p=>p.tp&&!p.x);"
  "for(let i=0;i<Q.length;i++)for(let j=i+1;j<Q.length;j++){const a=Q[i],b=Q[j],ta=String(a.tp),tb=String(b.tp);if(ta==tb||A.get(ta).has(tb))continue;if(Math.hypot((a.lon-b.lon)*K,(a.lat-b.lat)*110574)<150){A.get(ta).add(tb);A.get(tb).add(ta)}}"
  "TPCM=new Map();[...L0].sort((x,y)=>A.get(y).size-A.get(x).size||x.localeCompare(y,'ru',{numeric:true})).forEach(x=>{const used=new Set([...A.get(x)].map(y=>TPCM.get(y)).filter(Boolean));const cnt=new Map(TPCL.map(c=>[c,0]));TPCM.forEach(c=>cnt.set(c,(cnt.get(c)||0)+1));"
  "const rgb=c=>[1,3,5].map(i=>parseInt(c.slice(i,i+2),16)),dd=(a,b)=>{const A=rgb(a),B=rgb(b);return Math.hypot(A[0]-B[0],A[1]-B[1],A[2]-B[2])},md=c=>used.size?Math.min(...[...used].map(u=>dd(c,u))):999;const free=TPCL.filter(c=>!used.has(c));TPCM.set(x,(free.length?free:TPCL).sort((a,b)=>(Math.round(md(b)/60)-Math.round(md(a)/60))||(cnt.get(a)-cnt.get(b)))[0])})}return TPCM.get(t)||'#475569'}")
# карта: окантовка, толщина, метки ТП
R("const pa=pbu(ua),pq=pbu(ub),tc=pa&&pq&&String(pa.tp||'')==String(pq.tp||'')?tpCol(pa.tp):'#475569';L.polyline(path,has?{color:tc,weight:5,opacity:.95,interactive:false}:{color:tc,weight:3,opacity:.85,dashArray:dash,interactive:false}).addTo(ll);",
  "const pa=pbu(ua),pq=pbu(ub),same=pa&&pq&&String(pa.tp||'')==String(pq.tp||''),tc=same?tpCol(pa.tp):'#475569';L.polyline(path,{color:'#fff',weight:has?9:7,opacity:.85,interactive:false}).addTo(ll);L.polyline(path,has?{color:tc,weight:6,opacity:1,interactive:false}:{color:tc,weight:4,opacity:1,dashArray:dash,interactive:false}).addTo(ll);"
  "if(same){window.TPTG=window.TPTG||{};const t=String(pa.tp),n=(TPTG[t]=(TPTG[t]||0)+1);if(n%4==2&&!has)L.marker(path.length>2?path[Math.floor(path.length/2)]:[(a[0]+b[0])/2,(a[1]+b[1])/2],{interactive:false,icon:L.divIcon({className:'',iconSize:[0,0],html:'<div class=\"tpt\" style=\"background:'+tc+'\">'+esc(SHD(tpn(t)))+'</div>'})}).addTo(ll)}")
R("function lines(){ll.clearLayers();","function lines(){ll.clearLayers();window.TPTG={};")
R("function lines(){ll.clearLayers();window.TPTG={};","document.head.insertAdjacentHTML('beforeend','<style>.tpt{display:none;position:absolute;transform:translate(-50%,-50%);width:max-content;color:#fff;font:700 10px system-ui,sans-serif;padding:1px 5px;border-radius:6px;box-shadow:0 0 0 1.5px #fff,0 1px 3px rgba(0,0,0,.35);pointer-events:none}.z17 .tpt{display:block}</style>');\nsetTimeout(()=>{const f=()=>map.getContainer().classList.toggle('z17',map.getZoom()>=17);map.on('zoomend',f);f()},0);\nfunction lines(){ll.clearLayers();window.TPTG={};")
# PDF: линии в цвет ТП
R("DLC.forEach(sg=>{const ua='p'+sg[0][0],ub='p'+sg[1][0];if(NT.SK.has(ua<ub?ua+'|'+ub:ub+'|'+ua))return;const a=pt(sg[0]),b=pt(sg[1]);if(a&&b){g.setLineDash(sg[2]?[lw*4,lw*3]:[]);",
  "const tcP=(x,y)=>x&&y&&String(x.tp||'')==String(y.tp||'')?tpCol(x.tp):'#475569',TPU=new Set(),inBB=q=>q&&q.lat>=BB.s&&q.lat<=BB.n&&q.lon>=BB.w&&q.lon<=BB.e;DLC.forEach(sg=>{const ua='p'+sg[0][0],ub='p'+sg[1][0];if(NT.SK.has(ua<ub?ua+'|'+ub:ub+'|'+ua))return;const a=pt(sg[0]),b=pt(sg[1]);if(a&&b){const x=U.get(ua),y=U.get(ub);g.strokeStyle=tcP(x,y);if(x&&y&&x.tp==y.tp&&(inBB(x)||inBB(y)))TPU.add(String(x.tp));g.setLineDash(sg[2]?[lw*4,lw*3]:[]);")
R("NT.E.filter(e=>(e[2]!='d'||e.pts)&&SHS.has(e[0])&&SHS.has(e[1])).forEach(e=>{const[a,b,c]=e;g.setLineDash(c=='n'||c=='r'?[lw*4,lw*3]:[]);",
  "NT.E.filter(e=>(e[2]!='d'||e.pts)&&SHS.has(e[0])&&SHS.has(e[1])).forEach(e=>{const[a,b,c]=e;g.strokeStyle=tcP(a,b);if(String(a.tp||'')==String(b.tp||'')&&(inBB(a)||inBB(b)))TPU.add(String(a.tp));g.lineWidth=lw*2;g.setLineDash(c=='n'||c=='r'?[lw*4,lw*3]:[]);")
# PDF легенда (чертёж): строки ТП с цветом вместо «Линия ВЛ (по чертежу)»
R("['l','Линия ВЛ (по чертежу)','#1d4ed8',[]],","...[...TPU].sort((x,y)=>x.localeCompare(y,'ru',{numeric:true})).map(t=>['l','Линия СИП '+SHD(tpn(t)),tpCol(t),[]]),['l','Линия между ТП','#475569',[]],")
R("['#1d4ed8','Линия ВЛ (по чертежу)',[]],","...[...TPU].sort((x,y)=>x.localeCompare(y,'ru',{numeric:true})).map(t=>[tpCol(t),'Линия СИП '+SHD(tpn(t)),[]]),")
open(p,'w',encoding='utf-8').write(s);print('ok tpcolors',p)
