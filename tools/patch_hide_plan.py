#!/usr/bin/env python3
"""Убрать блок «План работ» (по просьбе Иля 12.11): блок скрыт, маршрут плана на карте не рисуется.
Задания и «Порядок обхода» в режиме «Задания бригаде» остаются.
Применяется к redaktor.html (один раз): python3 tools/patch_hide_plan.py redaktor.html
"""
import sys
path = sys.argv[1]
s = open(path, encoding='utf-8').read()
if '#pld{display:none!important}' in s:
    print('already applied'); sys.exit(0)
def R(old, new, cnt=1):
    global s
    n = s.count(old); assert n == cnt, (old[:80], n); s = s.replace(old, new)
R('.tki2.dn{opacity:.55}', '.tki2.dn{opacity:.55}#pld{display:none!important}')
R("setTimeout(()=>{plDraw();plUI()},1500);", "plDraw=function(){PLLY.clearLayers()};PLID=null;try{localStorage.removeItem(KEY+'_pl')}catch(e){}setTimeout(()=>{plDraw();plUI()},1500);")
open(path, 'w', encoding='utf-8').write(s); print('ok', path)
