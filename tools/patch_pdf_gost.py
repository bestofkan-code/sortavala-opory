# «План в PDF» в оформлении чертежа (как «Схема участка работ 17.11.2026»):
# рамка по ГОСТ (поле 20 мм слева, 5 мм), основная надпись (штамп) 185×55, справа панель: название, условные обозначения
# в две колонки; номера опор вида «97-15»; масштабная линейка с М 1:N; север вверху справа; шрифт osifont.
# Количеств нигде не пишем. Галочка #pdg «оформление чертежа (рамка, штамп)», по умолчанию включена.
import sys
p=sys.argv[1];s=open(p,encoding='utf-8').read()
def R(a,b):
    global s
    assert s.count(a)==1,(a[:90],s.count(a));s=s.replace(a,b)
# раскладка листа
R("const pad=10*u,panelW=(A3?96:72)*u,top=(A3?22:18)*u,mx=pad,my=top,mw=CW-2*pad-panelW-4*u,mh=CH-top-pad-4*u,F='Arial, Helvetica, sans-serif';",
  "const GO=o.gost!==false,FL=20*u,FM=5*u,SW=185*u,SHh=55*u,pad=10*u,panelW=GO?(A3?126:96)*u:(A3?96:72)*u,top=GO?FM:(A3?22:18)*u,mx=GO?FL:pad,my=top,mw=GO?CW-FL-FM-panelW:CW-2*pad-panelW-4*u,mh=GO?CH-2*FM:CH-top-pad-4*u,F=GO?'osifont, Arial, Helvetica, sans-serif':'Arial, Helvetica, sans-serif',SOV=GO?Math.max(0,SW-panelW):0;\n"
  "if(GO&&!window.OSIF){try{const ff=new FontFace('osifont','url(fonts/osifont-lgpl3fe.woff)');await ff.load();document.fonts.add(ff);window.OSIF=1}catch(e){}}")
# вписывание участка: не под штамп
R("y1=Math.max(...ys),f0=Math.min(mw*.94/(x1-x0),mh*.94/(y1-y0));",
  "y1=Math.max(...ys),dX=Math.max(x1-x0,1e-9),dY=Math.max(y1-y0,1e-9),fA=Math.min(mw*.94/dX,(mh-(SOV?SHh:0))*.94/dY),fB=Math.min((mw-SOV)*.94/dX,mh*.94/dY),f0=Math.max(fA,fB),OX=SOV&&fB>fA?-SOV/2:0,OY=SOV&&fA>=fB?-SHh/2:0;")
R("const s=2**z,k=f0/s,cwx=(x0+x1)/2*s,cwy=(y0+y1)/2*s,C=",
  "const s=2**z,k=f0/s,cwx=(x0+x1)/2*s-OX/k,cwy=(y0+y1)/2*s-OY/k,C=")
