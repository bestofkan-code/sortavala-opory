#!/usr/bin/env python3
"""Линии (пролёты) — в цвет своей ТП. Пролёт между опорами одной ТП — цвет этой ТП, между опорами разных ТП —
тёмно-серый. Пролёт с измеренной длиной СИП — толще, с подписью длины. Серые (предлагаемые) — как были.
В легенде — цвета ТП. Значок ТП обведён её цветом.
Применяется к redaktor.html (один раз): python3 tools/patch_tp_colors.py redaktor.html
"""
import sys
path = sys.argv[1]
s = open(path, encoding='utf-8').read()
if 'function tpCol(' in s:
    print('already applied'); sys.exit(0)
def R(old, new, cnt=1):
    global s
    n = s.count(old); assert n == cnt, (old[:80], n); s = s.replace(old, new)
R("L.polyline(path,has?{color:'#f97316',weight:4,opacity:.95,interactive:false}:{color:'#2563eb',weight:2,opacity:.7,dashArray:dash,interactive:false}).addTo(ll);",
  "const pa=pbu(ua),pq=pbu(ub),tc=pa&&pq&&String(pa.tp||'')==String(pq.tp||'')?tpCol(pa.tp):'#475569';"
  "L.polyline(path,has?{color:tc,weight:5,opacity:.95,interactive:false}:{color:tc,weight:3,opacity:.85,dashArray:dash,interactive:false}).addTo(ll);")
R("function spanLine(ua,ub,a,b,dash,pts){",
  "var TPCL=['#2563eb','#16a34a','#9333ea','#db2777','#0891b2','#ca8a04','#4f46e5','#059669','#c2410c','#0d9488','#0284c7','#65a30d','#1e40af','#a21caf','#b45309','#7c3aed','#0e7490','#15803d'],TPCM=null,PBU=null;\n"
  "function tpList(){return [...new Set(P.map(p=>String(p.tp||'')).filter(Boolean))].sort((x,y)=>x.localeCompare(y,'ru',{numeric:true}))}\n"
  "function tpCol(t){t=String(t||'');if(!TPCM||!TPCM.has(t)){TPCM=new Map(tpList().map((x,i)=>[x,TPCL[i%TPCL.length]]))}return TPCM.get(t)||'#475569'}\n"
  "function pbu(u){if(!PBU||PBU.size!=P.length)PBU=new Map(P.map(p=>[p.uid,p]));return PBU.get(u)}\n"
  "function tpLeg(){const e=document.getElementById('tplg');if(!e)return;e.innerHTML='Линии — в цвет своей ТП: '+tpList().map(t=>`<span style=\"white-space:nowrap;margin-right:6px\"><i style=\"display:inline-block;width:16px;height:0;border-top:4px solid ${tpCol(t)};vertical-align:middle;margin-right:3px\"></i>${esc(tpn(t))}</span>`).join('')+'<span style=\"white-space:nowrap\"><i style=\"display:inline-block;width:16px;height:0;border-top:4px solid #475569;vertical-align:middle;margin-right:3px\"></i>между ТП</span>'}\n"
  "function spanLine(ua,ub,a,b,dash,pts){")
R('<i style="display:inline-block;width:18px;height:0;border-top:4px solid #f97316;vertical-align:middle;margin-right:6px"></i>СИП проложен (длина)',
  '<i style="display:inline-block;width:18px;height:0;border-top:5px solid #475569;vertical-align:middle;margin-right:6px"></i>толстая с подписью — длина СИП измерена')
R('жёлтый — светильник (1 из 2)<br>', 'жёлтый — светильник (1 из 2)<br><div id="tplg" style="margin:3px 0;line-height:1.7"></div>')
R("function tpDraw(){if(typeof TPLY=='undefined')return;TPLY.clearLayers();",
  "function tpDraw(){if(typeof TPLY=='undefined')return;TPLY.clearLayers();try{tpLeg()}catch(e){}")
# значок ТП — обводка цветом ТП
R("const html='<div class=\"tpi s'+st+'\" title=",
  "const html='<div class=\"tpi s'+st+'\" style=\"box-shadow:0 0 0 3px '+tpCol(t)+'\" title=")
open(path, 'w', encoding='utf-8').write(s); print('ok', path)
