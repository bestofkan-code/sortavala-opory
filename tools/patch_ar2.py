# Арматура СИП на опоре, v2 (после patch_ar.py): крюк, анкерный зажим, прокол СИП–СИП (по 4) — вручную;
# промежуточный подвес — автоматически: СИП протянут на опоре и анкерного зажима нет.
import sys
fn=sys.argv[1];s=open(fn,encoding='utf-8').read()
a=s.index('/* ---- арматура СИП на опоре ---- */');b=s.index('function roPopup(p){',a)
js=r"""/* ---- арматура СИП на опоре ---- */
var ARC={t:0,m:null};
function arPlanAll(){if(ARC.m&&Date.now()-ARC.t<15000)return ARC.m;const m=new Map();try{const C=sipCalc(),ND=new Map([...C.ND.values()].map(d=>[d.p,d])),deg=new Map(),br=new Map();
 C.ED.forEach(e=>{deg.set(e.a,(deg.get(e.a)||0)+1);deg.set(e.b,(deg.get(e.b)||0)+1)});
 (C.PCS||[]).forEach(pc=>{const a=C.U.get(pc.nodes[0]);if(!a)return;const d=ND.get(a);if(d&&d.role==='branch')br.set(a,(br.get(a)||0)+1)});
 deg.forEach((k,p)=>{const d=ND.get(p)||{},b=br.get(p)||0,mm=k-b,an=d.role==='anchor'||d.role==='corner'||(d.turn||0)>=45;let a=0,s=0;
  if(mm===1)a=1;else if(mm>=2){if(an)a=2;else s=1}a+=b;m.set(p.uid,{a,s,h:a+s,pc:4*(mm>=1?b:0)})})}catch(e){}ARC={t:Date.now(),m};return m}
function arPlan(p){return arPlanAll().get(p.uid)||{a:0,s:0,h:0,pc:0}}
/* промежуточный подвес — автоматически: СИП протянут и анкерного зажима нет */
function arS(p){return wdone(p,5)&&!(+(p.ar||{}).a)?1:0}
function arV(p){const r=p.ar||{};return{h:+r.h||0,a:+r.a||0,s:arS(p),pc:+r.pc||0}}
function arTxt(p){const v=arV(p);if(!(v.h||v.a||v.s||v.pc))return '';const r=p.ar||{};return [v.h?'крюков '+v.h:'',v.a?'анкерных '+v.a:'',v.s?'подвес промежуточный':'',v.pc?'проколов СИП–СИП '+v.pc:''].filter(Boolean).join(', ')+(r.d?' · '+String(r.d).slice(8,10)+'.'+String(r.d).slice(5,7):'')}
function arBlock(box,p,onCh){const pl=arPlan(p),v=arV(p);
 if(RO){const t=arTxt(p);box.innerHTML=t?'<div class="cri">Арматура СИП: <b>'+t+'</b></div>':'';return}
 const st=(k,n,step,hint)=>`<div class="arr"><span>${n}</span><button data-ar=${k} data-d=${-step}>−</button><b>${v[k]}</b><button data-ar=${k} data-d=${step}>+</button><small>${hint||''}</small></div>`;
 const ok=v.a==pl.a&&v.h==pl.h&&v.pc==pl.pc&&(pl.a||pl.h||pl.pc);
 box.innerHTML='<div class="wh"><span>АРМАТУРА СИП НА ОПОРЕ</span>'+(pl.a||pl.h||pl.pc?'<button data-arp title="Крюки, анкерные зажимы и проколы — по расчёту СИП-карты"'+(ok?' disabled':'')+'>= по расчёту</button>':'')+'</div>'
  +st('h','Крюк',1,pl.h?'расчёт '+pl.h:'')+st('a','Анкерный зажим',1,pl.a?'расчёт '+pl.a:'')
  +`<div class="arr"><span>Подвес промежуточный</span><b class="ars${v.s?' on':''}">${v.s?'✓':'—'}</b><small>${v.s?'авто: СИП протянут':(wdone(p,5)?'нет: стоит анкерный':'ставится при «СИП»')}</small></div>`
  +st('pc','Прокол СИП–СИП',4,pl.pc?'расчёт '+pl.pc:'по 4 на ответвление');
 const set=o=>{PSEL=Date.now();const r=Object.assign({},p.ar||{},o);['h','a','pc'].forEach(k=>{r[k]=Math.max(0,+r[k]||0);if(!r[k])delete r[k]});delete r.s;
  p.ar=(r.h||r.a||r.pc)?Object.assign(r,{d:(typeof $=='function'&&$('md')&&$('md').value)||LD()}):null;arBlock(box,p,onCh);onCh()};
 box.querySelectorAll('[data-ar]').forEach(b=>b.onclick=()=>{const k=b.dataset.ar;set({[k]:v[k]+(+b.dataset.d)})});
 const bp=box.querySelector('[data-arp]');if(bp)bp.onclick=()=>set({h:pl.h,a:pl.a,pc:pl.pc})}
"""
s=s[:a]+js+s[b:]
c=".arr small{min-width:62px;opacity:.65}"
assert c in s;s=s.replace(c,c+".ars{min-width:62px;text-align:center}.ars.on{color:#4ade80}",1)
open(fn,'w',encoding='utf-8').write(s);print('ok ar2')
