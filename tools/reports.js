/* ---- отчёты за день (3 PDF): BEGIN ---- */
/* Кнопка «Создать отчёты за сегодня»: три PDF за выбранный день — забуренные котлованы (закладные), установленные опоры,
   установленные кронштейны и светильники. На листе только подложка, линии, опоры за день с подписями; без легенды и без названия карты. */
const DRday=v=>/^\d{4}-\d\d-\d\d/.test(v||'')?v.slice(0,10):'';
const DRzak=p=>p.t=='A'?'ФМ-0,273-2,5':'ФМ-0,219-2,5';
const DRogs=p=>'ОГС '+(p.t=='A'?'0,7':'0,4')+'-'+(+p.h==9?9:8);
const DRkr=p=>{const k=+p.kr||0,a=+p.ka||0;return k==2?'2-рожк.'+(a==90?' 90°':a==180?' 180°':''):k==1?'1-рожк.':''};
const DRlum=p=>Math.max(+p.sv||0,wdone(p,6)?1:0);
const DRsv=n=>n+' '+(n%10==1&&n%100!=11?'светильник':n%10>=2&&n%10<=4&&(n%100<10||n%100>=20)?'светильника':'светильников');
const DRcnt=(L,f)=>{const m=new Map();L.forEach(p=>{const k=f(p);m.set(k,(m.get(k)||0)+1)});return [...m].sort((a,b)=>a[0].localeCompare(b[0],'ru',{numeric:true})).map(([k,n])=>k+' — '+n).join(', ')};
const DREP=[
 {k:'zak',file:'Забуренные котлованы',title:'Закладные',col:'#ea580c',
  sel:(p,d)=>!isG(p)&&(DRday(wd(p,1))==d||DRday(wd(p,2))==d),
  lab:p=>[p.id,wdone(p,2)?DRzak(p):'котлован под '+DRzak(p)],
  sum:L=>{const z=L.filter(p=>wdone(p,2)).length;return 'забурено котлованов: '+L.length+' ('+DRcnt(L,DRzak)+')'+(z<L.length?' · закладных установлено: '+z:'')}},
 {k:'op',file:'Установленные опоры',title:'Опоры',col:'#16a34a',
  sel:(p,d)=>!!p.done&&DRday(p.date)==d,
  lab:p=>[p.id,DRogs(p)],
  sum:L=>'установлено опор: '+L.length+' ('+DRcnt(L,DRogs)+')'},
 {k:'krs',file:'Установленные кронштейны и светильники',title:'Кронштейны и светильники',col:'#2563eb',arms:true,
  sel:(p,d)=>DRday(wd(p,12))==d||DRday(wd(p,6))==d,
  lab:(p,d)=>{const a=[];if(DRday(wd(p,12))==d)a.push('кронштейн '+DRkr(p));if(DRday(wd(p,6))==d)a.push(DRsv(Math.max(1,DRlum(p))));return[p.id,a.join(' + ')]},
  sum:(L,d)=>{const K=L.filter(p=>DRday(wd(p,12))==d),S=L.filter(p=>DRday(wd(p,6))==d),n=S.reduce((s,p)=>s+Math.max(1,DRlum(p)),0);
   return 'кронштейнов: '+K.length+(K.length?' ('+DRcnt(K,DRkr)+')':'')+' · светильников: '+n}}];

