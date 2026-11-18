#!/usr/bin/env python3
"""Левая панель с таблицами (компьютер, ширина > 700 px) плотнее: всё содержимое в масштабе 0,86
(шрифт и элементы меньше), меньше отступы в таблицах, у кнопок, полей и заголовков. Ширина панели на экране ≈ 325 px.
  for f in redaktor.html prosmotr.html zamechaniya.html zamechaniya-prosmotr.html montazh.html uchastki.html; do python3 tools/patch_sdense.py $f; done
"""
import sys
path = sys.argv[1]
s = open(path, encoding='utf-8').read()
if 'SDENSE' in s:
    print('already applied', path); sys.exit(0)
CSS = ("@media(min-width:701px){#s{zoom:.86;width:378px!important;padding:6px 8px!important}"
 "#s button{padding:3px 7px!important}#s td,#s th{padding:1px 3px!important}"
 "#s h3{margin:8px 0 3px!important}#s .r{margin:2px 0!important}"
 "#s select,#s input[type=text],#s input[type=date],#s input[type=number],#s input[type=search]{padding:2px 4px!important}"
 "#s .hi{padding:2px 5px!important}#s label.wfc{padding:2px 6px!important}#s details>summary{padding-top:3px!important;padding-bottom:3px!important}}")
JS = "\n/*SDENSE*/{const st=document.createElement('style');st.textContent=" + repr(CSS) + ";(document.body||document.head).appendChild(st)}\n"
i = s.index("const map=L.map('m',"); j = s.index(';', s.index('.setView(', i)) + 1
s = s[:j] + JS + s[j:]
open(path, 'w', encoding='utf-8').write(s); print('ok', path)
