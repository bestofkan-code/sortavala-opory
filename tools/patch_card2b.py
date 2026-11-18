#!/usr/bin/env python3
"""Исправление к patch_card2.py: нажатие ✎ (параметры опоры, сверка) закрывало окно опоры на компьютере.
Кнопка перерисовывалась прямо в обработчике нажатия, Leaflet не находил её внутри окна и считал
нажатие кликом по карте (map.on('click') → closePopup). Перерисовка теперь после обработки нажатия.
  for f in redaktor.html prosmotr.html zamechaniya.html zamechaniya-prosmotr.html montazh.html uchastki.html; do python3 tools/patch_card2b.py $f; done
"""
import sys
path = sys.argv[1]
s = open(path, encoding='utf-8').read()
if 'CARD2B' in s:
    print('already applied', path); sys.exit(0)
def R(old, new, cnt=1):
    global s
    n = s.count(old); assert n == cnt, (path, old[:90], n); s = s.replace(old, new)
R("sm.onclick=()=>{op=!op;try{localStorage.setItem(KEY+'_pexp',op?'1':'0')}catch(e){}draw()}",
  "sm.onclick=()=>{op=!op;try{localStorage.setItem(KEY+'_pexp',op?'1':'0')}catch(e){}setTimeout(draw,0)}")
R("const ch=()=>{upd(p);save();stats();mark(p);vfDraw(b,p)},q=x=>b.querySelector(x)",
  "const ch=()=>{upd(p);save();stats();mark(p);setTimeout(()=>vfDraw(b,p),0)},q=x=>b.querySelector(x)")
R("q('[data-vt]').onclick=()=>{b._op=!op;vfDraw(b,p)};", "q('[data-vt]').onclick=()=>{b._op=!op;setTimeout(()=>vfDraw(b,p),0)};/*CARD2B*/")
R("{const wa=g.querySelector('[data-wall]');if(wa)wa.onclick=()=>{WALL=!WALL;rw()}}",
  "{const wa=g.querySelector('[data-wall]');if(wa)wa.onclick=()=>{WALL=!WALL;setTimeout(rw,0)}}")
open(path, 'w', encoding='utf-8').write(s); print('ok', path)
