#!/usr/bin/env python3
"""Кнопка «Не забурены котлованы»: на карте только опоры, где не отмечены «Забурен котлован» и «Установлена закладная»
(без исключённых, серых и гравитационных). Рядом — сколько таких опор.
С «Не забетонированными» и «Только серые» не совмещается: включение одной выключает другие.
Применяется после patch_gray_only.py ко всем страницам с кнопкой «Только серые»:
  for f in redaktor.html prosmotr.html zamechaniya.html zamechaniya-prosmotr.html montazh.html uchastki.html; do python3 tools/patch_nk.py $f; done
"""
import sys
path = sys.argv[1]
s = open(path, encoding='utf-8').read()
if 'id="nkb"' in s:
    print('already applied', path); sys.exit(0)
def R(old, new, cnt=1):
    global s
    n = s.count(old); assert n == cnt, (path, old[:80], n); s = s.replace(old, new)

R('<button class="b" id="gyb" style="border-color:#6b7280">Только серые (предполагаемые)</button><small id="gys"></small></div>',
  '<button class="b" id="gyb" style="border-color:#6b7280">Только серые (предполагаемые)</button><small id="gys"></small></div>'
  '<div class="r"><button class="b" id="nkb" style="border-color:#d97706">Не забурены котлованы</button><small id="nks"></small></div>')

R("function vis(p){return ftyOk(p)&&visB(p)&&(!NB||nbOk(p))&&(!GY||gyOk(p))}",
  "var NK=false;try{NK=localStorage.getItem(KEY+'_nk')==='1'}catch(e){}if(NK){NB=false;GY=false}\n"
  "function nkOk(p){return !p.x&&!p.pp&&!isG(p)&&!wdone(p,1)&&!wdone(p,2)}\n"
  "function nkUI(){const b=$('nkb');if(!b)return;b.style.background=NK?'#d97706':'';b.style.color=NK?'#fff':'';b.textContent=NK?'Показаны не забуренные ✕':'Не забурены котлованы';"
  "const n=P.filter(p=>nkOk(p)&&tpOk(p)).length;$('nks').innerHTML='котлован не забурен: <b>'+n+'</b> '+(n%10==1&&n%100!=11?'опора':n%10>=2&&n%10<=4&&(n%100<12||n%100>14)?'опоры':'опор')}\n"
  "function vis(p){return ftyOk(p)&&visB(p)&&(!NB||nbOk(p))&&(!GY||gyOk(p))&&(!NK||nkOk(p))}")

R("{const _st=stats;stats=function(){const r=_st.apply(this,arguments);try{nbUI();gyUI()}catch(e){}return r}}",
  "{const _st=stats;stats=function(){const r=_st.apply(this,arguments);try{nbUI();gyUI();nkUI()}catch(e){}return r}}\n"
  "function nkOff(){if(!NK)return;NK=false;try{localStorage.setItem(KEY+'_nk','0')}catch(e){}nkUI()}\n"
  "{const a=$('nbb').onclick,b=$('gyb').onclick;$('nbb').onclick=()=>{if(!NB)nkOff();a()};$('gyb').onclick=()=>{if(!GY)nkOff();b()}}\n"
  "$('nkb').onclick=()=>{NK=!NK;if(NK){if(NB){NB=false;try{localStorage.setItem(KEY+'_nb','0')}catch(e){}nbUI()}if(GY){GY=false;try{localStorage.setItem(KEY+'_gy','0')}catch(e){}gyUI()}}"
  "try{localStorage.setItem(KEY+'_nk',NK?'1':'0')}catch(e){}nkUI();P.forEach(upd);numLabels();"
  "if(NK){const L2=P.filter(p=>nkOk(p)&&tpOk(p));if(L2.length)map.fitBounds(L.latLngBounds(L2.map(p=>[p.lat,p.lon])).pad(.15),{maxZoom:18});else toast('Таких опор нет: все котлованы забурены')}};setTimeout(nkUI,0);")

open(path, 'w', encoding='utf-8').write(s); print('ok', path)