async function drPage(o){const u=250/25.4,CW=Math.round(297*u),CH=Math.round(210*u),cv=document.createElement('canvas');cv.width=CW;cv.height=CH;const g=cv.getContext('2d');g.fillStyle='#fff';g.fillRect(0,0,CW,CH);
 const F='Arial, Helvetica, sans-serif',pad=9*u,top=22*u,mx=pad,my=top,mw=CW-2*pad,mh=CH-top-pad-3*u;
 const wX=lo=>(lo+180)/360*256,wY=la=>{const s=Math.sin(la*Math.PI/180);return(.5-Math.log((1+s)/(1-s))/(4*Math.PI))*256};
 const L=o.L,lat=L.map(p=>p.lat),lon=L.map(p=>p.lon);let bb={s:Math.min(...lat),n:Math.max(...lat),w:Math.min(...lon),e:Math.max(...lon)};
 {const dl=Math.max(0,.0022-(bb.n-bb.s))/2,dw=Math.max(0,.0046-(bb.e-bb.w))/2,ml=(bb.n-bb.s)*.08+.00025,mwd=(bb.e-bb.w)*.08+.0005;bb={s:bb.s-dl-ml,n:bb.n+dl+ml,w:bb.w-dw-mwd,e:bb.e+dw+mwd}}
 const x0=wX(bb.w),x1=wX(bb.e),y0=wY(bb.n),y1=wY(bb.s),f0=Math.min(mw/(x1-x0),mh/(y1-y0));
 const cnt=z=>{const s=2**z,k=f0/s,hw=mw/2/k,hh=mh/2/k,cx=(x0+x1)/2*s,cy=(y0+y1)/2*s;return(Math.floor((cx+hw)/256)-Math.floor((cx-hw)/256)+1)*(Math.floor((cy+hh)/256)-Math.floor((cy-hh)/256)+1)};
 let z=Math.min(19,Math.ceil(Math.log2(f0)));while(z>8&&cnt(z)>140)z--;
 const s=2**z,k=f0/s,cwx=(x0+x1)/2*s,cwy=(y0+y1)/2*s,C=(la,lo)=>[mx+mw/2+(wX(lo)*s-cwx)*k,my+mh/2+(wY(la)*s-cwy)*k];
 const jobs=[];for(let a=Math.floor((cwx-mw/2/k)/256);a<=Math.floor((cwx+mw/2/k)/256);a++)for(let b=Math.floor((cwy-mh/2/k)/256);b<=Math.floor((cwy+mh/2/k)/256);b++)jobs.push([a,b]);
 const url=(a,b)=>o.base=='esri'?`https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/${z}/${b}/${a}`:`https://tile.openstreetmap.org/${Math.min(z,19)}/${a}/${b}.png`;
 g.save();g.beginPath();g.rect(mx,my,mw,mh);g.clip();g.fillStyle='#eef0f2';g.fillRect(mx,my,mw,mh);let ok=0,n=0,q=0;
 await Promise.all(Array.from({length:6},async()=>{while(q<jobs.length){const [a,b]=jobs[q++],im=await loadTile(url(a,b));n++;if(im){ok++;g.drawImage(im,mx+mw/2+(a*256-cwx)*k,my+mh/2+(b*256-cwy)*k,256*k+.6,256*k+.6)}o.onp&&o.onp(n,jobs.length)}}));
 g.fillStyle=o.base=='esri'?'rgba(255,255,255,.12)':'rgba(255,255,255,.25)';g.fillRect(mx,my,mw,mh);
 const inb=(la,lo)=>la>=bb.s-.002&&la<=bb.n+.002&&lo>=bb.w-.004&&lo<=bb.e+.004,lw=.3*u;
 /* линии и остальные опоры — для ориентира */
 try{g.lineCap='round';const NT=netEdges();g.strokeStyle='rgba(29,78,216,.55)';g.lineWidth=lw*1.3;NT.E.filter(e=>(e[2]!='d'||e.pts)&&(inb(e[0].lat,e[0].lon)||inb(e[1].lat,e[1].lon))).forEach(e=>{g.setLineDash(e[2]=='n'||e[2]=='r'?[lw*4,lw*3]:[]);g.beginPath();epath(e[0],e[1],e.pts).forEach((c,i)=>i?g.lineTo(...C(c[0],c[1])):g.moveTo(...C(c[0],c[1])));g.stroke()});g.setLineDash([])}catch(e){}
 const SEL=new Set(L);P.forEach(p=>{if(SEL.has(p)||!inb(p.lat,p.lon))return;const[x,y]=C(p.lat,p.lon);g.beginPath();g.arc(x,y,.75*u,0,7);g.fillStyle='rgba(255,255,255,.9)';g.fill();g.strokeStyle='#6b7280';g.lineWidth=.25*u;g.stroke()});
 /* опоры за день */
 const R=1.35*u,PT=L.map(p=>({p,xy:C(p.lat,p.lon)}));
 PT.forEach(({p,xy:[x,y]})=>{if(o.rep.arms){const nA=armN(p);armAng(nA,+p.ka).forEach((a,i)=>{const t=a*Math.PI/180,ex=x+4.2*u*Math.cos(t),ey=y+4.2*u*Math.sin(t);g.beginPath();g.moveTo(x,y);g.lineTo(ex,ey);g.strokeStyle='#fff';g.lineWidth=1.1*u;g.stroke();g.strokeStyle='#111';g.lineWidth=.55*u;g.stroke();if(i<DRlum(p)){g.beginPath();g.arc(ex,ey,1*u,0,7);g.fillStyle='#facc15';g.fill();g.strokeStyle='#111';g.lineWidth=.3*u;g.stroke()}})}
  g.beginPath();g.arc(x,y,R,0,7);g.fillStyle=o.rep.col;g.fill();g.strokeStyle='#fff';g.lineWidth=.45*u;g.stroke();g.beginPath();g.arc(x,y,R+.25*u,0,7);g.strokeStyle='#111';g.lineWidth=.2*u;g.stroke()});
 /* подписи: подбираем место, чтобы не налезали друг на друга */
 const placed=[],obst=PT.map(({xy:[x,y]})=>[x-R-.6*u,y-R-.6*u,x+R+.6*u,y+R+.6*u]),hit=(b,A)=>A.some(c=>b[0]<c[2]&&b[2]>c[0]&&b[1]<c[3]&&b[3]>c[1]),f1=2.7*u,f2=2.35*u,lh=3.1*u;
 const order=PT.slice().sort((a,b)=>a.xy[1]-b.xy[1]||a.xy[0]-b.xy[0]);
 order.forEach(({p,xy:[x,y]})=>{const t=o.rep.lab(p,o.d);g.font=`bold ${f1}px ${F}`;const w1=g.measureText(t[0]).width;g.font=`${f2}px ${F}`;const w2=t[1]?g.measureText(t[1]).width:0,bw=Math.max(w1,w2)+2*u,bh=(t[1]?2*lh:lh)+1*u;
  const cand=[];[1,2.2,3.6,5.2].forEach(m=>{const d=(R+1.2*u)*m;[[d,-bh/2],[-d-bw,-bh/2],[-bw/2,-d-bh],[-bw/2,d],[d*.75,-d*.75-bh],[-d*.75-bw,-d*.75-bh],[d*.75,d*.75],[-d*.75-bw,d*.75]].forEach(([dx,dy])=>cand.push([x+dx,y+dy]))});
  let bx=cand[0],ok2=false;for(const c of cand){const b=[c[0],c[1],c[0]+bw,c[1]+bh];if(b[0]<mx+1*u||b[2]>mx+mw-1*u||b[1]<my+1*u||b[3]>my+mh-1*u)continue;if(hit(b,placed)||hit(b,obst))continue;bx=c;ok2=true;break}
  const b=[bx[0],bx[1],bx[0]+bw,bx[1]+bh];placed.push(b);const cx=Math.max(b[0],Math.min(x,b[2])),cy=Math.max(b[1],Math.min(y,b[3]));if(Math.hypot(cx-x,cy-y)>R+1.5*u){g.beginPath();g.moveTo(x,y);g.lineTo(cx,cy);g.strokeStyle='#111';g.lineWidth=.22*u;g.stroke()}
  g.fillStyle='rgba(255,255,255,.93)';g.fillRect(b[0],b[1],bw,bh);g.strokeStyle=o.rep.col;g.lineWidth=.3*u;g.strokeRect(b[0],b[1],bw,bh);
  g.fillStyle='#111';g.textAlign='left';g.textBaseline='middle';g.font=`bold ${f1}px ${F}`;g.fillText(t[0],b[0]+1*u,b[1]+.5*u+lh/2);if(t[1]){g.font=`${f2}px ${F}`;g.fillText(t[1],b[0]+1*u,b[1]+.5*u+lh*1.5)}});
 /* масштаб и север */
 const mpp=156543.03392*Math.cos(((bb.s+bb.n)/2)*Math.PI/180)/s/k;let m=[10,20,25,50,100,200,250,500,1000].find(v=>v/mpp>=22*u)||1000;
 g.fillStyle='rgba(255,255,255,.88)';g.fillRect(mx+3*u,my+mh-12*u,m/mpp+10*u,9*u);g.strokeStyle='#111';g.lineWidth=.4*u;const sx=mx+8*u,sy=my+mh-5.5*u;g.beginPath();g.moveTo(sx,sy);g.lineTo(sx+m/mpp,sy);g.moveTo(sx,sy-1.1*u);g.lineTo(sx,sy+1.1*u);g.moveTo(sx+m/mpp,sy-1.1*u);g.lineTo(sx+m/mpp,sy+1.1*u);g.stroke();g.fillStyle='#111';g.font=`${2.8*u}px ${F}`;g.textAlign='left';g.textBaseline='alphabetic';g.fillText(m+' м',sx,sy-2.6*u);
 const nx=mx+mw-9*u,ny=my+12*u;g.fillStyle='rgba(255,255,255,.88)';g.fillRect(nx-5*u,ny-9*u,10*u,18*u);g.strokeStyle='#111';g.lineWidth=.4*u;g.beginPath();g.moveTo(nx,ny+7*u);g.lineTo(nx,ny-4*u);g.stroke();g.beginPath();g.moveTo(nx,ny-8*u);g.lineTo(nx-1.8*u,ny-3*u);g.lineTo(nx+1.8*u,ny-3*u);g.fillStyle='#111';g.fill();g.font=`bold ${3*u}px ${F}`;g.textAlign='center';g.fillText('С',nx,ny+6.5*u);
 g.font=`${2.2*u}px ${F}`;g.textAlign='right';const at=ok?(o.base=='esri'?'Подложка: Esri World Imagery':'© участники OpenStreetMap'):'Подложка не загрузилась (нет интернета)',aw=g.measureText(at).width+3*u;g.fillStyle='rgba(255,255,255,.85)';g.fillRect(mx+mw-aw,my+mh-4.6*u,aw,4.6*u);g.fillStyle='#222';g.fillText(at,mx+mw-1.5*u,my+mh-1.4*u);
 g.restore();g.strokeStyle='#666';g.lineWidth=.3*u;g.strokeRect(mx,my,mw,mh);
 /* заголовок: только название работ, дата и итог */
 g.textAlign='left';g.textBaseline='alphabetic';g.fillStyle='#111';g.font=`bold ${8*u}px ${F}`;g.fillText(o.rep.title,pad,top-9.5*u);
 g.font=`${3.6*u}px ${F}`;g.fillText(rd(o.d)+(o.tp?' · '+o.tp:'')+' · '+o.rep.sum(L,o.d)+(o.pages>1?' · лист '+o.page+' из '+o.pages:''),pad,top-3*u);
 return cv}

