#!/usr/bin/env python3
"""Кнопка «СИП-карта»: режим, в котором видно, как пойдёт СИП по опорам — магистраль и ответвления,
длина каждого пролёта, роль опоры на линии (концевая, анкерная, угловая, ответвительная, промежуточная)
и приблизительный расчёт арматуры с выгрузкой в Excel. Код режима — tools/sip.js.
Применяется к redaktor.html (один раз): python3 tools/patch_main_sip.py redaktor.html
"""
import os
import sys

path = sys.argv[1]
s = open(path, encoding='utf-8').read()
if 'id="sipb"' in s:
    print('already applied')
    sys.exit(0)
js = open(os.path.join(os.path.dirname(__file__), 'sip.js'), encoding='utf-8').read()


def R(old, new, cnt=1):
    global s
    n = s.count(old)
    assert n == cnt, (old[:90], n)
    s = s.replace(old, new)


# 1) кнопка и панель — сразу под таблицей «Контракт и выполнение», вне блока редактирования (видны и на карте просмотра, и на монтажной)
R('Красным — расхождение карты с контрактом.</small></details>',
  'Красным — расхождение карты с контрактом.</small></details>'
  '<div class="r" id="sipbar"><button class="b" id="sipb" title="Показать, как пойдёт СИП по опорам, длины пролётов и расчёт арматуры">СИП-карта</button></div>'
  '<div id="sipp" hidden><b>СИП-карта — как пойдёт СИП</b>'
  '<small style="display:block;margin:2px 0 4px"><span style="color:#3b82f6;font-weight:700">Синяя</span> — магистраль от опоры ввода до самой дальней опоры, '
  '<span style="color:#f97316;font-weight:700">оранжевая</span> — ответвления, <span style="color:#9ca3af;font-weight:700">серый пунктир</span> — отрезки только к опорам на гравитационном фундаменте (следующий этап). '
  'Кольцо <span style="color:#f87171;font-weight:700">красное</span> — СИП крепится анкерно (ввод, конец линии, анкерная или угловая опора), '
  '<span style="color:#e879f9;font-weight:700">фиолетовое</span> — ответвление. Длины пролётов видны при приближении. Нажмите на опору или пролёт — подробности.</small>'
  '<div id="sips"></div><div class="r"><button id="sipx">Расчёт арматуры (Excel)</button></div>'
  '<small style="display:block;opacity:.75">Расчёт приблизительный: длины — по прямой между опорами по нарисованным линиям; нормы указаны в таблице и меняются в Excel.</small></div>')

# 2) скрытая кнопка режима (переключается кнопкой «СИП-карта»)
R('<button class="b" data-m="task" style="border-color:#22d3ee">Задания бригаде</button></div>',
  '<button class="b" data-m="task" style="border-color:#22d3ee">Задания бригаде</button><button class="b" data-m="sip" hidden>СИП-карта</button></div>')

# 3) переключение режима
R("$('spp').hidden=mode!='sp';$('tkp').hidden=mode!='task';",
  "$('spp').hidden=mode!='sp';$('tkp').hidden=mode!='task';$('sipp').hidden=mode!='sip';$('sipb').classList.toggle('on',mode=='sip');try{sipDraw()}catch(e){console.error(e)}")

# 4) нажатие на опору в режиме СИП
R("else if(mode=='sp')L.popup(PO()).setLatLng(m.getLatLng()).setContent(sqMenu(p)).openOn(map);",
  "else if(mode=='sip')L.popup(PO()).setLatLng(m.getLatLng()).setContent(sipPop(p)).openOn(map);else if(mode=='sp')L.popup(PO()).setLatLng(m.getLatLng()).setContent(sqMenu(p)).openOn(map);")

# 5) пересчёт при изменении данных
R('try{skUI()}catch(e){}', 'try{skUI()}catch(e){}try{sipSoon()}catch(e){}')

# 6) стили
R('#ktn{display:block;opacity:.75;margin:2px 0 3px;line-height:1.3}</style>',
  '#ktn{display:block;opacity:.75;margin:2px 0 3px;line-height:1.3}'
  '#sipbar{margin:8px 0 2px}#sipb{width:100%;font-weight:600;border-color:#3b82f6}'
  '#sipp{margin-top:6px;border:1px solid #3b82f6;border-radius:8px;padding:6px 8px}#sipp[hidden]{display:none}#sips>div{margin:3px 0;font-size:12px;line-height:1.35}'
  '#sipt,#siptp{width:100%;border-collapse:collapse;font-size:12px;margin:5px 0 3px}'
  '#sipt th,#sipt td,#siptp th,#siptp td{padding:3px 4px;text-align:right;border-bottom:1px solid rgba(127,127,127,.22);white-space:nowrap;font-variant-numeric:tabular-nums;vertical-align:top}'
  '#sipt th:first-child,#sipt td:first-child,#siptp th:first-child,#siptp td:first-child{text-align:left;white-space:normal}'
  '#sipt th,#siptp th{font-weight:600;font-size:11px;opacity:.85}#sipt td small{display:block;font-size:10px;opacity:.7;line-height:1.15}'
  '#sipd{margin-top:4px}#sipd>summary{cursor:pointer;font-size:12px}'
  '.sipl{transform:translate(-50%,-50%);width:max-content;background:#fff;color:#1e3a8a;font:700 10.5px/1.25 system-ui,sans-serif;padding:0 4px;border-radius:6px;border:1px solid #1d4ed8;box-shadow:0 1px 2px rgba(0,0,0,.25);pointer-events:none;white-space:nowrap}'
  '.sipl.n{color:#4b5563;border-color:#9ca3af}'
  '</style>')

# 7) код режима
R('/* ---- контракт и выполнение: опоры, кронштейны, светильники ---- */',
  js + '/* ---- контракт и выполнение: опоры, кронштейны, светильники ---- */')

open(path, 'w', encoding='utf-8').write(s)
print('ok')
