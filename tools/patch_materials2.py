# «Материалы на складе»: расход крюков, ленты, бугелей и проколов CT 16 P (светильники + перемычка PEN); позиции с одним mkey складываются в одну строку
import sys
fn=sys.argv[1];s=open(fn,encoding='utf-8').read()
def R(a,b,n=1):
    global s
    assert s.count(a)==n,(a[:90],s.count(a));s=s.replace(a,b)
R("o.strap=o.sus*2+o.anc+o.zoi+o.bond+o.ct70;o.nki=o.grover=o.washer=o.bolt=o.bond;o.pugv=Math.round(o.bond*SIPN.pen*10)/10;return o}",
  "o.strap=o.sus*2+o.anc+o.zoi+o.bond+o.ct70;o.nki=o.grover=o.washer=o.bolt=o.bond;o.pugv=Math.round(o.bond*SIPN.pen*10)/10;o.pierce=o.zoi+o.bond;o.hook=o.sus+o.anc;o.tape=Math.round(o.hook*1.5*10)/10;o.clip=Math.ceil(o.tape);return o}")
R("MATI.forEach(r=>{const k=r.code||r.name,g=G.get(k)||{name:r.name,unit:un(r.unit),q:0,key:r.mkey,docs:new Set()};g.q+=(+r.qty||0)*(+r.per||1);g.docs.add(r.doc);G.set(k,g)});",
  "MATI.forEach(r=>{const k=r.mkey?'k:'+r.mkey:(r.code||r.name),g=G.get(k)||{name:r.name,unit:un(r.unit),q:0,key:r.mkey,docs:new Set(),nm:new Set()};g.q+=(+r.qty||0)*(+r.per||1);g.docs.add(r.doc);g.nm.add(r.name);g.name=[...g.nm].join(' + ');G.set(k,g)});")
open(fn,'w',encoding='utf-8').write(s);print('ok materials2')
