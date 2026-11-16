# Арматура v3 (после patch_ar2.py): подвес промежуточный — авто по «СИП», но можно поставить вручную (ar.s), кнопка «авто» возвращает расчёт.
import sys
fn=sys.argv[1];s=open(fn,encoding='utf-8').read()
def R(a,b):
    global s
    assert s.count(a)==1,(a[:90],s.count(a));s=s.replace(a,b)
R("function arS(p){return wdone(p,5)&&!(+(p.ar||{}).a)?1:0}",
  "function arSA(p){return wdone(p,5)&&!(+(p.ar||{}).a)?1:0}\nfunction arS(p){const r=p.ar||{};return ('s' in r)?Math.max(0,+r.s||0):arSA(p)}")
R("+`<div class=\"arr\"><span>Подвес промежуточный</span><b class=\"ars${v.s?' on':''}\">${v.s?'✓':'—'}</b><small>${v.s?'авто: СИП протянут':(wdone(p,5)?'нет: стоит анкерный':'ставится при «СИП»')}</small></div>`",
  "+(()=>{const man='s' in (p.ar||{});return `<div class=\"arr\"><span>Подвес промежуточный</span><button data-ar=s data-d=-1>−</button><b class=\"ars${v.s?' on':''}\">${v.s}</b><button data-ar=s data-d=1>+</button><small>${man?'<a href=\"#\" data-ara title=\"Вернуть автоматически\">вручную · авто</a>':(v.s?'авто: СИП протянут':(wdone(p,5)?'авто: стоит анкерный':'авто при «СИП»'))}</small></div>`})()")
R("['h','a','pc'].forEach(k=>{r[k]=Math.max(0,+r[k]||0);if(!r[k])delete r[k]});delete r.s;\n  p.ar=(r.h||r.a||r.pc)?",
  "['h','a','pc'].forEach(k=>{r[k]=Math.max(0,+r[k]||0);if(!r[k])delete r[k]});if('s' in o){if(o.s===null)delete r.s;else r.s=Math.max(0,+o.s||0)}\n  p.ar=(r.h||r.a||r.pc||('s' in r))?")
R("const bp=box.querySelector('[data-arp]');if(bp)bp.onclick=()=>set({h:pl.h,a:pl.a,pc:pl.pc})}",
  "const bp=box.querySelector('[data-arp]');if(bp)bp.onclick=()=>set({h:pl.h,a:pl.a,pc:pl.pc});const aa=box.querySelector('[data-ara]');if(aa)aa.onclick=e=>{e.preventDefault();set({s:null})}}")
R(".ars{min-width:62px;text-align:center}",".ars{min-width:18px;text-align:center}")
open(fn,'w',encoding='utf-8').write(s);print('ok ar3')
