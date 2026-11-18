#!/usr/bin/env python3
"""Телефон: кнопка на карте внизу слева — скрыть/показать нижнюю панель с таблицами (карта на весь экран).
Состояние запоминается в браузере. На экранах шире 700 px кнопки нет.
  for f in redaktor.html prosmotr.html zamechaniya.html zamechaniya-prosmotr.html montazh.html uchastki.html; do python3 tools/patch_mfull.py $f; done
"""
import sys
path = sys.argv[1]
s = open(path, encoding='utf-8').read()
if 'MFULL' in s:
    print('already applied', path); sys.exit(0)
old = '@media(max-width:700px){body{flex-direction:column-reverse}#s{width:100%;height:45vh}}'
assert s.count(old) == 1, path
s = s.replace(old, old + '@media(max-width:700px){body.mfull #s{display:none}}.mfb{display:none}'
              '@media(max-width:700px){.leaflet-control.mfb{display:flex;align-items:center;gap:5px;height:34px;padding:0 11px;border-radius:9px;'
              'background:#1d2230;color:#e5e7eb;border:1px solid #2c3346;font:600 12px system-ui,sans-serif;cursor:pointer;box-shadow:0 2px 8px rgba(0,0,0,.35)}}')
i = s.index("const map=L.map('m',"); j = s.index(';', s.index('.setView(', i)) + 1
JS = r"""
/*MFULL*/{let MF=false;try{MF=localStorage.getItem(KEY+'_mfull')==='1'}catch(e){}
 const C=L.Control.extend({options:{position:'bottomleft'},onAdd(){const b=L.DomUtil.create('div','leaflet-control mfb');L.DomEvent.disableClickPropagation(b);
  const ui=()=>{document.body.classList.toggle('mfull',MF);b.textContent=MF?'▲ Таблицы':'▼ Скрыть таблицы';b.title=MF?'Показать панель с таблицами':'Скрыть панель с таблицами — карта на весь экран'};
  b.onclick=()=>{MF=!MF;try{localStorage.setItem(KEY+'_mfull',MF?'1':'0')}catch(e){}ui();setTimeout(()=>{map.invalidateSize({pan:false});const el=document.querySelector('.leaflet-popup.side');if(el&&typeof sdPos=='function')sdPos(el)},60)};
  ui();setTimeout(()=>map.invalidateSize({pan:false}),60);return b}});
 map.addControl(new C())}
"""
s = s[:j] + JS + s[j:]
open(path, 'w', encoding='utf-8').write(s); print('ok', path)
