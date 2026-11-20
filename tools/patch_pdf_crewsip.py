# PDF-план для бригады СИП: подписи номеров опор и крупные кронштейны (цвет по типу, как на карте).
# Галочки в блоке «PDF общего плана»: «номера опор» (#pdl) и «крупные кронштейны» (#pdk), обе включены по умолчанию.
import sys
p=sys.argv[1];s=open(p,encoding='utf-8').read()
def R(a,b):
    global s
    assert s.count(a)==1,(a[:80],s.count(a));s=s.replace(a,b)
# 1) кронштейны в dpole: крупный режим (DPK)
OLD="{const n=armN(p),ins=wdone(p,12),sv=Math.min(2,+p.sv||0),AL=r*2.5;armAng(n,+p.ka).forEach("
NEW=("{const n=armN(p),ins=wdone(p,12),sv=Math.min(2,+p.sv||0),AL=r*2.5;"
 "if(window.DPK){const AK=r*4.6,S0=r*1.2,col=armCol(p),W=Math.max(2,r*.6);armAng(n,+p.ka).forEach((a,i)=>{const t=a*Math.PI/180,c=Math.cos(t),sn=Math.sin(t),sx=x+S0*c,sy=y+S0*sn,ex=x+AK*c,ey=y+AK*sn;"
 "g.setLineDash([]);g.lineCap='round';g.beginPath();g.moveTo(sx,sy);g.lineTo(ex,ey);g.strokeStyle='#fff';g.lineWidth=W*2.1;g.stroke();"
 "g.beginPath();g.moveTo(sx,sy);g.lineTo(ex,ey);g.strokeStyle=col;g.lineWidth=W;g.lineCap=ins?'round':'butt';g.setLineDash(ins?[]:[W*1.8,W*1.1]);g.stroke();g.setLineDash([]);g.lineCap='round';"
 "const R=r*.95;if(i<sv||ins){g.beginPath();g.arc(ex,ey,R,0,7);g.fillStyle=i<sv?'#facc15':'#fff';g.fill();g.strokeStyle=i<sv?'#854d0e':col;g.lineWidth=W*.55;g.stroke()}})}"
 "else armAng(n,+p.ka).forEach(")
R(OLD,NEW)
# 2) подписи номеров опор
OLD2="const r=.95*u;SH.forEach(p=>dpole(g,...C(p.lat,p.lon),p,r));"
NEW2=("const r=.95*u;window.DPK=!!o.bigk;SH.forEach(p=>dpole(g,...C(p.lat,p.lon),p,r));"
 "if(o.lab){const fz=2.3*u,PT=SH.map(p=>C(p.lat,p.lon)),BX=[],hit=(a,b)=>a[0]<b[2]&&b[0]<a[2]&&a[1]<b[3]&&b[1]<a[3];g.font=`bold ${fz}px ${F}`;g.textAlign='left';g.textBaseline='middle';"
 "SH.forEach((p,i)=>{const t=String(p.n||p.id||'');if(!t)return;const [x,y]=PT[i],w=g.measureText(t).width,h=fz*1.05,d=r*1.7,"
 "cs=[[x-w/2,y+d],[x+d,y+d*.35],[x-d-w,y+d*.35],[x+d*.9,y+d],[x-d*.9-w,y+d],[x-w/2,y+d*2.4],[x+d,y-h],[x-d-w,y-h],[x-w/2,y-d*3.2-h]];"
 "let best=null,bo=1e9;for(const [cx,cy] of cs){const b=[cx-1,cy-1,cx+w+1,cy+h+1];let ov=BX.filter(q=>hit(b,q)).length*3;PT.forEach((q,j)=>{if(j!=i&&q[0]>b[0]-r&&q[0]<b[2]+r&&q[1]>b[1]-r&&q[1]<b[3]+r)ov++});if(ov<bo){bo=ov;best=b;if(!ov)break}}"
 "BX.push(best);g.lineJoin='round';g.strokeStyle='rgba(255,255,255,.95)';g.lineWidth=fz*.32;g.strokeText(t,best[0]+1,best[1]+1+h/2);g.fillStyle='#111';g.fillText(t,best[0]+1,best[1]+1+h/2)});g.lineJoin='miter'}")
R(OLD2,NEW2)
# 3) легенда: в крупном режиме — типы кронштейнов, строки повыше
OLD3="['Кронштейн 1-рожк. (проект)',{t:'S',kr:1}],['Кронштейн 2-рожк. установлен',{t:'S',kr:2,w:{12:'x'}}],['Светильник установлен (1 из 2)',{t:'S',kr:2,sv:1,w:{12:'x'}}],"
NEW3=("...(window.DPK?[['Кронштейн 1-рожковый',{t:'S',kr:1}],['Кронштейн 2-рожк. 90°',{t:'S',kr:2,ka:90}],['Кронштейн 2-рожк. 180°',{t:'S',kr:2,ka:180}],['Кронштейн установлен',{t:'S',kr:2,ka:180,w:{12:'x'}}],['Светильники установлены',{t:'S',kr:2,ka:180,sv:2,w:{12:'x'}}]]"
 ":[['Кронштейн 1-рожк. (проект)',{t:'S',kr:1}],['Кронштейн 2-рожк. установлен',{t:'S',kr:2,w:{12:'x'}}],['Светильник установлен (1 из 2)',{t:'S',kr:2,sv:1,w:{12:'x'}}]]),")
R(OLD3,NEW3)
OLD4="].forEach(([tx,f])=>{dpole(g,px+3*u,y,Object.assign({uid:'p0',w:{}},f),1.1*u);g.fillStyle='#111';g.font=`${fs}px ${F}`;g.textBaseline='middle';g.fillText(tx,px+8*u,y);y+=4.6*u});"
NEW4=("].forEach(([tx,f])=>{const bk=window.DPK&&f.kr;if(bk)y+=1.8*u;dpole(g,bk?px+4.2*u:px+3*u,y,Object.assign({uid:'p0',w:{}},f),bk?.72*u:1.1*u);g.fillStyle='#111';g.font=`${fs}px ${F}`;g.textBaseline='middle';g.fillText(tx,px+(bk?10:8)*u,y);y+=bk?5*u:4.6*u});"
 "if(o.lab){g.font=`bold ${2.6*u}px ${F}`;g.textAlign='center';g.lineJoin='round';g.strokeStyle='#fff';g.lineWidth=.8*u;g.strokeText('12',px+3*u,y);g.fillStyle='#111';g.fillText('12',px+3*u,y);g.textAlign='left';g.lineJoin='miter';g.font=`${fs}px ${F}`;g.fillText('Номер опоры',px+8*u,y);y+=4.6*u}")
R(OLD4,NEW4)
# сброс флага в конце buildPlan
R("`Масштаб подложки: z${z}`,CW-pad,CH-5*u);\nreturn cv}","`Масштаб подложки: z${z}`,CW-pad,CH-5*u);window.DPK=false;\nreturn cv}")
# 4) UI и передача опций
R('<div class="r">Область: <select id="parea"','<div class="r"><label><input type="checkbox" id="pdl" checked> номера опор</label> <label><input type="checkbox" id="pdk" checked> крупные кронштейны</label></div><div class="r">Область: <select id="parea"')
R("const cv=await buildPlan({only:ar.only||null,bb:ar.bb,title:ar.title,paper:$('pq').value,","const cv=await buildPlan({only:ar.only||null,bb:ar.bb,title:ar.title,lab:$('pdl').checked,bigk:$('pdk').checked,paper:$('pq').value,")
open(p,'w',encoding='utf-8').write(s);print('ok crewsip',p)
