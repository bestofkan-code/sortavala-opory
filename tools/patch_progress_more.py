#!/usr/bin/env python3
"""«Ход работ»: к закладным, бетону и опорам добавлены
  • светильники установлено — из 831 по смете (на опоре: число светильников из карточки, иначе по числу рожков);
  • кронштейны по типам — 1-рожковые из 353, 2-рожковые 90° из 50, 2-рожковые 180° из 189;
  • СИП протянут ≈ м — сумма пролётов, где на обеих опорах отмечен СИП, из 16 664 м по смете.
Серые, исключённые и опоры на гравитационном фундаменте не считаются.
Применяется к redaktor.html (один раз): python3 tools/patch_progress_more.py redaktor.html
"""
import sys
path = sys.argv[1]
s = open(path, encoding='utf-8').read()
if 'function hwMore(' in s:
    print('already applied'); sys.exit(0)
def R(old, new, cnt=1):
    global s
    n = s.count(old); assert n == cnt, (old[:80], n); s = s.replace(old, new)

FN = r"""function hwMore(A){const B=A.filter(p=>!p.pp),bar=(v,T,c)=>`<div style="height:6px;background:#e5e7eb;border-radius:3px;overflow:hidden;margin:2px 0 5px"><i style="display:block;height:100%;width:${T?Math.min(100,v/T*100):0}%;background:${c}"></i></div>`,
 ln=(nm,v,T,c,u)=>`<div style="display:flex;justify-content:space-between;gap:6px"><span>${nm}</span><b style="color:${c}">${u?'≈ ':''}${v.toLocaleString('ru-RU')}${u||''} из ${T.toLocaleString('ru-RU')}${u||''} <small style="color:#555;font-weight:400">(${T?Math.round(v/T*1000)/10:0}%) · осталось ${u?'≈ ':''}${Math.max(0,T-v).toLocaleString('ru-RU')}${u||''}</small></b></div>`+bar(v,T,c),
 sv=B.reduce((a,p)=>a+(wdone(p,6)?(+p.sv||Math.max(1,+p.kr||1)):0),0),kc=t=>B.filter(p=>wdone(p,12)&&kcT(p)==t).length;
 let sip='';try{const C=sipCalc(),ok=p=>!p.x&&wdone(p,5);let L=0,n=0;C.ED.forEach(x=>{if(ok(x.a)&&ok(x.b)){L+=x.len;n++}});L=Math.round(L/10)*10;
  sip=ln('СИП протянут',L,16664,'#b45309',' м').replace('</span>',` <small style="color:#555">(${n} ${n%10==1&&n%100!=11?'пролёт':n%10>=2&&n%10<=4&&(n%100<12||n%100>14)?'пролёта':'пролётов'})</small></span>`)}catch(e){}
 return ln('Светильников установлено',sv,831,'#ca8a04')
  +'<div style="margin:3px 0 1px;color:#555">Кронштейны установлено:</div>'
  +ln('1-рожковые',kc('1'),353,'#0f172a')+ln('2-рожковые 90°',kc('90'),50,'#ea580c')+ln('2-рожковые 180°',kc('180'),189,'#7c3aed')
  +sip+'<small style="color:#555;display:block;margin:-2px 0 4px">Светильники, кронштейны и СИП — из сметы (831 шт., 353/50/189 шт., 16 664 м). СИП — приблизительно, по длинам пролётов на карте, где на обеих опорах отмечен СИП.</small>'}
function stats(){"""
R("function stats(){", FN)
R("ln('Опор установлено',o,'#15803d')+", "ln('Опор установлено',o,'#15803d')+(()=>{try{return hwMore(A)}catch(e){return ''}})()+")
R(".dk #st b[style*='color:#854d0e']{color:#fde047!important}",
  ".dk #st b[style*='color:#854d0e']{color:#fde047!important}\n"
  ".dk #st b[style*='color:#0f172a']{color:#e2e8f0!important}.dk #st i[style*='background:#0f172a']{background:#cbd5e1!important}\n"
  ".dk #st b[style*='color:#7c3aed']{color:#c4b5fd!important}.dk #st i[style*='background:#7c3aed']{background:#a78bfa!important}\n"
  ".dk #st b[style*='color:#b45309']{color:#fbbf24!important}.dk #st i[style*='background:#b45309']{background:#f59e0b!important}\n"
  ".dk #st b[style*='color:#ca8a04']{color:#fde047!important}.dk #st b[style*='color:#ea580c']{color:#fdba74!important}")
open(path, 'w', encoding='utf-8').write(s); print('ok', path)