# номера опор как «97-15»
R("const t=String(p.n||p.id||'');","const t=GO?String(p.id||'').replace(/^ТП/,'').replace(/^Шуно Дорожная/,'ШД'):String(p.n||p.id||'');")
# хвост: оформление
a=s.find("const lat0=(Math.min(...P.map(p=>p.lat))+Math.max(...P.map(p=>p.lat)))/2,mpp=");b=s.find("window.DPK=false;\nreturn cv}",a)
assert a>0 and b>a
old=s[a:b]
GOST=r"""const lat0=(Math.min(...P.map(p=>p.lat))+Math.max(...P.map(p=>p.lat)))/2,mpp=156543.03392*Math.cos(lat0*Math.PI/180)/s/k,N=Math.round(mpp*u*1000/100)*100;
let m=[50,100,200,250,500,1000,2000].find(v=>v/mpp>=40*u)||2000;const sl=m/mpp,bx=mx+6*u,by=my+mh-7*u;
g.fillStyle='rgba(255,255,255,.88)';g.fillRect(mx+2*u,my+mh-17*u,sl+34*u,15*u);g.strokeStyle='#111';g.lineWidth=.3*u;for(let i=0;i<5;i++){g.fillStyle=i%2?'#fff':'#111';g.fillRect(bx+sl*i/5,by-.8*u,sl/5,1.6*u)}g.strokeRect(bx,by-.8*u,sl,1.6*u);
g.fillStyle='#111';g.font=`${2.6*u}px ${F}`;g.textAlign='center';g.textBaseline='alphabetic';for(let i=0;i<=5;i++)g.fillText(String(Math.round(m*i/5)),bx+sl*i/5,by-2*u);g.textAlign='left';g.fillText('м',bx+sl+2*u,by+.9*u);g.fillText('М 1:'+N.toLocaleString('ru-RU'),bx+sl+7*u,by+.9*u);
g.font=`${2*u}px ${F}`;g.fillStyle='#333';const at=o.base=='esri'?'Подложка: Esri World Imagery':o.base=='ya'||o.base=='yas'?'Подложка: © Яндекс':'© участники OpenStreetMap';g.fillText(at,mx+3*u,my+mh-13.6*u);
const nx=mx+mw-10*u,ny=my+12*u;g.fillStyle='rgba(255,255,255,.85)';g.fillRect(nx-6*u,ny-9*u,12*u,20*u);g.fillStyle='#111';g.strokeStyle='#111';g.lineWidth=.45*u;g.beginPath();g.moveTo(nx,ny+5*u);g.lineTo(nx,ny-4*u);g.stroke();g.beginPath();g.moveTo(nx,ny-8*u);g.lineTo(nx-2*u,ny-3*u);g.lineTo(nx+2*u,ny-3*u);g.fill();g.font=`${3.4*u}px ${F}`;g.textAlign='center';g.fillText('С',nx,ny+9.5*u);
g.restore();
const wrap=(t,w)=>{const W=String(t).split(' '),L=[];let c='';W.forEach(x=>{const n=c?c+' '+x:x;if(g.measureText(n).width>w&&c){L.push(c);c=x}else c=n});if(c)L.push(c);return L};
const T=(t,x,y,fz,al)=>{g.font=`${fz}px ${F}`;g.textAlign=al||'left';g.fillStyle='#111';g.fillText(t,x,y)};
// панель
const px=mx+mw+5*u,pw=panelW-9*u,date=new Date().toLocaleDateString('ru-RU');let y=my+11*u;g.textBaseline='alphabetic';
T('План-схема участка работ',px,y,(A3?6.2:5.2)*u);y+=(A3?6.5:5.6)*u;T('опоры, кронштейны, СИП-4 4×25',px,y,(A3?4.4:3.8)*u);y+=5*u;
g.font=`${3.2*u}px ${F}`;wrap((o.title||'Общий план')+' · по состоянию на '+date,pw).forEach(l=>{g.fillStyle='#555';g.textAlign='left';g.fillText(l,px,y);y+=4*u});y+=3*u;
T('Условные обозначения (как на карте)',px,y,(A3?4.6:4)*u);y+=5*u;
const LGP=[['Стандартная опора',{t:'S'}],['Анкерная опора',{t:'A'}],['Установлена',{t:'S',done:1}],['Заземление',{t:'S',g:1}],['Гравит. фундамент выполнен',{t:'S',w:{10:'x'}}],['Гравит. фундамент (проект)',{t:'S',f:'G'}],...(window.DPK?[['Кронштейн 1-рожковый',{t:'S',kr:1}],['Кронштейн 2-рожк. 90°',{t:'S',kr:2,ka:90}],['Кронштейн 2-рожк. 180°',{t:'S',kr:2,ka:180}],['Кронштейн установлен',{t:'S',kr:2,ka:180,w:{12:'x'}}],['Светильники установлены',{t:'S',kr:2,ka:180,sv:2,w:{12:'x'}}]]:[['Кронштейн 1-рожк. (проект)',{t:'S',kr:1}],['Кронштейн 2-рожк. установлен',{t:'S',kr:2,w:{12:'x'}}],['Светильник установлен (1 из 2)',{t:'S',kr:2,sv:1,w:{12:'x'}}]]),['Опора готова: все светильники',{t:'S',done:1,kr:2,sv:2,w:{12:'x'}}],['Предлагаемая (серая)',{t:'S',pp:1,uid:'n1'}],['Новая (не в проекте)',{t:'S',uid:'n1'}],['Совместная подвеска',{t:'S',js:1}],['Опора ввода КЛ (люк)',{t:'S',vk:1}]].map(x=>['p',...x]);
const LGI=[...LGP,...(o.lab?[['n','Номер опоры']]:[]),['l','Линия ВЛ (по чертежу)','#1d4ed8',[]],['l','Связь предположительная','#1d4ed8',[1.2*u,.9*u]],['l','Совместная подвеска (линия)','#dc2626',[]],['l','Бронекабель от ТП (КЛ)','#c026d3',[2*u,1*u]],['t','Трансформаторная подстанция']];
const half=Math.ceil(LGI.length/2),cwd=pw/2,rh=(A3?6:5.2)*u;let lfz=(A3?3:2.6)*u;g.font=`${lfz}px ${F}`;{const mw2=Math.max(...LGI.map(it=>g.measureText(it[1]).width)),av=cwd-12*u;if(mw2>av)lfz*=av/mw2}
LGI.forEach((it,i)=>{const col=i<half?0:1,xx=px+col*cwd,yy=y+(col?i-half:i)*rh+rh/2,tx=xx+11*u;g.textBaseline='middle';
 if(it[0]=='p'){const f=it[2],bk=window.DPK&&f.kr;dpole(g,xx+4.5*u,yy+(bk?1.3*u:0),Object.assign({uid:'p0',w:{}},f),bk?.62*u:(A3?1:.9)*u)}
 else if(it[0]=='n'){g.font=`bold ${2.4*u}px ${F}`;g.textAlign='center';g.fillStyle='#111';g.fillText('97-15',xx+4.5*u,yy)}
 else if(it[0]=='l'){g.strokeStyle=it[2];g.lineWidth=it[2]=='#dc2626'?1.1*u:.5*u;g.setLineDash(it[3]);g.beginPath();g.moveTo(xx+.5*u,yy);g.lineTo(xx+9*u,yy);g.stroke();g.setLineDash([])}
 else{g.fillStyle='#1f2937';g.strokeStyle='#9ca3af';g.lineWidth=.35*u;g.fillRect(xx+1*u,yy-1.6*u,7*u,3.2*u);g.strokeRect(xx+1*u,yy-1.6*u,7*u,3.2*u);g.fillStyle='#fff';g.font=`${2.2*u}px ${F}`;g.textAlign='center';g.fillText('ТП',xx+4.5*u,yy+.1*u)}
 g.font=`${lfz}px ${F}`;g.textAlign='left';g.fillStyle='#111';g.fillText(it[1],tx,yy)});
y+=half*rh+5*u;g.textBaseline='alphabetic';g.font=`${2.8*u}px ${F}`;g.fillStyle='#444';g.textAlign='left';g.fillText('Положение опор приблизительное.',px,y);
// рамка
g.strokeStyle='#000';g.lineWidth=.7*u;g.strokeRect(FL,FM,CW-FL-FM,CH-2*FM);g.beginPath();g.moveTo(mx+mw,FM);g.lineTo(mx+mw,CH-FM-SHh);g.stroke();
// штамп (основная надпись)
const sx=CW-FM-SW,sy=CH-FM-SHh,r5=5*u,ln=(x1,y1,x2,y2,w)=>{g.lineWidth=w;g.beginPath();g.moveTo(x1,y1);g.lineTo(x2,y2);g.stroke()},TK=.7*u,TN=.25*u;
g.fillStyle='#fff';g.fillRect(sx,sy,SW,SHh);g.strokeStyle='#000';g.lineWidth=TK;g.strokeRect(sx,sy,SW,SHh);
const cxs=[10,10,10,10,15,10];let xx=sx;cxs.forEach((w,i)=>{xx+=w*u;if(i<5)ln(xx,sy,xx,sy+SHh,i==4||i==3||i==2||i==1||i==0?(i<4?TK:TK):TK)});
for(let i=1;i<11;i++)ln(sx,sy+i*r5,sx+65*u,sy+i*r5,i==5||i==6?TK:TN);
ln(sx+65*u,sy,sx+65*u,sy+SHh,TK);ln(sx+65*u,sy+15*u,sx+SW,sy+15*u,TK);ln(sx+65*u,sy+40*u,sx+SW,sy+40*u,TK);ln(sx+135*u,sy+15*u,sx+135*u,sy+SHh,TK);
ln(sx+135*u,sy+20*u,sx+SW,sy+20*u,TN);ln(sx+135*u,sy+25*u,sx+SW,sy+25*u,TK);ln(sx+150*u,sy+15*u,sx+150*u,sy+25*u,TN);ln(sx+165*u,sy+15*u,sx+165*u,sy+25*u,TN);
g.textBaseline='middle';const hz=2.5*u;[['Изм.',5],['Кол.уч',15],['Лист',25],['№ док.',35],['Подп.',47.5],['Дата',60]].forEach(([t,c])=>T(t,sx+c*u,sy+5.5*r5,hz,'center'));
[['Разраб.',6],['Пров.',7],['Н.контр.',9],['ГИП',10]].forEach(([t,r])=>T(t,sx+1*u,sy+(r+.5)*r5,hz,'left'));
T('КАР/00230/26',sx+100*u,sy+7.5*u,5*u,'center');
[['Стадия',142.5],['Лист',157.5],['Листов',175]].forEach(([t,c])=>T(t,sx+c*u,sy+17.5*u,hz,'center'));[['Р',142.5],['1',157.5],['1',175]].forEach(([t,c])=>T(t,sx+c*u,sy+22.5*u,3*u,'center'));
g.font=`${3.4*u}px ${F}`;let L1=wrap('Модернизация (капитальный ремонт) уличного освещения г. Сортавала (1 этап)',66*u);L1.forEach((l,i)=>T(l,sx+100*u,sy+27.5*u+(i-(L1.length-1)/2)*4.6*u,3.4*u,'center'));
g.font=`${3.2*u}px ${F}`;let L2=wrap('План-схема участка работ: опоры, кронштейны, СИП-4 4×25',66*u);L2.forEach((l,i)=>T(l,sx+100*u,sy+47.5*u+(i-(L2.length-1)/2)*4.4*u,3.2*u,'center'));
g.textBaseline='alphabetic';"""
s=s[:a]+"if(!GO){"+old+"}else{"+GOST+"}"+s[b:]
# UI
R('<label><input type="checkbox" id="pdk" checked> крупные кронштейны</label></div>','<label><input type="checkbox" id="pdk" checked> крупные кронштейны</label></div><div class="r"><label><input type="checkbox" id="pdg" checked> оформление чертежа (рамка, штамп)</label></div>')
R("lab:$('pdl').checked,bigk:$('pdk').checked,","lab:$('pdl').checked,bigk:$('pdk').checked,gost:$('pdg').checked,")
open(p,'w',encoding='utf-8').write(s);print('ok gost',p)
