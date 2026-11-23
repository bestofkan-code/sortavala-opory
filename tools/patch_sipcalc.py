# -*- coding: utf-8 -*-
"""СИП к заказу: вместо «длина пролётов × 1,02» — расчёт по отрезкам:
  СИП отрезка = (Σ пролётов + Σ провис по каждому пролёту) × (1 + запас на раскатку)
               + шлейфы на транзитных анкерных/угловых опорах
               + хвосты на обоих концах отрезка (натяжка монтажным зажимом, заделка колпачками, проколы ответвления)
               + опуск к соединению с бронекабелем на опоре ввода (первый отрезок от ТП)
  стык (отрезок длиннее барабана) — ещё 2 хвоста и шлейф.
Провис: стрела f = f40·(L/40)² (по умолчанию 1,0 м при 40 м — монтажная стрела СИП-4 4×25),
длина провода в пролёте по параболе: L + 8f²/(3L).
Нормы — в SIPN: f40, loop, tail, inlT, res. Применять: python3 tools/patch_sipcalc.py <file.html> [...]"""
import sys

R = [
 ("var SIPN={sipK:1.02,tail:1.5,", "var SIPN={sipK:1.02,tail:1.5,f40:1.0,loop:1.0,inlT:1.5,res:0.01,"),
 ("function sipCalc(){", "function sipSag(L){const f=SIPN.f40*Math.pow((L||0)/40,2);return{f,d:L>0?8*f*f/(3*L):0}}\n"
  "function sipNeed(pc){const s=pc.sag||0,lp=(pc.loops||0)*SIPN.loop,tl=2*SIPN.tail,ib=pc.inl?SIPN.inlT:0,rs=(pc.len+s)*SIPN.res;return{len:pc.len,sag:s,loops:lp,tails:tl,inl:ib,res:rs,all:pc.len+s+lp+tl+ib+rs}}\n"
  "function sipCalc(){"),
 ("if(rt){PCS.push(run(r,c[0]));", "if(rt){const p0=run(r,c[0]);p0.inl=1;PCS.push(p0);"),
 ("PCS.forEach(pc=>{const n=pc.nodes;pc.a=U.get(n[0]);", "PCS.forEach(pc=>{const n=pc.nodes;pc.sag=0;pc.loops=0;for(let i=1;i<n.length;i++)pc.sag+=sipSag(LEN.get(kk(n[i-1],n[i]))||0).d;pc.a=U.get(n[0]);"),
 ("if(d.p.t=='A'||t>=45){d.anc+=2;d.ia=true}", "if(d.p.t=='A'||t>=45){d.anc+=2;d.ia=true;pc.loops++}"),
 ("const need=pc.len*SIPN.sipK+2*SIPN.tail;if(need<=drum)it.push({pc,need,part:1,parts:1});else{const k=Math.ceil(need/drum);",
  "let need=sipNeed(pc).all;if(need<=drum)it.push({pc,need,part:1,parts:1});else{const jx=2*SIPN.tail+SIPN.loop;let k=Math.ceil(need/drum);while((need+(k-1)*jx)/k>drum)k++;need+=(k-1)*jx;"),
 ("o.pcs=C.PCS.filter(pc=>tpOk(pc.a));o.cut=sipCut(o.pcs,SIPDR);",
  "o.pcs=C.PCS.filter(pc=>tpOk(pc.a));o.cut=sipCut(o.pcs,SIPDR);o.nd={len:0,sag:0,loops:0,tails:0,inl:0,res:0,all:0};o.loopN=0;o.inlN=0;o.pcs.forEach(pc=>{const z=sipNeed(pc);Object.keys(o.nd).forEach(k=>o.nd[k]+=z[k]);o.loopN+=pc.loops||0;o.inlN+=pc.inl?1:0});o.jx=o.cut.joints*(2*SIPN.tail+SIPN.loop);o.need=o.nd.all+o.jx;"),
 ("E.forEach(x=>{const r=T(x.a.tp);r.sp++;r.len+=x.len;if(x.kind!='t')r.br+=x.len});",
  "E.forEach(x=>{const r=T(x.a.tp);r.sp++;r.len+=x.len;if(x.kind!='t')r.br+=x.len});o.pcs.forEach(pc=>{const r=T(pc.a.tp);r.need=(r.need||0)+sipNeed(pc).all});"),
 ("['СИП-4 4×25','м','длина пролётов по карте, м',Math.round(o.len),n.sipK,'длина × 1,02 на провис','sip'],",
  "['СИП-4 4×25','м','расчёт по отрезкам, м',Math.ceil(o.need),1,'пролёты '+Math.round(o.nd.len)+' м + провис по каждому пролёту '+o.nd.sag.toFixed(1).replace('.',',')+' м + шлейфы на анкерных и угловых опорах '+o.loopN+' × '+String(n.loop).replace('.',',')+' м + хвосты на концах отрезков '+(2*o.pcs.length)+' × '+String(n.tail).replace('.',',')+' м + опуск к бронекабелю на вводе '+o.inlN+' × '+String(n.inlT).replace('.',',')+' м'+(o.cut.joints?' + стыки '+o.cut.joints+' × '+String(2*n.tail+n.loop).replace('.',',')+' м':'')+' + запас на раскатку '+Math.round(n.res*100)+'% ('+Math.round(o.nd.res)+' м)','sip'],"),
 ("(СИП с запасом ≈ ${Math.ceil(x.len*SIPN.sipK)} м)", "<br>стрела провеса ≈ ${sipSag(x.len).f.toFixed(2).replace('.',',')} м · провода в пролёте ≈ ${(x.len+sipSag(x.len).d).toFixed(1).replace('.',',')} м"),
 ("'Длина, м','С запасом (×1,02 + 2×1,5 м), м','Примечание']", "'Длина, м','Провис, м','Шлейфов','Нужно СИП, м','Примечание']"),
 ("f1(pc.len),Math.ceil(pc.len*SIPN.sipK+2*SIPN.tail),pc.nofeed", "f1(pc.len),f1(pc.sag||0),pc.loops||0,Math.ceil(sipNeed(pc).all),pc.nofeed"),
 ("'СИП с запасом 1,02, м'", "'Нужно СИП (провис, шлейфы, хвосты, запас), м'"),
 ("f1(r.br),Math.ceil(r.len*SIPN.sipK),r.pcs", "f1(r.br),Math.ceil(r.need||0),r.pcs"),
]

for f in sys.argv[1:]:
    s = open(f, encoding='utf-8').read()
    if 'function sipNeed(' in s:
        print(f, 'уже применён'); continue
    c = []
    for a, b in R:
        c.append(s.count(a)); s = s.replace(a, b)
    open(f, 'w', encoding='utf-8').write(s); print(f, c)
