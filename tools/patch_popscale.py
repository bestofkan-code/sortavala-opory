#!/usr/bin/env python3
"""Окно опоры (и другие всплывающие окна карты) уменьшается вместе с картой при отдалении.

Масштаб окна = 2^(текущий зум − зум, при котором окно открыто), не больше 1 и не меньше 0,25:
отдалились на один шаг — окно вдвое меньше, приблизились обратно — снова обычный размер.
Крупнее исходного не становится. Окно сжимается к своему хвостику (к опоре), при щипке — плавно.
Сделано обёрткой L.DomUtil.setPosition, поэтому работает и с поворотом карты (leaflet-rotate).
  for f in redaktor.html prosmotr.html zamechaniya.html zamechaniya-prosmotr.html montazh.html uchastki.html; do python3 tools/patch_popscale.py $f; done
"""
import sys
path = sys.argv[1]
s = open(path, encoding='utf-8').read()
if 'POPSCALE' in s:
    print('already applied', path); sys.exit(0)
anchor = "const map=L.map('m',"
assert s.count(anchor) == 1, path
i = s.index(anchor); j = s.index(';', s.index('.setView(', i)) + 1
JS = r"""
/*POPSCALE*/var PSZ=null;{const sp=L.DomUtil.setPosition;L.DomUtil.setPosition=function(el,pt){sp.apply(this,arguments);if(!el||el._psZ0==null||!el.classList.contains('leaflet-popup'))return;
const z=PSZ==null?map.getZoom():PSZ,k=Math.min(1,Math.max(.25,Math.pow(2,z-el._psZ0)));if(k>=.999){el.style.transformOrigin='';return}
el.style.transformOrigin=(-(parseFloat(el.style.left)||0))+'px calc(100% + '+(parseFloat(el.style.bottom)||0)+'px)';el.style.transform+=' scale('+k.toFixed(4)+')'}}
map.on('zoomanim',e=>{PSZ=e.zoom});map.on('zoom zoomend',()=>{PSZ=null});
map.on('popupopen',e=>{const el=e.popup.getElement();if(el){el._psZ0=map.getZoom();el.style.transformOrigin=''}});"""
s = s[:j] + JS + s[j:]
open(path, 'w', encoding='utf-8').write(s); print('ok', path)
