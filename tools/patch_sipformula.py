# -*- coding: utf-8 -*-
"""В окне СИП-карты — блок «Как считается СИП к заказу»: формула с текущими нормами из SIPN и подстановка чисел по сети.
Применять: python3 tools/patch_sipformula.py <file.html> [...]"""
import sys
A = "h+=`<div>Опор на линии <b>${o.nodes}</b>"
B = ("{const n=SIPN,c=v=>String(v).replace('.',','),g=x=>Math.round(x).toLocaleString('ru');"
     "h+=`<div class=\"sipf\" style=\"margin:6px 0;padding:6px 8px;border:1px solid rgba(127,127,127,.4);border-radius:6px;font-size:12px;line-height:1.45\">"
     "<b>Как считается СИП к заказу</b>"
     "<div style=\"margin-top:3px\"><b>СИП отрезка</b> = (Σ пролётов + Σ провис) × ${c(1+n.res)} + петля ${c(n.loop)} м × число анкерных и угловых опор внутри отрезка + хвост ${c(n.tail)} м × 2 конца + опуск ${c(n.inlT)} м к бронекабелю (первый отрезок от ТП)</div>"
     "<div><b>Провис пролёта L</b>: стрела f = ${c(n.f40)} м × (L / 40)²; провода в пролёте = L + 8·f² / (3·L). Пример: 30 м — f ${c(sipSag(30).f.toFixed(2))} м, +${c(sipSag(30).d.toFixed(2))} м; 40 м — f ${c(sipSag(40).f.toFixed(2))} м, +${c(sipSag(40).d.toFixed(2))} м; 60 м — f ${c(sipSag(60).f.toFixed(2))} м, +${c(sipSag(60).d.toFixed(2))} м</div>"
     "<div><b>Стык</b> (отрезок длиннее барабана): + 2 хвоста + петля = ${c(2*n.tail+n.loop)} м</div>"
     "<div style=\"margin-top:3px\"><b>По сети</b>: ${g(o.nd.len)} пролёты + ${c(o.nd.sag.toFixed(1))} провис + ${g(o.nd.loops)} петли (${o.loopN} опор) + ${g(o.nd.tails)} хвосты (${2*o.pcs.length} концов) + ${g(o.nd.inl)} ввод (${o.inlN}) + ${g(o.nd.res)} запас ${Math.round(n.res*100)}%${o.cut.joints?' + '+g(o.jx)+' стыки ('+o.cut.joints+')':''} = <b>${g(o.need)} м</b></div></div>`}"
     + A)
for f in sys.argv[1:]:
    s = open(f, encoding='utf-8').read()
    if 'Как считается СИП к заказу' in s:
        print(f, 'уже применён'); continue
    n = s.count(A); s = s.replace(A, B, 1)
    open(f, 'w', encoding='utf-8').write(s); print(f, n)