async function drMake(rep,d,base,st){const L=P.filter(p=>p.lat&&p.lon&&rep.sel(p,d));if(!L.length)return null;
 /* листы: опоры, которые стоят цепочкой ближе 500 м друг от друга, — на одном листе */
 const par=L.map((_,i)=>i),fd=i=>par[i]==i?i:(par[i]=fd(par[i])),xy=p=>[p.lon*K1,p.lat*K2];
 for(let i=0;i<L.length;i++)for(let j=i+1;j<L.length;j++){const a=xy(L[i]),b=xy(L[j]);if(Math.hypot(a[0]-b[0],a[1]-b[1])<500)par[fd(i)]=fd(j)}
 const G=new Map();L.forEach((p,i)=>{const r=fd(i);if(!G.has(r))G.set(r,[]);G.get(r).push(p)});
 const ru=(a,b)=>String(a).localeCompare(String(b),'ru',{numeric:true}),tps=Lg=>[...new Set(Lg.map(p=>String(p.tp||'')).filter(Boolean))].sort(ru).map(tpn).join(', ');
 const groups=[...G.values()].map(Lg=>[tps(Lg),Lg.sort((a,b)=>ru(a.id,b.id))]).sort((a,b)=>b[1].length-a[1].length||ru(a[0],b[0]));
 if(!window.jspdf)await loadScript('https://cdnjs.cloudflare.com/ajax/libs/jspdf/2.5.1/jspdf.umd.min.js');
 const{jsPDF}=window.jspdf,doc=new jsPDF({orientation:'landscape',unit:'mm',format:'a4',compress:true});
 for(let i=0;i<groups.length;i++){const [t,Lg]=groups[i];if(i)doc.addPage('a4','landscape');
  const cv=await drPage({rep,d,L:Lg,tp:t,base,page:i+1,pages:groups.length,onp:(a,b)=>st(rep.file+': подложка '+(i+1)+'/'+groups.length+', '+a+'/'+b)});
  doc.addImage(cv.toDataURL('image/jpeg',.9),'JPEG',0,0,297,210)}
 return{name:rd(d)+' '+rep.file+'.pdf',blob:doc.output('blob'),n:L.length}}

