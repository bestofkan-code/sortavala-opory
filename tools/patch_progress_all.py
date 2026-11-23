#!/usr/bin/env python3
"""«Ход работ»: вверху — общий прогресс по всем работам контракта.
Общий % = среднее по 7 видам работ (каждый не больше 100%):
котлованы, закладные, бетон, опоры (из 0), кронштейны установлено (из 0), светильники (из 0), СИП (≈ м из N).
Серые, исключённые и опоры на гравитационном фундаменте не считаются (как в остальном «Ходе работ»).
  for f in redaktor.html prosmotr.html zamechaniya.html zamechaniya-prosmotr.html montazh.html uchastki.html; do python3 tools/patch_progress_all.py $f; done
"""
import sys
path = sys.argv[1]
s = open(path, encoding='utf-8').read()
if 'function hwAllH(' in s:
    print('already applied', path); sys.exit(0)
old = 'return `<div style="padding:6px 8px;margin-bottom:8px;background:#eef3fb'
if s.count(old) != 1:
    print('skip (нет блока «Ход работ»)', path); sys.exit(0)
s = s.replace(old, 'return (()=>{try{return hwAllH(A)}catch(e){return \'\'}})()+`<div style="padding:6px 8px;margin-bottom:8px;background:#eef3fb')
FN = r"""function hwAllH(A){const K=0,c=f=>A.filter(f).length,pc=(v,T)=>T?Math.min(100,v/T*100):0;
 const sv=A.reduce((a,p)=>a+(wdone(p,6)?(+p.sv||Math.max(1,+p.kr||1)):0),0);let L=0;try{const C=sipCalc(),ok=p=>!p.x&&wdone(p,5);C.ED.forEach(x=>{if(ok(x.a)&&ok(x.b))L+=x.len})}catch(e){}
 const it=[['котл.',pc(c(p=>wdone(p,1)),K)],['закл.',pc(c(p=>wdone(p,2)),K)],['бетон',pc(c(p=>wdone(p,3)),K)],['опоры',pc(c(p=>p.done),K)],['кроншт.',pc(c(p=>wdone(p,12)),K)],['свет.',pc(sv,0)],['СИП',pc(L,0)]];
 const t=it.reduce((a,x)=>a+x[1],0)/it.length,f=v=>(Math.round(v*10)/10).toLocaleString('ru-RU');
 return `<div style="padding:7px 9px;margin-bottom:8px;border:1px solid #1d4ed8;border-radius:6px;background:rgba(29,78,216,.12)"><div style="display:flex;justify-content:space-between;align-items:baseline"><b>Общий прогресс работ</b><b style="font-size:17px;color:#60a5fa">${f(t)}%</b></div>`
  +`<div style="height:9px;background:rgba(127,127,127,.25);border-radius:5px;overflow:hidden;margin:4px 0 5px"><i style="display:block;height:100%;width:${Math.min(100,t)}%;background:#3b82f6"></i></div>`
  +`<div style="display:flex;flex-wrap:wrap;gap:2px 9px;font-size:11px;opacity:.85">${it.map(([n,v])=>`<span>${n} <b>${Math.round(v)}%</b></span>`).join('')}</div>`
  +`<small style="display:block;margin-top:3px;opacity:.7">Среднее по 7 видам работ: котлованы, закладные, бетон, опоры, кронштейны (из 0), светильники (из 0), СИП (из N м).</small></div>`}
"""
s = s.replace("function stats(){", FN + "function stats(){", 1)
open(path, 'w', encoding='utf-8').write(s); print('ok', path)
