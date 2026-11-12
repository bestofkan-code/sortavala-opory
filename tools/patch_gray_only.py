#!/usr/bin/env python3
"""Кнопка «Только серые (предполагаемые)»: на карте только серые опоры (без исключённых), рядом — сколько их.
С кнопкой «Не забетонированные» не совмещается: включение одной выключает другую.
Применяется к redaktor.html (один раз, после patch_nb.py): python3 tools/patch_gray_only.py redaktor.html
"""
import sys
path = sys.argv[1]
s = open(path, encoding='utf-8').read()
if 'id="gyb"' in s:
    print('already applied'); sys.exit(0)
def R(old, new, cnt=1):
    global s
    n = s.count(old); assert n == cnt, (old[:80], n); s = s.replace(old, new)
R('<div class="r"><button class="b" id="nbb" style="border-color:#0891b2">Не забетонированные</button><small id="nbs"></small></div>',
  '<div class="r"><button class="b" id="nbb" style="border-color:#0891b2">Не забетонированные</button><small id="nbs"></small></div>'
  '<div class="r"><button class="b" id="gyb" style="border-color:#6b7280">Только серые (предполагаемые)</button><small id="gys"></small></div>')
R("function vis(p){return ftyOk(p)&&visB(p)&&(!NB||nbOk(p))}",
  "var GY=false;try{GY=localStorage.getItem(KEY+'_gy')==='1'}catch(e){}if(GY&&NB)NB=false;\n"
  "function gyOk(p){return !!p.pp&&!p.x}\n"
  "function gyUI(){const b=$('gyb');if(!b)return;b.style.background=GY?'#6b7280':'';b.style.color=GY?'#fff':'';b.textContent=GY?'Показаны только серые ✕':'Только серые (предполагаемые)';"
  "const n=P.filter(p=>gyOk(p)&&tpOk(p)).length;$('gys').innerHTML='серых опор: <b>'+n+'</b>'}\n"
  "function vis(p){return ftyOk(p)&&visB(p)&&(!NB||nbOk(p))&&(!GY||gyOk(p))}")
R("$('nbb').onclick=()=>{NB=!NB;",
  "$('gyb').onclick=()=>{GY=!GY;if(GY&&NB){NB=false;try{localStorage.setItem(KEY+'_nb','0')}catch(e){}nbUI()}try{localStorage.setItem(KEY+'_gy',GY?'1':'0')}catch(e){}gyUI();P.forEach(upd);numLabels();"
  "if(GY){const L2=P.filter(p=>gyOk(p)&&tpOk(p));if(L2.length)map.fitBounds(L.latLngBounds(L2.map(p=>[p.lat,p.lon])).pad(.15),{maxZoom:18});else toast('Серых опор нет')}};setTimeout(gyUI,0);\n"
  "$('nbb').onclick=()=>{NB=!NB;if(NB&&GY){GY=false;try{localStorage.setItem(KEY+'_gy','0')}catch(e){}gyUI()}")
R("{const _st=stats;stats=function(){const r=_st.apply(this,arguments);try{nbUI()}catch(e){}return r}}",
  "{const _st=stats;stats=function(){const r=_st.apply(this,arguments);try{nbUI();gyUI()}catch(e){}return r}}")
open(path, 'w', encoding='utf-8').write(s); print('ok', path)
