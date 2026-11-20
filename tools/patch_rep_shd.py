# Отчёты PDF: «Шуно Дорожная» пишется как «ШД» (подписи опор, значок ТП, заголовки, имя файла) — план в PDF и фотоотчёты.
import sys
p=sys.argv[1];s=open(p,encoding='utf-8').read()
def R(a,b,n=1):
    global s
    assert s.count(a)==n,(a[:90],s.count(a));s=s.replace(a,b)
SHD="function SHD(t){return String(t).replace(/Шуно Дорожная/g,'ШД')}\nfunction shdCtx(g){const f=g.fillText.bind(g),k=g.strokeText.bind(g);g.fillText=(t,...a)=>f(SHD(t),...a);g.strokeText=(t,...a)=>k(SHD(t),...a);return g}\n"
R("async function buildPlan(o){","\n"+SHD+"async function buildPlan(o){")
R("cv.width=CW;cv.height=CH;const g=cv.getContext('2d');g.fillStyle='#fff';g.fillRect(0,0,CW,CH);","cv.width=CW;cv.height=CH;const g=shdCtx(cv.getContext('2d'));g.fillStyle='#fff';g.fillRect(0,0,CW,CH);")
R("const cv=document.createElement('canvas');cv.width=W;cv.height=Hh;const g=cv.getContext('2d');g.fillStyle='#fff';g.fillRect(0,0,W,Hh);g.fillStyle='#111';g.textBaseline='alphabetic';\n  g.font=`bold 34px ${F}`;g.fillText(TT,50,62);",
  "const cv=document.createElement('canvas');cv.width=W;cv.height=Hh;const g=shdCtx(cv.getContext('2d'));g.fillStyle='#fff';g.fillRect(0,0,W,Hh);g.fillStyle='#111';g.textBaseline='alphabetic';\n  g.font=`bold 34px ${F}`;g.fillText(TT,50,62);")
R("doc.save(TT.replace(':','')+' '+per+'.pdf')","doc.save(SHD(TT.replace(':','')+' '+per+'.pdf'))")
R("const parts=[base].concat(F).concat(tp?[tp]:[]).concat([t]);let f=parts.join(' — ')","const parts=[base].concat(F).concat(tp?[tp]:[]).concat([t]);let f=SHD(parts.join(' — '))")
open(p,'w',encoding='utf-8').write(s);print('ok shd',p)
