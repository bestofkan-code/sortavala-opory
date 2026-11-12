#!/usr/bin/env python3
"""Новые опоры и смена типа кронштейна — с учётом сверки со сметой (после patch_brackets_smeta.py).
- Новая опора (режим «Добавить») сразу получает тип кронштейна, который ещё остался по смете:
  сначала 1-рожк., потом 180°, потом 90°; всплывает подсказка, что осталось по смете.
  Если на карте уже 592 опоры — предупреждение, что опора сверх контракта.
- Смена типа кронштейна в карточке и возврат опоры из исключённых: если тип выходит за смету — предупреждение.
Применяется к redaktor.html (один раз): python3 tools/patch_kc_add.py redaktor.html
"""
import sys
path = sys.argv[1]
s = open(path, encoding='utf-8').read()
if 'function kcPick(' in s:
    print('already applied'); sys.exit(0)
def R(old, new, cnt=1):
    global s
    n = s.count(old); assert n == cnt, (old[:80], n); s = s.replace(old, new)
R("function addAt(la,lo){",
  "function kcCnt(){const c={'1':0,'90':0,'180':0,n:0};P.forEach(p=>{if(p.x||isG(p)||p.pp)return;c.n++;const t=kcT(p);if(c[t]!=null)c[t]++});return c}\n"
  "function kcLeftTxt(c){c=c||kcCnt();const L=['1','180','90'].map(t=>[t,KCT[t]-c[t]]),nm={'1':'1-рожк.','90':'90°','180':'180°'};return 'по смете осталось: '+L.map(([t,k])=>nm[t]+' '+k).join(', ')+' · опор '+c.n+' из '+KCP}\n"
  "function kcPick(){const c=kcCnt();return ['1','180','90'].find(t=>KCT[t]-c[t]>0)||null}\n"
  "function kcOver(p){if(!p||p.x||isG(p)||p.pp)return;const c=kcCnt(),t=kcT(p),o=[];if(KCT[t]!=null&&c[t]>KCT[t])o.push(({'1':'однорожковых','90':'двухрожковых 90°','180':'двухрожковых 180°'})[t]+' '+c[t]+' при '+KCT[t]+' по смете');if(c.n>KCP)o.push('опор '+c.n+' при '+KCP+' по контракту');"
  "if(o.length)toast('⚠ '+p.id+': сверх сметы — '+o.join('; ')+'. '+kcLeftTxt(c))}\n"
  "function addAt(la,lo){")
R("const p={uid:'n'+Date.now()+Math.random().toString(36).slice(2,6),id:tp?pid(tp,n):'Н-'+(P.length+1),lat:la,lon:lo,t:$('nt').value,h:+$('nh').value||8,g:false,tp,n:tp?n:'',line:q?q.line:'',done:false,date:'',note:''};P.push(p);add(p);save();stats();mark(p)}",
  "const c0=kcCnt(),tk=kcPick(),p={uid:'n'+Date.now()+Math.random().toString(36).slice(2,6),id:tp?pid(tp,n):'Н-'+(P.length+1),lat:la,lon:lo,t:$('nt').value,h:+$('nh').value||8,g:false,tp,n:tp?n:'',line:q?q.line:'',done:false,date:'',note:''};"
  "if(tk){p.kr=tk=='1'?1:2;p.ka=tk=='1'?null:+tk}P.push(p);add(p);save();stats();mark(p);"
  "if(c0.n>=KCP)toast('⚠ '+p.id+': на карте уже '+c0.n+' опор — эта сверх контракта ('+KCP+'). Сделайте её серой или исключите лишнюю.');"
  "else toast(p.id+': кронштейн '+(tk=='1'?'1-рожковый':tk?'2-рожковый '+tk+'°':'не задан — по смете типов не осталось')+' · '+kcLeftTxt())}")
R("d.querySelector('[data-kr]').onchange=e=>{PSEL=Date.now();const[a,b]=e.target.value.split('-');p.kr=+a;p.ka=b?+b:null;krSel();ch()};",
  "d.querySelector('[data-kr]').onchange=e=>{PSEL=Date.now();const[a,b]=e.target.value.split('-');p.kr=+a;p.ka=b?+b:null;krSel();ch();try{kcOver(p)}catch(er){}};")
R("else if(mode=='excl'){p.x=!p.x;upd(p);save();stats();mark(p)}",
  "else if(mode=='excl'){p.x=!p.x;upd(p);save();stats();mark(p);if(!p.x)try{kcOver(p)}catch(er){}}")
open(path, 'w', encoding='utf-8').write(s); print('ok', path)