async function drRun(){const d=$('drd').value||LD(),st=t=>$('drs').textContent=t,out=$('drl'),base=($('pbm')&&$('pbm').value)||'osm';$('drb').disabled=true;out.innerHTML='';
 try{const res=[];for(const rep of DREP){st('Готовлю: '+rep.file+'…');const r=await drMake(rep,d,base,st);res.push([rep,r])}
  const got=res.filter(x=>x[1]);if(!got.length){st('За '+rd(d)+' нет отмеченных работ: котлованов, опор, кронштейнов и светильников.');return}
  out.innerHTML=res.map(([rep,r])=>r?'<a href="'+URL.createObjectURL(r.blob)+'" download="'+esc(r.name)+'">'+esc(r.name)+'</a> <small>('+r.n+' оп.)</small>':'<span style="opacity:.6">'+esc(rd(d)+' '+rep.file)+' — работ нет</span>').join('<br>');
  const A=[...out.querySelectorAll('a')];for(let i=0;i<A.length;i++){A[i].click();await new Promise(r=>setTimeout(r,700))}
  st('Готово: '+got.length+' из 3 файлов. Если браузер скачал не все, нажмите на ссылки ниже.')}
 catch(e){st('Ошибка: '+e.message)}finally{$('drb').disabled=false}}
function drLbl(){const d=$('drd').value;$('drb').textContent=!d||d==LD()?'Создать отчёты за сегодня':'Создать отчёты за '+rd(d)}
$('drd').value=LD();$('drd').onchange=drLbl;$('drb').onclick=drRun;drLbl();
/* ---- отчёты за день (3 PDF): END ---- */
