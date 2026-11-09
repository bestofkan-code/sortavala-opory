#!/usr/bin/env python3
"""Кнопка «Создать отчёты за сегодня»: три PDF за выбранный день —
1) «ДД.ММ.ГГГГ Забуренные котлованы.pdf» (заголовок листа «Закладные», у каждой опоры — какая закладная),
2) «ДД.ММ.ГГГГ Установленные опоры.pdf» (заголовок «Опоры», у опоры — тип ОГС),
3) «ДД.ММ.ГГГГ Установленные кронштейны и светильники.pdf» (заголовок «Кронштейны и светильники»).
На листе — подложка, линии, опоры за день с подписями; без условных обозначений и без названия карты.
Код — tools/reports.js. Повторный запуск заменяет код на актуальный:
    python3 tools/patch_main_reports.py redaktor.html
"""
import os
import re
import sys

path = sys.argv[1]
s = open(path, encoding='utf-8').read()
js = open(os.path.join(os.path.dirname(__file__), 'reports.js'), encoding='utf-8').read()
B, E = '/* ---- отчёты за день (3 PDF): BEGIN ---- */', '/* ---- отчёты за день (3 PDF): END ---- */'

if 'id="drb"' in s:
    s = re.sub(re.escape(B) + r'.*?' + re.escape(E) + r'\n?', lambda m: js, s, count=1, flags=re.S)
    open(path, 'w', encoding='utf-8').write(s)
    print('updated')
    sys.exit(0)


def R(old, new, cnt=1):
    global s
    n = s.count(old)
    assert n == cnt, (old[:90], n)
    s = s.replace(old, new)


# 1) блок с кнопкой — под кнопкой «СИП-карта» (виден на основной карте, на карте просмотра и на монтажной)
R('<div id="sipp" hidden>',
  '<div id="drbox"><div class="r"><input type="date" id="drd" title="День, за который делать отчёты">'
  '<button class="b" id="drb">Создать отчёты за сегодня</button></div>'
  '<small id="drs">Три PDF: забуренные котлованы (закладные), установленные опоры, установленные кронштейны и светильники.</small>'
  '<div id="drl"></div></div>'
  '<div id="sipp" hidden>')

# 2) стили
R('#sipbar{margin:8px 0 2px}',
  '#sipbar{margin:8px 0 2px}#drbox{margin:2px 0 4px}#drbox .r{flex-wrap:nowrap}#drd{flex:0 0 auto}#drb{flex:1;font-weight:600;border-color:#ea580c}'
  '#drs{display:block;opacity:.75;line-height:1.3}#drl{font-size:12px;line-height:1.5;margin-top:2px}#drl a{color:inherit}')

# 3) код
R('/* ---- контракт и выполнение: опоры, кронштейны, светильники ---- */',
  js + '/* ---- контракт и выполнение: опоры, кронштейны, светильники ---- */')

open(path, 'w', encoding='utf-8').write(s)
print('ok')
