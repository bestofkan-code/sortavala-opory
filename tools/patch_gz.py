#!/usr/bin/env python3
"""Кнопка «Нужен котлован под заземление»: на карте только опоры, где отмечено заземление (галочка «заземл.»),
а работа «Котл. заземл.» ещё не отмечена. Исключённые, серые и гравитационные опоры не показываются.
Рядом — сколько таких опор и сколько котлованов уже выкопано.
Применяется ко всем страницам с кнопкой «Не забурены котлованы»:
  for f in redaktor.html prosmotr.html zamechaniya.html zamechaniya-prosmotr.html montazh.html uchastki.html; do python3 tools/patch_gz.py $f; done
"""
import sys
path = sys.argv[1]
s = open(path, encoding='utf-8').read()
if 'id="gzb"' in s:
    print('already applied', path); sys.exit(0)
def R(old, new, cnt=1):
    global s
    n = s.count(old); assert n == cnt, (path, old[:80], n); s = s.replace(old, new)

R('<button class="b" id="nkb" style="border-color:#d97706">Не забурены котлованы</button><small id="nks"></small></div>',
  '<button class="b" id="nkb" style="border-color:#d97706">Не забурены котлованы</button><small id="nks"></small></div>'
  '<div class="r"><button class="b" id="gzb" style="border-color:#65a30d">Нужен котлован под заземление</button><small id="gzs"></small></div>')

R("function vis(p){return ftyOk(p)&&visB(p)&&",
  "var GZF=false;try{GZF=localStorage.getItem(KEY+'_gzf')==='1'}catch(e){}\n"
  "function gzEl(p){return !!p.g&&!p.x&&!p.pp&&!isG(p)}\n"
  "function gzOk(p){return gzEl(p)&&!wdone(p,11)}\n"
  "function gzUI(){const b=$('gzb');if(!b)return;b.style.background=GZF?'#65a30d':'';b.style.color=GZF?'#fff':'';"
  "b.textContent=GZF?'Показаны котлованы под заземление ✕':'Нужен котлован под заземление';"
  "const E=P.filter(p=>gzEl(p)&&tpOk(p)),n=E.filter(p=>!wdone(p,11)).length;"
  "$('gzs').innerHTML='осталось выкопать: <b>'+n+'</b> из '+E.length+' (выкопано '+(E.length-n)+')'}\n"
  "function vis(p){return (!GZF||gzOk(p))&&ftyOk(p)&&visB(p)&&")

JS = ("\n<script>(function(){const b=document.getElementById('gzb');if(!b)return;"
      "b.onclick=()=>{GZF=!GZF;try{localStorage.setItem(KEY+'_gzf',GZF?'1':'0')}catch(e){}gzUI();P.forEach(upd);numLabels();"
      "if(GZF){const L2=P.filter(p=>gzOk(p)&&tpOk(p));if(L2.length)map.fitBounds(L.latLngBounds(L2.map(p=>[p.lat,p.lon])).pad(.15),{maxZoom:17});"
      "else toast('Таких опор нет: все котлованы под заземление выкопаны')}};"
      "try{const _s=stats;stats=function(){const r=_s.apply(this,arguments);try{gzUI()}catch(e){}return r}}catch(e){}"
      "setTimeout(gzUI,0);setTimeout(gzUI,3000)})();</script>\n")
assert s.rstrip().endswith('</html>') or True
i = s.rfind('</body>'); assert i > 0, path
s = s[:i] + JS + s[i:]

open(path, 'w', encoding='utf-8').write(s); print('ok', path)
