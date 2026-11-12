#!/usr/bin/env python3
"""Кнопка «Не забетонированные»: на карте только опоры, где отмечены «Забурен котлован» и «Установлена закладная»,
а «Забетонирована» не отмечена (без исключённых, серых и гравитационных). Рядом — сколько таких опор.
Применяется к redaktor.html (один раз): python3 tools/patch_nb.py redaktor.html
"""
import sys
path = sys.argv[1]
s = open(path, encoding='utf-8').read()
if "id=\"nbb\"" in s:
    print('already applied'); sys.exit(0)
def R(old, new, cnt=1):
    global s
    n = s.count(old); assert n == cnt, (old[:80], n); s = s.replace(old, new)
R('<button class="b" id="fjb" style="border-color:#dc2626">Только совместная подвеска</button><small id="fjs"></small></div>',
  '<button class="b" id="fjb" style="border-color:#dc2626">Только совместная подвеска</button><small id="fjs"></small></div>'
  '<div class="r"><button class="b" id="nbb" style="border-color:#0891b2">Не забетонированные</button><small id="nbs"></small></div>')
R("function vis(p){return ftyOk(p)&&visB(p)}",
  "var NB=false;try{NB=localStorage.getItem(KEY+'_nb')==='1'}catch(e){}\n"
  "function nbOk(p){return !p.x&&!p.pp&&!isG(p)&&wdone(p,1)&&wdone(p,2)&&!wdone(p,3)}\n"
  "function nbUI(){const b=$('nbb');if(!b)return;b.style.background=NB?'#0891b2':'';b.style.color=NB?'#fff':'';b.textContent=NB?'Показаны не забетонированные ✕':'Не забетонированные';"
  "const n=P.filter(p=>nbOk(p)&&tpOk(p)).length;$('nbs').innerHTML='котлован и закладная есть, бетона нет: <b>'+n+'</b> '+(n%10==1&&n%100!=11?'опора':n%10>=2&&n%10<=4&&(n%100<12||n%100>14)?'опоры':'опор')}\n"
  "function vis(p){return ftyOk(p)&&visB(p)&&(!NB||nbOk(p))}")
R("$('fjb').onclick=",
  "$('nbb').onclick=()=>{NB=!NB;try{localStorage.setItem(KEY+'_nb',NB?'1':'0')}catch(e){}nbUI();P.forEach(upd);numLabels();if(NB){const L2=P.filter(p=>nbOk(p)&&tpOk(p));if(L2.length)map.fitBounds(L.latLngBounds(L2.map(p=>[p.lat,p.lon])).pad(.15),{maxZoom:18});else toast('Таких опор нет: везде, где стоит закладная, отмечен и бетон')}};setTimeout(nbUI,0);\n"
  "{const _st=stats;stats=function(){const r=_st.apply(this,arguments);try{nbUI()}catch(e){}return r}}\n"
  "$('fjb').onclick=")
open(path, 'w', encoding='utf-8').write(s); print('ok', path)
