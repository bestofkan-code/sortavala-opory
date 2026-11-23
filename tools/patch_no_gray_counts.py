#!/usr/bin/env python3
"""Серые (предлагаемые) опоры не участвуют в подсчётах.

Что меняется:
- таблица «Контракт и выполнение» и сводки под ней (опоры, закладные, кронштейны, светильники, высоты) — без серых;
- «По контракту в этом этапе: 0» и «Не хватает N опор» — без серых, серые показаны отдельной строкой «в счёт не входят»;
- «нет на карте» в таблице и в СИП-карте — без серых;
- счётчик по фильтру работ: «опор контракта» без серых;
- монтажная карта: таблица «Кронштейны» (krTbl) без серых;
- подсказка у галочки «серая (предлаг.)».

Блоки «Проверка кронштейнов», «Проверка котлованов», «Ход работ», склад закладных и подсказки по смете серые уже не считали.

Применяется ко всем страницам (повторный запуск ничего не меняет):
  for f in redaktor.html prosmotr.html zamechaniya.html zamechaniya-prosmotr.html montazh.html uchastki.html; do python3 tools/patch_no_gray_counts.py $f; done
"""
import sys
path = sys.argv[1]
s = open(path, encoding='utf-8').read()
if 'NOGRAYCNT' in s:
    print('already applied', path); sys.exit(0)

def R(old, new, cnt=1, need=True):
    global s
    n = s.count(old)
    if not need and n == 0:
        return
    assert n == cnt, (path, old[:90], n)
    s = s.replace(old, new)

# основная выборка для таблиц и сводок
R("const Q=P.filter(p=>tpOk(p)&&wmatch(p)&&!isG(p)),",
  "const Q=P.filter(p=>tpOk(p)&&wmatch(p)&&!isG(p)&&!p.pp)/*NOGRAYCNT*/,")
# «нет на карте» до 0 — в таблице и в СИП-карте
R("0-P.filter(p=>!p.x&&!isG(p)).length", "0-P.filter(p=>!p.x&&!isG(p)&&!p.pp).length", 2)
# блок «По контракту в этом этапе»
R("A=P.filter(p=>!p.x&&!isG(p)),GA=A.filter(p=>p.pp).length",
  "GA=P.filter(p=>!p.x&&!isG(p)&&p.pp).length,A=P.filter(p=>!p.x&&!isG(p)&&!p.pp)")
R("${GA?`, из них предлагаемых (серых) ${GA}`:''}",
  "${GA?`; серых (предлагаемых) ещё ${GA} — в счёт не входят`:''}")
R("${GA?` (из них предлагаемых (серых) ${GA})`:''}",
  "${GA?` (серых (предлагаемых) ещё ${GA} — в счёт не входят)`:''}")
# счётчик «Подходит опор» по фильтру работ
R("const kc=V.length-x-g;", "const kc=V.length-x-g-gr;")
R("(gr?' (из них серых предлагаемых '+gr+')':'')",
  "(gr?' · серых предлагаемых '+gr+' (не в счёт)':'')")
# подсказка у галочки
R("учитывается в счёте опор по контракту", "в подсчёты (контракт, кронштейны, светильники) не входит")
# монтажная карта: таблица кронштейнов
R("function krTbl(Q,ALL){const C=", "function krTbl(Q,ALL){Q=Q.filter(p=>!p.pp);const C=", need=False)

open(path, 'w', encoding='utf-8').write(s)
print('ok', path)
