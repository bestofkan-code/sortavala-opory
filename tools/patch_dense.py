#!/usr/bin/env python3
"""Окно опоры плотнее: шрифт меньше, плитки работ ниже, промежутки меньше. Только CSS, состав окна прежний.
  for f in redaktor.html prosmotr.html zamechaniya.html zamechaniya-prosmotr.html montazh.html uchastki.html; do python3 tools/patch_dense.py $f; done
"""
import sys
path = sys.argv[1]
s = open(path, encoding='utf-8').read()
if 'DENSE' in s:
    print('already applied', path); sys.exit(0)
CSS = (
 ".leaflet-popup .leaflet-popup-content{margin:5px 7px!important;font-size:11px!important;line-height:1.2!important}"
 ".leaflet-popup .pp.cw{width:372px!important}.leaflet-popup .pp.fix{width:268px}"
 ".leaflet-popup .pp b{font-size:12px}.leaflet-popup .pp small{font-size:10px}.leaflet-popup .pp .adr{font-size:11px;margin:0}"
 ".leaflet-popup .pp .pph{padding-bottom:1px!important}"
 ".leaflet-popup .pp .yco{font-size:10px!important;margin:1px 0 2px!important;gap:4px!important}.leaflet-popup .pp .yco button{font-size:10px!important;height:18px!important;padding:0 5px!important;margin:0!important}.leaflet-popup .pp .yco a{font-size:10px!important}"
 ".leaflet-popup .pp .g3p{gap:1px 3px!important;margin:2px 0!important}.leaflet-popup .pp .g3p label{font-size:9.5px!important;line-height:1.1!important}"
 ".leaflet-popup .pp select,.leaflet-popup .pp input[type=text],.leaflet-popup .pp input[type=date]{height:21px!important;font-size:11px!important;padding:0 4px!important;margin:0!important}"
 ".leaflet-popup .pp .ck2{gap:0 10px!important;font-size:11px!important;margin:1px 0 0!important}.leaflet-popup .pp .ck2 label,.leaflet-popup .pp .ck label{line-height:18px!important;font-size:11px}"
 ".leaflet-popup .pp input[type=checkbox]{width:13px!important;height:13px!important;margin:0 3px 0 0!important;vertical-align:-2px!important}"
 ".leaflet-popup .pp .wh{font-size:9.5px!important;margin:3px 0 1px!important}.leaflet-popup .pp .wh span:last-child{display:none}"
 ".leaflet-popup .pp .wg{gap:2px!important}"
 ".leaflet-popup .pp .wt,.leaflet-popup .pp .wt button{height:21px!important}.leaflet-popup .pp .wt{border-radius:6px!important}"
 ".leaflet-popup .pp .wt button{font-size:10.5px!important}.leaflet-popup .pp .wt .wn{gap:3px!important;padding:0 2px 0 4px!important}"
 ".leaflet-popup .pp .wt .wn i{width:12px!important;height:12px!important;font-size:9px!important;border-radius:3px!important}"
 ".leaflet-popup .pp .wt .wdt{font-size:9.5px!important;padding:0 4px 0 1px!important}.leaflet-popup .pp .wt .wph{font-size:9.5px!important;padding:0 3px!important}"
 ".leaflet-popup .pp .g2i{gap:3px!important;margin-top:3px!important}"
 ".leaflet-popup .pp .brow{gap:3px!important;margin-top:3px!important}.leaflet-popup .pp .brow button{height:22px!important;font-size:11px!important;padding:0 6px!important;margin:0!important}"
 ".leaflet-popup .pp .more button{height:22px;font-size:11px;margin:3px 0 0!important}"
 ".leaflet-popup .pp .vfb{padding:3px 6px!important;margin:3px 0!important;font-size:11px!important}.leaflet-popup .pp .vft{margin-bottom:1px!important;font-size:11px}"
 ".leaflet-popup .pp .vfc{font-size:11px!important;padding:1px 0!important}.leaflet-popup .pp .vfc input{width:14px!important;height:14px!important}"
 ".leaflet-popup .pp .vfr{gap:3px!important;margin:2px 0!important}.leaflet-popup .pp .vfr label{font-size:9.5px!important}.leaflet-popup .pp .vfr button{height:22px!important;padding:0 7px!important;font-size:11px!important;margin:0!important}"
 ".leaflet-popup .pp .vfb small{font-size:10px!important;margin-top:1px!important}"
 ".leaflet-popup .pp .hin{font-size:10.5px!important;padding:2px 5px!important;margin-top:3px!important}.leaflet-popup .pp .hin .hir{padding:2px 0!important}.leaflet-popup .pp .hin .hfull{height:22px!important}"
 ".leaflet-popup .pp .phb{margin:2px 0!important}"
)
JS = "\n/*DENSE*/{const st=document.createElement('style');st.textContent=" + repr(CSS) + ";(document.body||document.head).appendChild(st)}\n"
i = s.index("const map=L.map('m',"); j = s.index(';', s.index('.setView(', i)) + 1
s = s[:j] + JS + s[j:]
open(path, 'w', encoding='utf-8').write(s); print('ok', path)
