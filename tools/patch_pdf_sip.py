#!/usr/bin/env python3
"""PDF общего плана: в сводке справа — сколько СИП протянуто (≈ м, пролётов), и за период фильтра дат.
Пролёт считается протянутым, если на обеих его опорах отмечено «Протянут СИП»; длина — по СИП-карте.
Применяется к redaktor.html (один раз): python3 tools/patch_pdf_sip.py redaktor.html
"""
import sys
path = sys.argv[1]
s = open(path, encoding='utf-8').read()
if 'SIPI=' in s:
    print('already applied'); sys.exit(0)
def R(old, new, cnt=1):
    global s
    n = s.count(old); assert n == cnt, (old[:80], n); s = s.replace(old, new)
R("const pf=$('wdf').value,pt2=$('wdt').value,PR=",
  "const pf=$('wdf').value,pt2=$('wdt').value,"
  "SIPI=(()=>{try{const C=sipCalc(),inS=new Set(SHT.map(p=>p.uid)),m5=p=>wdone(p,5),ir=v=>/^\\d{4}-/.test(v)&&(!pf||v>=pf)&&(!pt2||v<=pt2);let L=0,n=0,Lp=0,np=0;"
  "C.ED.forEach(x=>{if(!(inS.has(x.a.uid)||inS.has(x.b.uid))||!m5(x.a)||!m5(x.b))return;L+=x.len;n++;const d=[String(wd(x.a,5)),String(wd(x.b,5))].sort()[1];if((pf||pt2)&&ir(d)){Lp+=x.len;np++}});return{L,n,Lp,np}}catch(e){return null}})(),"
  "SM=v=>(v<1000?String(Math.round(v)):(Math.round(v/10)*10).toLocaleString('ru-RU'))+' м',"
  "PR=")
R("`  опор установлено: ${c(4)}`,'']",
  "`  опор установлено: ${c(4)}`,...(SIPI?[`  СИП протянуто: ≈ ${SM(SIPI.Lp)} (${SIPI.np} пролётов)`]:[]),'']")
R("`Опор установлено: ${S.ins}`,",
  "`Опор установлено: ${S.ins}`,...(SIPI?[`СИП протянут: ≈ ${SM(SIPI.L)} (${SIPI.n} пролётов)`]:[]),")
open(path, 'w', encoding='utf-8').write(s); print('ok', path)
