# «План в PDF» без условных обозначений — схема на всю страницу:
# старый вид — без правой панели; чертёж — участок вписывается в рамку целиком, крупнее,
# лишь бы ни одна опора не попала под штамп (иначе — как раньше, рядом со штампом).
import sys
p=sys.argv[1];s=open(p,encoding='utf-8').read()
def R(a,b):
    global s
    assert s.count(a)==1,(a[:90],s.count(a));s=s.replace(a,b)
R("panelW=GO?(LG?(A3?126:96)*u:0):(A3?96:72)*u,","panelW=GO?(LG?(A3?126:96)*u:0):(LG?(A3?96:72)*u:0),")
R("mw=GO?CW-FL-FM-panelW:CW-2*pad-panelW-4*u,","mw=GO?CW-FL-FM-panelW:CW-2*pad-panelW-(LG?4*u:0),")
R("f0=Math.max(fA,fB),OX=SOV&&fB>fA?-SOV/2:0,OY=SOV&&fA>=fB?-SHh/2:0;",
  "f00=Math.max(fA,fB);let f0=f00,OX=SOV&&fB>fA?-SOV/2:0,OY=SOV&&fA>=fB?-SHh/2:0;"
  "if(GO&&!LG){const Q=(o.only||P.filter(p=>p.lat>=BB.s&&p.lat<=BB.n&&p.lon>=BB.w&&p.lon<=BB.e)).filter(p=>!p.x).map(p=>[wX(p.lon),wY(p.lat)]),cx0=(x0+x1)/2,cy0=(y0+y1)/2,sxs=CW-FM-SW-4*u,sys=CH-FM-SHh-4*u;"
  "for(let f=Math.min(mw*.94/dX,mh*.94/dY);f>f00;f*=.97){if(!Q.some(q=>mx+mw/2+(q[0]-cx0)*f>sxs&&my+mh/2+(q[1]-cy0)*f>sys)){f0=f;OX=0;OY=0;break}}}")
open(p,'w',encoding='utf-8').write(s);print('ok fullpage',p)
