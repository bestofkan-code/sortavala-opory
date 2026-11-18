#!/usr/bin/env python3
"""Опора, у которой открыто окно, выделена на карте: яркое кольцо с пульсацией и точка-«прицел»
поверх значков (своя панель карты между значками и окнами). Исчезает при закрытии окна.
  for f in redaktor.html prosmotr.html zamechaniya.html zamechaniya-prosmotr.html montazh.html uchastki.html; do python3 tools/patch_selring.py $f; done
"""
import sys
path = sys.argv[1]
s = open(path, encoding='utf-8').read()
if 'SELRING' in s:
    print('already applied', path); sys.exit(0)
JS = r"""
/*SELRING*/{map.createPane('selPane');const sp=map.getPane('selPane');sp.style.zIndex=650;sp.style.pointerEvents='none';
 const st=document.createElement('style');st.textContent='.selr{position:relative;width:0;height:0}.selr i{position:absolute;left:-22px;top:-22px;width:44px;height:44px;border-radius:50%;border:4px solid #f59e0b;box-sizing:border-box;box-shadow:0 0 0 2px #fff,0 0 12px 3px rgba(245,158,11,.8)}.selr b{position:absolute;left:-22px;top:-22px;width:44px;height:44px;border-radius:50%;border:3px solid #f59e0b;box-sizing:border-box;animation:selp 1.3s ease-out infinite}@keyframes selp{0%{transform:scale(1);opacity:.9}100%{transform:scale(2);opacity:0}}';document.head.appendChild(st);
 let RG=null;const off=()=>{if(RG){map.removeLayer(RG);RG=null}};
 map.on('popupopen',e=>{off();const el=e.popup.getElement(),c=el&&el.querySelector('.pp[data-uid]');if(!c)return;const p=P.find(o=>o.uid==c.dataset.uid),ll=p?L.latLng(p.lat,p.lon):e.popup.getLatLng();
  RG=L.marker(ll,{pane:'selPane',interactive:false,keyboard:false,icon:L.divIcon({className:'',html:'<div class="selr"><b></b><i></i></div>',iconSize:[0,0]})}).addTo(map);RG._uid=c.dataset.uid});
 map.on('popupclose',off);
 setInterval(()=>{if(!RG)return;const p=P.find(o=>o.uid==RG._uid);if(p){const a=RG.getLatLng();if(Math.abs(a.lat-p.lat)>1e-9||Math.abs(a.lng-p.lon)>1e-9)RG.setLatLng([p.lat,p.lon])}},700)}
"""
i = s.index("const map=L.map('m',"); j = s.index(';', s.index('.setView(', i)) + 1
# P определяется позже — обращения к P только внутри обработчиков, это безопасно
s = s[:j] + JS + s[j:]
open(path, 'w', encoding='utf-8').write(s); print('ok', path)
