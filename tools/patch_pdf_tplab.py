# «План в PDF»: номера опор в виде «ТП97-15» (как id опоры), в обоих видах листа. «КТП 163-5» → «КТП163-5», Шуно Дорожная → «ШД-8».
import sys
p=sys.argv[1];s=open(p,encoding='utf-8').read()
def R(a,b):
    global s
    assert s.count(a)==1,(a[:90],s.count(a));s=s.replace(a,b)
R("const t=GO?String(p.id||'').replace(/^ТП/,'').replace(/^Шуно Дорожная/,'ШД'):String(p.n||p.id||'');",
  "const t=String(p.id||p.n||'').replace(/^КТП\\s+/,'КТП').replace(/^Шуно Дорожная/,'ШД');")
R("g.fillText('97-15',xx+4.5*u,yy)","g.fillText('ТП97-15',xx+4.5*u,yy)")
R("g.strokeText('12',px+3*u,y);g.fillStyle='#111';g.fillText('12',px+3*u,y);","g.strokeText('ТП97-15',px+3*u,y);g.fillStyle='#111';g.fillText('ТП97-15',px+3*u,y);")
open(p,'w',encoding='utf-8').write(s);print('ok tplab',p)
