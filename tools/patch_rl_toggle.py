#!/usr/bin/env python3
"""Совместная подвеска — по кнопке на карте. Кнопка слева под масштабом: включена — линии совместной подвески
красные, как раньше (и при фильтре «Только совместная подвеска»); выключена — линий нет, остаётся красная точка у опоры.
Состояние кнопки запоминается в браузере.
Применяется к redaktor.html (один раз): python3 tools/patch_rl_toggle.py redaktor.html
"""
import sys
path = sys.argv[1]
s = open(path, encoding='utf-8').read()
if 'var RLON=' in s:
    print('already applied'); sys.exit(0)
def R(old, new, cnt=1):
    global s
    n = s.count(old); assert n == cnt, (old[:80], n); s = s.replace(old, new)
R("rlinks().forEach(([a,b,pts])=>L.polyline(epath(a,b,pts),{color:'#dc2626',weight:2,opacity:.4,interactive:false}).addTo(ll));",
  "if(RLON||FJ)rlinks().forEach(([a,b,pts])=>L.polyline(epath(a,b,pts),{color:'#dc2626',weight:4,opacity:.9,interactive:false}).addTo(ll));")
R("border-top:2px solid rgba(220,38,38,.45);vertical-align:middle;margin-right:5px\"></i>совм. подвеска",
  "border-top:3px solid #dc2626;vertical-align:middle;margin-right:5px\"></i>совм. подвеска (линии — кнопкой «СП» на карте)")
R("function lines(){ll.clearLayers();",
  "var RLON=false;try{RLON=localStorage.getItem(KEY+'_rl')==='1'}catch(e){}\n"
  "{const C=L.Control.extend({options:{position:'topleft'},onAdd(){const d=L.DomUtil.create('div','leaflet-bar');d.innerHTML='<a href=\"#\" id=\"rlb\" title=\"Совместная подвеска: показать или скрыть линии\" style=\"width:auto;padding:0 7px;font:700 12px/30px system-ui,sans-serif;display:flex;align-items:center;gap:4px\"><i style=\"display:inline-block;width:14px;border-top:3px solid #dc2626\"></i>СП</a>';"
  "L.DomEvent.disableClickPropagation(d);d.querySelector('a').onclick=e=>{e.preventDefault();RLON=!RLON;try{localStorage.setItem(KEY+'_rl',RLON?'1':'0')}catch(er){}rlBtn();lines();toast(RLON?'Линии совместной подвески показаны':'Линии совместной подвески скрыты — красные точки у опор остаются')};return d}});"
  "new C().addTo(map)}\n"
  "function rlBtn(){const a=document.getElementById('rlb');if(!a)return;a.style.background=RLON?'#dc2626':'';a.style.color=RLON?'#fff':'';a.querySelector('i').style.borderTopColor=RLON?'#fff':'#dc2626'}\n"
  "setTimeout(rlBtn,0);\n"
  "function lines(){ll.clearLayers();")
open(path, 'w', encoding='utf-8').write(s); print('ok', path)
