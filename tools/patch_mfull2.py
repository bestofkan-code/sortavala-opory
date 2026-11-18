#!/usr/bin/env python3
"""Кнопка скрытия панели и на компьютере (после patch_mfull.py): на широком экране прячет левую панель
(«◀ Скрыть панель» / «▶ Панель»), на телефоне — нижнюю, как раньше.
  for f in redaktor.html prosmotr.html zamechaniya.html zamechaniya-prosmotr.html montazh.html uchastki.html; do python3 tools/patch_mfull2.py $f; done
"""
import sys
path = sys.argv[1]
s = open(path, encoding='utf-8').read()
if 'MFULL2' in s and 'rgba(0,0,0,.35)}}' not in s:
    print('already applied', path); sys.exit(0)
def R(old, new):
    global s
    assert s.count(old) == 1, (path, old[:80]); s = s.replace(old, new)
if 'MFULL2' not in s: R('@media(max-width:700px){body.mfull #s{display:none}}.mfb{display:none}@media(max-width:700px){.leaflet-control.mfb{',
  'body.mfull #s{display:none}/*MFULL2*/.leaflet-control.mfb{')
if "const ph=innerWidth" not in s: R("b.textContent=MF?'▲ Таблицы':'▼ Скрыть таблицы';b.title=MF?'Показать панель с таблицами':'Скрыть панель с таблицами — карта на весь экран'",
  "const ph=innerWidth<=700;b.textContent=ph?(MF?'▲ Таблицы':'▼ Скрыть таблицы'):(MF?'▶ Панель':'◀ Скрыть панель');b.title=MF?'Показать панель с таблицами':'Скрыть панель с таблицами — карта на весь экран'")
if "addEventListener('resize',ui)" not in s: R("ui();setTimeout(()=>map.invalidateSize({pan:false}),60);return b}});",
  "ui();addEventListener('resize',ui);setTimeout(()=>map.invalidateSize({pan:false}),60);return b}});")
R("box-shadow:0 2px 8px rgba(0,0,0,.35)}}", "box-shadow:0 2px 8px rgba(0,0,0,.35)}")
open(path, 'w', encoding='utf-8').write(s); print('ok', path)
