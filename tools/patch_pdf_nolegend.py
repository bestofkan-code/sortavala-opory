# «План в PDF»: галочка «условные обозначения» (#pdlg, по умолчанию выключена — легенда скрыта).
# В оформлении чертежа без легенды правой панели нет: карта на всю рамку, над штампом — строка «по состоянию на …».
import sys
p=sys.argv[1];s=open(p,encoding='utf-8').read()
def R(a,b):
    global s
    assert s.count(a)==1,(a[:90],s.count(a));s=s.replace(a,b)
R("const GO=o.gost!==false,FL=20*u,FM=5*u,SW=185*u,SHh=55*u,pad=10*u,panelW=GO?(A3?126:96)*u:(A3?96:72)*u,",
  "const GO=o.gost!==false,LG=o.legend!==false,FL=20*u,FM=5*u,SW=185*u,SHh=55*u,pad=10*u,panelW=GO?(LG?(A3?126:96)*u:0):(A3?96:72)*u,")
# чертёж: панель только с легендой
a="const px=mx+mw+5*u,pw=panelW-9*u,date=new Date().toLocaleDateString('ru-RU');let y=my+11*u;g.textBaseline='alphabetic';"
R(a,"const date=new Date().toLocaleDateString('ru-RU');if(!LG){g.font=`${3*u}px ${F}`;const tl=(o.title||'Общий план')+' · по состоянию на '+date,tw=Math.min(g.measureText(tl).width,CW-FM-FL-SW),bx2=CW-FM-tw-4*u,by2=CH-FM-SHh-6*u;g.fillStyle='rgba(255,255,255,.9)';g.fillRect(bx2,by2,tw+4*u,6*u);g.fillStyle='#111';g.textAlign='left';g.textBaseline='middle';g.fillText(tl,bx2+2*u,by2+3*u,tw);g.textBaseline='alphabetic'}else{"
  "const px=mx+mw+5*u,pw=panelW-9*u;let y=my+11*u;g.textBaseline='alphabetic';")
R("g.fillText('Положение опор приблизительное.',px,y);\n// рамка","g.fillText('Положение опор приблизительное.',px,y)}\n// рамка")
R("g.beginPath();g.moveTo(mx+mw,FM);g.lineTo(mx+mw,CH-FM-SHh);g.stroke();","if(LG){g.beginPath();g.moveTo(mx+mw,FM);g.lineTo(mx+mw,CH-FM-SHh);g.stroke()}")
# старый вид: без блока легенды
R("const px=mx+mw+4*u;let y=my+3*u;const fs=3.1*u;g.font=`bold ${3.8*u}px ${F}`;g.fillText('Условные обозначения',px,y+3*u);y+=6.5*u;",
  "const px=mx+mw+4*u;let y=my+3*u;const fs=3.1*u;if(LG){g.font=`bold ${3.8*u}px ${F}`;g.fillText('Условные обозначения',px,y+3*u);y+=6.5*u;")
R("g.fillStyle='#111';g.fillText(tx,px+8*u,y);y+=4.6*u});\nconst ST=","g.fillStyle='#111';g.fillText(tx,px+8*u,y);y+=4.6*u})}\nconst ST=")
# UI
R('<label><input type="checkbox" id="pdg" checked> оформление чертежа (рамка, штамп)</label></div>','<label><input type="checkbox" id="pdg" checked> оформление чертежа (рамка, штамп)</label> <label><input type="checkbox" id="pdlg"> условные обозначения</label></div>')
R("gost:$('pdg').checked,","gost:$('pdg').checked,legend:$('pdlg').checked,")
open(p,'w',encoding='utf-8').write(s);print('ok nolegend',p)
