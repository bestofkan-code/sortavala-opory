#!/usr/bin/env python3
"""Запрет масштабирования самой страницы на телефонах (масштабируется только карта).

На iPhone Safari увеличивал всю страницу при нажатии в поле ввода с шрифтом меньше 16 px
и при щипке поверх окна опоры — окно опоры «меняло масштаб» вместе с картой.
- viewport: maximum-scale=1, user-scalable=no (iOS перестаёт увеличивать страницу при вводе);
- gesturestart/gesturechange/gestureend (только Safari) — preventDefault: щипок не масштабирует страницу;
- окно опоры и панели: touch-action pan-x pan-y (прокрутка есть, масштаба страницы нет).
Карта (Leaflet) работает на touch/pointer-событиях, её щипок не затрагивается.
  for f in redaktor.html prosmotr.html zamechaniya.html zamechaniya-prosmotr.html montazh.html uchastki.html vyvoz.html; do python3 tools/patch_nozoom.py $f; done
"""
import sys
path = sys.argv[1]
s = open(path, encoding='utf-8').read()
if 'NOZOOM' in s:
    print('already applied', path); sys.exit(0)
old = '<meta name="viewport" content="width=device-width,initial-scale=1">'
assert s.count(old) == 1, path
s = s.replace(old,
    '<meta name="viewport" content="width=device-width,initial-scale=1,maximum-scale=1,user-scalable=no,viewport-fit=cover">'
    '<style>/*NOZOOM*/html,body{-webkit-text-size-adjust:100%;text-size-adjust:100%}'
    '.leaflet-popup,.leaflet-popup-content-wrapper,.leaflet-popup-content,.pp{touch-action:pan-x pan-y}</style>'
    '<script>/*NOZOOM*/["gesturestart","gesturechange","gestureend"].forEach(function(t){document.addEventListener(t,function(e){e.preventDefault()},{passive:false})});'
    'document.addEventListener("dblclick",function(e){if(!e.target.closest||!e.target.closest(".leaflet-container"))e.preventDefault()},{passive:false});</script>')
open(path, 'w', encoding='utf-8').write(s); print('ok', path)
