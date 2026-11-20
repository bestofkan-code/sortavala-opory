# «PDF как на карте (снимок)»: печать карты ровно как на экране (все значки, линии, подписи, подложка),
# крупно, на лист A3/A4, + номера опор вида «ТП97-15». Область — из «Область:» (опоры в работе / все / как на экране).
import sys
p=sys.argv[1];s=open(p,encoding='utf-8').read()
def R(a,b,n=1):
    global s
    assert s.count(a)==n,(a[:90],s.count(a));s=s.replace(a,b)
R('<div class="r"><button id="pdfb">Скачать PDF общего плана</button></div>',
  '<div class="r"><button id="pdfb">Скачать PDF общего плана</button></div><div class="r"><button id="pdfs" title="Снимок карты как на экране: все значки и подписи, плюс номера опор">PDF как на карте (снимок)</button></div>')
JS=r"""
async function pdfSnap(){const st=$('pst'),A3=$('pq').value=='A3',sleep=t=>new Promise(r=>setTimeout(r,t));let ov=null,el=null,sv=null,c0=null,z0=null,b0=0,hadN=false;
try{const ar=pdfArea();if(!ar)return st.textContent='Нет опор под текущими фильтрами.';st.textContent='Готовлю снимок карты…';
 if(!window.htmlToImage)await loadScript('https://cdn.jsdelivr.net/npm/html-to-image@1.11.11/dist/html-to-image.js');
 if(!window.jspdf)await loadScript('https://cdnjs.cloudflare.com/ajax/libs/jspdf/2.5.1/jspdf.umd.min.js');
 map.closePopup();el=map.getContainer();sv=el.getAttribute('style')||'';c0=map.getCenter();z0=map.getZoom();try{b0=map.getBearing?map.getBearing():0}catch(e){}
 const isView=$('parea').value=='view',bb=ar.bb,B=isView?map.getBounds():L.latLngBounds([bb.s,bb.w],[bb.n,bb.e]).pad(.05),PW=A3?420:297,PH=A3?297:210,asp=PW/PH,MAXP=A3?5600:4200;
 let Z=isView?Math.min(19,z0):18,w,h;const dim=()=>{const a=map.project(B.getNorthWest(),Z),b=map.project(B.getSouthEast(),Z);w=Math.max(200,b.x-a.x);h=Math.max(200,b.y-a.y);if(w/h<asp)w=h*asp;else h=w/asp};dim();while(Math.max(w,h)>MAXP&&Z>13){Z-=.25;dim()}w=Math.round(w);h=Math.round(h);
 ov=document.createElement('div');ov.style.cssText='position:fixed;inset:0;z-index:2147483000;background:#11141c;color:#eef1f7;display:flex;align-items:center;justify-content:center;font:600 16px Commissioner,Arial';ov.textContent='Готовлю PDF как на карте…';document.body.appendChild(ov);
 el.style.cssText=sv+';position:fixed;left:0;top:0;width:'+w+'px;height:'+h+'px;z-index:2147482000';
 hadN=map.hasLayer(nlg);if(hadN)map.removeLayer(nlg);try{if(b0&&map.setBearing)map.setBearing(0)}catch(e){}
 map.invalidateSize({pan:false});map.setView(B.getCenter(),Z,{animate:false});await sleep(900);
 for(let t=0;t<120;t++){const im=[...el.querySelectorAll('.leaflet-tile-container img')];ov.textContent='Загрузка подложки… '+im.filter(i=>i.complete).length+'/'+im.length;if(im.length&&im.every(i=>i.complete))break;await sleep(250)}
 await sleep(400);ov.textContent='Снимаю карту…';
 const pr=Math.min(3,(A3?7200:5400)/Math.max(w,h)),cv=await htmlToImage.toCanvas(el,{pixelRatio:pr,cacheBust:false,skipFonts:true,imagePlaceholder:'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII=',filter:n=>!(n.classList&&(n.classList.contains('leaflet-control-container')))});
 const g=shdCtx(cv.getContext('2d'));
 if($('pdl').checked){const fz=12*pr,PT=[],SHW=[];P.forEach(p=>{if(p.x)return;const m=mk.get(p);if(!m||!map.hasLayer(m))return;const c=map.latLngToContainerPoint([p.lat,p.lon]);if(c.x<-20||c.y<-20||c.x>w+20||c.y>h+20)return;PT.push([c.x*pr,c.y*pr]);SHW.push(p)});
  const BX=[],hit=(a,b)=>a[0]<b[2]&&b[0]<a[2]&&a[1]<b[3]&&b[1]<a[3],r=9*pr;g.font=`bold ${fz}px Arial`;g.textBaseline='middle';g.textAlign='left';
  SHW.forEach((p,i)=>{const t=String(p.id||'').replace(/^КТП\s+/,'КТП').replace(/^Шуно Дорожная/,'ШД'),[x,y]=PT[i],tw=g.measureText(t).width,th=fz*1.1,d=r*1.4,
   cs=[[x-tw/2,y+d],[x+d,y+d*.3],[x-d-tw,y+d*.3],[x+d,y+d],[x-d-tw,y+d],[x-tw/2,y+d*2],[x+d,y-th-d*.2],[x-d-tw,y-th-d*.2],[x-tw/2,y-d*2.4-th]];
   let best=null,bo=1e9;for(const [cx,cy] of cs){const b=[cx-2,cy-2,cx+tw+2,cy+th+2];let ov2=BX.filter(q=>hit(b,q)).length*3;PT.forEach((q,j)=>{if(j!=i&&q[0]>b[0]-r&&q[0]<b[2]+r&&q[1]>b[1]-r&&q[1]<b[3]+r)ov2++});if(ov2<bo){bo=ov2;best=b;if(!ov2)break}}
   BX.push(best);g.lineJoin='round';g.strokeStyle='rgba(255,255,255,.95)';g.lineWidth=fz*.35;g.strokeText(t,best[0]+2,best[1]+2+th/2);g.fillStyle='#111';g.fillText(t,best[0]+2,best[1]+2+th/2)})}
 {const date=new Date().toLocaleDateString('ru-RU'),fz=13*pr,t1=(ar.title||'План')+' · по состоянию на '+date,t2=($('pbm').value=='esri'?'Подложка: Esri World Imagery':'Подложка: © участники OpenStreetMap')+' · положение опор приблизительное';g.font=`bold ${fz}px Arial`;const tw=Math.max(g.measureText(t1).width,(g.font=`${fz*.85}px Arial`,g.measureText(t2).width));g.fillStyle='rgba(255,255,255,.92)';g.fillRect(8*pr,cv.height-fz*3.4-8*pr,tw+16*pr,fz*3.4);g.fillStyle='#111';g.textBaseline='alphabetic';g.font=`bold ${fz}px Arial`;g.fillText(t1,16*pr,cv.height-fz*1.9-8*pr);g.font=`${fz*.85}px Arial`;g.fillStyle='#444';g.fillText(t2,16*pr,cv.height-fz*.6-8*pr)}
 ov.textContent='Собираю PDF…';const{jsPDF}=window.jspdf,doc=new jsPDF({orientation:'landscape',unit:'mm',format:A3?'a3':'a4',compress:true});doc.addImage(cv.toDataURL('image/jpeg',.9),'JPEG',0,0,PW,PH);doc.save(SHD('Как на карте — '+ar.file));st.textContent='Готово: файл сохранён'}
catch(e){st.textContent='Ошибка: '+(e.message||e)}
finally{if(el){el.setAttribute('style',sv);map.invalidateSize({pan:false});if(c0)map.setView(c0,z0,{animate:false});try{if(b0&&map.setBearing)map.setBearing(b0)}catch(e){}if(hadN)nlg.addTo(map)}if(ov)ov.remove()}}
$('pdfs').onclick=pdfSnap;
"""
R("$('pdfb').onclick=pdfPlan;","$('pdfb').onclick=pdfPlan;"+JS)
open(p,'w',encoding='utf-8').write(s);print('ok snap',p)
