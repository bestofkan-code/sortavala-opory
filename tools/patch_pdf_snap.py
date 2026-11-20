# «PDF как на карте (снимок)»: печать карты ровно как на экране (все значки, линии, подписи, подложка),
# только текущий вид экрана (что приближено и какие опоры видны), лист A3/A4, + номера опор вида «ТП97-15».
import sys
p=sys.argv[1];s=open(p,encoding='utf-8').read()
def R(a,b,n=1):
    global s
    assert s.count(a)==n,(a[:90],s.count(a));s=s.replace(a,b)
R('<div class="r"><button id="pdfb">Скачать PDF общего плана</button></div>',
  '<div class="r"><button id="pdfb">Скачать PDF общего плана</button></div><div class="r"><button id="pdfs" title="Снимок той части карты, что сейчас на экране: видимые опоры, значки, подписи и номера опор">PDF как на экране (снимок)</button></div>')
JS=r"""
async function pdfSnap(){const st=$('pst'),A3=$('pq').value=='A3',btn=$('pdfs');if(btn.disabled)return;
try{btn.disabled=true;let FL=[];try{FL=pdfFlt()}catch(e){}const tp0=(typeof FTS!='undefined'&&FTS.size)?[...FTS].map(t=>tpn(t)).join(', '):'',dt=new Date().toLocaleDateString('ru-RU'),ar={title:'Как на экране'+(tp0?' · '+tp0:'')+(FL.length?' · '+FL.join(' · '):''),file:('Как на карте'+(tp0?' — '+tp0:'')+(FL.length?' — '+FL.join(', '):'')+' — '+dt).replace(/[\\/:*?"<>|]/g,' ').slice(0,150)+'.pdf'};
 st.textContent='Снимаю карту в фоне… (несколько секунд не двигайте карту)';toast('Снимаю карту для PDF — несколько секунд не двигайте карту');
 if(!window.htmlToImage)await loadScript('https://cdn.jsdelivr.net/npm/html-to-image@1.11.11/dist/html-to-image.js');
 if(!window.jspdf)await loadScript('https://cdnjs.cloudflare.com/ajax/libs/jspdf/2.5.1/jspdf.umd.min.js');
 const el=map.getContainer(),w=el.clientWidth,h=el.clientHeight,PW=A3?420:297,PH=A3?297:210,pr=Math.min(4,(A3?6400:4800)/Math.max(w,h));
 // номера опор — по положению на момент нажатия
 const LB=[];if($('pdl').checked){const fz=12*pr,PT=[],SHW=[];P.forEach(p=>{if(p.x)return;const m=mk.get(p);if(!m||!map.hasLayer(m))return;const c=map.latLngToContainerPoint([p.lat,p.lon]);if(c.x<-20||c.y<-20||c.x>w+20||c.y>h+20)return;PT.push([c.x*pr,c.y*pr]);SHW.push(p)});
  const mc=document.createElement('canvas').getContext('2d'),BX=[],hit=(a,b)=>a[0]<b[2]&&b[0]<a[2]&&a[1]<b[3]&&b[1]<a[3],r=9*pr;mc.font=`bold ${fz}px Arial`;
  SHW.forEach((p,i)=>{const t=SHD(String(p.id||'').replace(/^КТП\s+/,'КТП')),[x,y]=PT[i],tw=mc.measureText(t).width,th=fz*1.1,d=r*1.4,
   cs=[[x-tw/2,y+d],[x+d,y+d*.3],[x-d-tw,y+d*.3],[x+d,y+d],[x-d-tw,y+d],[x-tw/2,y+d*2],[x+d,y-th-d*.2],[x-d-tw,y-th-d*.2],[x-tw/2,y-d*2.4-th]];
   let best=null,bo=1e9;for(const [cx,cy] of cs){const b=[cx-2,cy-2,cx+tw+2,cy+th+2];let o2=BX.filter(q=>hit(b,q)).length*3;PT.forEach((q,j)=>{if(j!=i&&q[0]>b[0]-r&&q[0]<b[2]+r&&q[1]>b[1]-r&&q[1]<b[3]+r)o2++});if(o2<bo){bo=o2;best=b;if(!o2)break}}
   BX.push(best);LB.push([t,best[0]+2,best[1]+2+th/2,fz])})}
 const mcv=await htmlToImage.toCanvas(el,{pixelRatio:pr,cacheBust:false,skipFonts:true,imagePlaceholder:'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII=',filter:n=>!(n.classList&&(n.classList.contains('leaflet-control-container')||n.classList.contains('nlab')||n.classList.contains('leaflet-popup-pane')))});
 st.textContent='Собираю PDF…';
 {const g=mcv.getContext('2d');g.textBaseline='middle';g.textAlign='left';g.lineJoin='round';LB.forEach(([t,x,y,fz])=>{g.font=`bold ${fz}px Arial`;g.strokeStyle='rgba(255,255,255,.95)';g.lineWidth=fz*.35;g.strokeText(t,x,y);g.fillStyle='#111';g.fillText(t,x,y)})}
 // лист: снимок целиком, по центру, подпись снизу
 const CW=A3?7200:5100,CH=Math.round(CW*PH/PW),cv=document.createElement('canvas');cv.width=CW;cv.height=CH;const g=shdCtx(cv.getContext('2d'));g.fillStyle='#fff';g.fillRect(0,0,CW,CH);
 const fz=CW/120,cap=fz*3.2,m=CW/70,sc=Math.min((CW-2*m)/mcv.width,(CH-2*m-cap)/mcv.height),iw=mcv.width*sc,ih=mcv.height*sc,ix=(CW-iw)/2,iy=m;g.drawImage(mcv,ix,iy,iw,ih);g.strokeStyle='#999';g.lineWidth=2;g.strokeRect(ix,iy,iw,ih);
 g.fillStyle='#111';g.textBaseline='alphabetic';g.font=`bold ${fz}px Arial`;g.fillText(ar.title+' · по состоянию на '+dt,ix,iy+ih+fz*1.4);g.font=`${fz*.8}px Arial`;g.fillStyle='#555';g.fillText(($('pbm').value=='esri'?'Подложка: Esri World Imagery':'Подложка: © участники OpenStreetMap')+' · положение опор приблизительное',ix,iy+ih+fz*2.6);
 const{jsPDF}=window.jspdf,doc=new jsPDF({orientation:'landscape',unit:'mm',format:A3?'a3':'a4',compress:true});doc.addImage(cv.toDataURL('image/jpeg',.9),'JPEG',0,0,PW,PH);doc.save(ar.file);st.textContent='Готово: файл сохранён';toast('PDF готов')}
catch(e){st.textContent='Ошибка: '+(e.message||e)}finally{btn.disabled=false}}
$('pdfs').onclick=pdfSnap;
"""
R("$('pdfb').onclick=pdfPlan;","$('pdfb').onclick=pdfPlan;"+JS)
open(p,'w',encoding='utf-8').write(s);print('ok snap',p)
