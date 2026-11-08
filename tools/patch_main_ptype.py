#!/usr/bin/env python3
"""Фильтр «Опоры»: стандартные / анкерные и 8 м / 9 м (вместо выпадающего списка высоты).
Внутри группы — «или», между группами — «и» (например, анкерные + 9 м = анкерные 9 м).
Применяется к redaktor.html (один раз): python3 tools/patch_main_ptype.py redaktor.html
"""
import sys

path = sys.argv[1]
s = open(path, encoding='utf-8').read()
if 'id="fty"' in s:
    print('already applied')
    sys.exit(0)


def R(old, new, cnt=1):
    global s
    n = s.count(old)
    assert n == cnt, (old[:90], n)
    s = s.replace(old, new)


# 1) разметка: убираем список высоты, добавляем строку фильтра «Опоры»
R('<select id="fh" title="Высота опор"><option value="">любая высота</option><option value="8">8 м</option><option value="9">9 м</option></select></div>',
  '</div><div class="r" id="fty"><span>Опоры:</span>'
  '<label class="wfc"><input type="checkbox" data-t="S"> стандартные <small></small></label>'
  '<label class="wfc"><input type="checkbox" data-t="A"> анкерные <small></small></label>'
  '<label class="wfc"><input type="checkbox" data-h="8"> 8 м <small></small></label>'
  '<label class="wfc"><input type="checkbox" data-h="9"> 9 м <small></small></label>'
  '<button id="ftyx" hidden>Все</button></div>')

# 2) стили — как у фильтра по работам
R('#wf .wfc{border:1px solid #bbb;border-radius:10px;padding:1px 7px;background:#fff;cursor:pointer}',
  '#wf .wfc,#fty .wfc{border:1px solid #bbb;border-radius:10px;padding:1px 7px;background:#fff;cursor:pointer}'
  '#fty .wfc small{opacity:.7}#fty #ftyx{padding:1px 8px;font-size:12px}')
R('#wf .wfc:has(input:checked){background:#dbeafe;border-color:#2563eb}',
  '#wf .wfc:has(input:checked),#fty .wfc:has(input:checked){background:#dbeafe;border-color:#2563eb}')
R('.dk #wf .wfc{background:#1d2230;border-color:#2c3346;color:#e6e9f2;padding:3px 9px}',
  '.dk #wf .wfc,.dk #fty .wfc{background:#1d2230;border-color:#2c3346;color:#e6e9f2;padding:3px 9px}')
R('.dk #wf .wfc:has(input:checked){background:#24325c;border-color:#4f7cff;color:#fff}',
  '.dk #wf .wfc:has(input:checked),.dk #fty .wfc:has(input:checked){background:#24325c;border-color:#4f7cff;color:#fff}')

# 3) видимость опор
R("function vis(p){return tpOk(p)&&sqVis(p)&&!(HG&&isG(p))&&(!FJ||!!p.js)&&(!$('fh').value||String(+p.h||8)==$('fh').value)&&wmatch(p)",
  "function vis(p){return ftyOk(p)&&visB(p)}function visB(p){return tpOk(p)&&sqVis(p)&&!(HG&&isG(p))&&(!FJ||!!p.js)&&wmatch(p)")
R("['fd','fr','fx','fh'].forEach(i=>$(i).onchange=()=>{P.forEach(upd);numLabels()});",
  "['fd','fr','fx'].forEach(i=>$(i).onchange=()=>{P.forEach(upd);numLabels()});")

# 4) пересчёт счётчиков вместе со статистикой
R('try{skUI()}catch(e){}', 'try{skUI()}catch(e){}try{ftyUI()}catch(e){}')

# 5) код фильтра
R('/* ---- склад закладных: привезено − установлено по карте ---- */',
  r'''/* ---- фильтр «Опоры»: стандартные/анкерные, 8/9 м ---- */
var FTYT=new Set(),FTYH=new Set();
try{const v=JSON.parse(localStorage.getItem(KEY+'_fty')||'{}');(v.t||[]).forEach(x=>FTYT.add(x));(v.h||[]).forEach(x=>FTYH.add(+x))}catch(e){}
function ftyT(p){return p.t=='A'?'A':'S'}function ftyH(p){return +p.h==9?9:8}
function ftyOk(p){return (!FTYT.size||FTYT.has(ftyT(p)))&&(!FTYH.size||FTYH.has(ftyH(p)))}
function ftyTxt(){const a=[];if(FTYT.size)a.push([...FTYT].map(x=>x=='A'?'анкерные':'стандартные').join(' и '));if(FTYH.size)a.push([...FTYH].sort().map(x=>x+' м').join(' и '));return a.join(', ')}
function ftyReset(){FTYT.clear();FTYH.clear();ftySave();ftyUI()}
function ftySave(){try{localStorage.setItem(KEY+'_fty',JSON.stringify({t:[...FTYT],h:[...FTYH]}))}catch(e){}}
function ftyUI(){const B=P.filter(visB);document.querySelectorAll('#fty input').forEach(i=>{const t=i.dataset.t,h=+i.dataset.h;
i.checked=t?FTYT.has(t):FTYH.has(h);
const n=t?B.filter(p=>ftyT(p)==t&&(!FTYH.size||FTYH.has(ftyH(p)))).length:B.filter(p=>ftyH(p)==h&&(!FTYT.size||FTYT.has(ftyT(p)))).length;
i.parentNode.querySelector('small').textContent=n});$('ftyx').hidden=!(FTYT.size||FTYH.size)}
document.querySelectorAll('#fty input').forEach(i=>i.onchange=()=>{const t=i.dataset.t,h=+i.dataset.h,S=t?FTYT:FTYH,v=t||h;if(i.checked)S.add(v);else S.delete(v);ftySave();ftyUI();P.forEach(upd);numLabels()});
$('ftyx').onclick=()=>{ftyReset();P.forEach(upd);numLabels()};
/* ---- склад закладных: привезено − установлено по карте ---- */''')

open(path, 'w', encoding='utf-8').write(s)
print('ok')
