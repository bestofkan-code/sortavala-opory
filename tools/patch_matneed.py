#!/usr/bin/env python3
"""«Материалы на складе»: колонки «Нужно всего» и «Не хватает».
  Нужно всего — та же норма, что для «Ушло», но по всей сети карты (все пролёты СИП, все светильники,
  все опоры с отметкой «заземление»). СИП — с провисом, петлями, хвостами и опусками (sipNeed).
  Новые нормы: клеммы 222-413 — 3 на светильник (mkey term); круг Ø12 — 10 м × 0,888 кг/м на заземление (gzr, т);
  уголок 50×5 — 5 м × 3,77 кг/м на заземление (gza, т); ВВГ 3×1,5 — SIPN.vvg м на светильник.
Применение: python3 tools/patch_matneed.py <file.html>
"""
import sys
path = sys.argv[1]
s = open(path, encoding='utf-8').read()
if 'function matUse(all)' in s:
    print('already', path); sys.exit(0)
def R(old, new, cnt=1):
    global s
    n = s.count(old); assert n == cnt, (path, old[:70], n); s = s.replace(old, new)
R("zoi:'3 на светильник'};", "zoi:'3 на светильник',pierce:'3 на светильник + 1 на перемычку PEN',hook:'1 на анкерный и поддерживающий зажим',tape:'1,5 м на крюк',clip:'1 на метр ленты',len:'по пролётам; «нужно» — с провисом, петлями, хвостами и опусками',term:'3 на светильник (L, N, PE)',gzr:'10 м круга Ø12 на заземление (0,888 кг/м)',gza:'2 уголка × 2,5 м на заземление (3,77 кг/м)',vvg:SIPN.vvg+' м на светильник'};")
R("function matUse(){const C=sipCalc(),E=C.ED.filter(e=>wdone(e.a,5)&&wdone(e.b,5))",
  "function matUse(all){const C=sipCalc(),E=all?C.ED:C.ED.filter(e=>wdone(e.a,5)&&wdone(e.b,5))")
R("o.bond++;if(wdone(p,6))o.zoi+=3*(+p.sv||Math.max(1,+p.kr||1))});",
  "o.bond++;if(all||wdone(p,6))o.zoi+=3*(+p.sv||Math.max(1,+p.kr||1))});")
R("o.tape=Math.round(o.hook*1.5*10)/10;o.clip=Math.ceil(o.tape);return o}",
  "o.tape=Math.round(o.hook*1.5*10)/10;o.clip=Math.ceil(o.tape);o.term=o.zoi;o.vvg=Math.round(o.zoi/3*SIPN.vvg*10)/10;"
  "const gn=P.filter(p=>gzEl(p)&&(all||wdone(p,15))).length;o.gz=gn;o.gzr=gn*10*0.888/1000;o.gza=gn*5*3.77/1000;"
  "if(all)o.len=(C.PCS||[]).reduce((a,pc)=>a+sipNeed(pc).all,0);return o}")
R("let U={};try{U=matUse()}catch(e){}", "let U={},N={};try{U=matUse()}catch(e){}try{N=matUse(1)}catch(e){}")
R("const G=new Map(),f=v=>(Math.round(v*10)/10).toLocaleString('ru-RU')", "const G=new Map(),f=(v,u)=>u=='т'?(Math.round(v*1000)/1000).toLocaleString('ru-RU'):(Math.round(v*10)/10).toLocaleString('ru-RU')")
R("<th>Остаток</th></tr>',neg=0;", "<th>Остаток</th><th>Нужно всего</th><th>Не хватает</th></tr>',neg=0,sh=0;")
R("""rest=u==null?null:g.q-u;if(rest!=null&&rest<0)neg++;""",
  """rest=u==null?null:g.q-u,nd=g.key&&N[g.key]!=null?N[g.key]:null,mi=nd==null?null:Math.max(0,nd-g.q);if(rest!=null&&rest<0)neg++;if(mi>0.0005)sh++;""")
R("""<td>${f(g.q)} ${esc(g.unit)}</td><td title="${esc(MATK[g.key]||'расход по карте не считается')}">${u==null?'—':f(u)}</td><td class="${rest!=null&&rest<0?'neg':''}">${rest==null?'—':f(rest)}</td></tr>`""",
  """<td>${f(g.q,g.unit)} ${esc(g.unit)}</td><td title="${esc(MATK[g.key]||'расход по карте не считается')}">${u==null?'—':f(u,g.unit)}</td><td class="${rest!=null&&rest<0?'neg':''}">${rest==null?'—':f(rest,g.unit)}</td><td title="${esc(MATK[g.key]||'норма не задана')}">${nd==null?'—':f(nd,g.unit)}</td><td class="${mi>0.0005?'neg':''}">${mi==null?'—':mi>0.0005?f(mi,g.unit):'хватает'}</td></tr>`""")
R("«—» — для позиции норма расхода по карте не задана.",
  "«Нужно всего» — по тем же нормам на всю сеть карты (все пролёты СИП, ${N.zoi?N.zoi/3:0} светильников, ${N.gz||0} заземлений); «Не хватает» = нужно всего − пришло. «—» — для позиции норма расхода по карте не задана.")
R("$('mats').textContent=neg?' · не хватает: '+neg:''}", "$('mats').textContent=(sh?' · докупить: '+sh+' поз.':'')+(neg?' · ушло больше прихода: '+neg:'')}")
open(path, 'w', encoding='utf-8').write(s); print('ok', path)
