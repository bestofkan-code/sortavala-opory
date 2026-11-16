# Арматура СИП на опоре (poles.ar = {a: анкерных, s: поддерживающих / промежуточный подвес, d: дата}):
# отмечает бригада на монтажной карте (и редакторы), «по расчёту» — из СИП-карты; в просмотре — строка в карточке.
import sys
fn=sys.argv[1];s=open(fn,encoding='utf-8').read()
def R(a,b,n=1):
    global s
    assert s.count(a)==n,(a[:90],s.count(a));s=s.replace(a,b)
R("ad:p.ad||'',od:p.od||null};miss.forEach","ad:p.ad||'',od:p.od||null,ar:p.ar||null};miss.forEach")
R("ad:r.ad||'',od:r.od||'',tp:r.tp,","ad:r.ad||'',od:r.od||'',ar:r.ar||null,tp:r.tp,")
R("'sx','pp','sp','od']","'sx','pp','sp','od','ar']")
R("var SF=['od','sp',","var SF=['ar','od','sp',")
js=r"""
/* ---- арматура СИП на опоре ---- */
var ARC={t:0,m:null};
function arPlanAll(){if(ARC.m&&Date.now()-ARC.t<15000)return ARC.m;const m=new Map();try{const C=sipCalc(),ND=new Map([...C.ND.values()].map(d=>[d.p,d])),deg=new Map(),br=new Map();
 C.ED.forEach(e=>{deg.set(e.a,(deg.get(e.a)||0)+1);deg.set(e.b,(deg.get(e.b)||0)+1)});
 (C.PCS||[]).forEach(pc=>{const a=C.U.get(pc.nodes[0]);if(!a)return;const d=ND.get(a);if(d&&d.role==='branch')br.set(a,(br.get(a)||0)+1)});
 deg.forEach((k,p)=>{const d=ND.get(p)||{},b=br.get(p)||0,mm=k-b,an=d.role==='anchor'||d.role==='corner'||(d.turn||0)>=45;let a=0,s=0;
  if(mm===1)a=1;else if(mm>=2){if(an)a=2;else s=1}a+=b;m.set(p.uid,{a,s})})}catch(e){}ARC={t:Date.now(),m};return m}
function arPlan(p){return arPlanAll().get(p.uid)||{a:0,s:0}}
function arTxt(p){const r=p.ar;if(!r||!(+r.a||+r.s))return '';return 'анкерных '+(+r.a||0)+', подвесов '+(+r.s||0)+(r.d?' · '+String(r.d).slice(8,10)+'.'+String(r.d).slice(5,7):'')}
function arBlock(box,p,onCh){const pl=arPlan(p),r=p.ar||{},v=k=>+r[k]||0;
 if(RO){const t=arTxt(p);box.innerHTML=t?'<div class="cri">Арматура СИП: <b>'+t+'</b></div>':'';return}
 const row=(k,n)=>`<div class="arr"><span>${n}</span><button data-ar=${k} data-d=-1>−</button><b>${v(k)}</b><button data-ar=${k} data-d=1>+</button><small>${pl[k]?'расчёт '+pl[k]:''}</small></div>`;
 const ok=v('a')==pl.a&&v('s')==pl.s&&(pl.a||pl.s);
 box.innerHTML='<div class="wh"><span>АРМАТУРА СИП НА ОПОРЕ</span>'+(pl.a||pl.s?'<button data-arp title="Поставить количество по расчёту СИП-карты"'+(ok?' disabled':'')+'>= по расчёту</button>':'')+'</div>'+row('a','Анкерный зажим')+row('s','Промежуточный подвес');
 const set=(a,s)=>{PSEL=Date.now();p.ar=(a||s)?{a,s,d:(typeof $=='function'&&$('md')&&$('md').value)||LD()}:null;arBlock(box,p,onCh);onCh()};
 box.querySelectorAll('[data-ar]').forEach(b=>b.onclick=()=>{const k=b.dataset.ar,n=Math.max(0,v(k)+(+b.dataset.d));set(k=='a'?n:v('a'),k=='s'?n:v('s'))});
 const bp=box.querySelector('[data-arp]');if(bp)bp.onclick=()=>set(pl.a,pl.s)}
"""
R("function roPopup(p){",js+"function roPopup(p){")
R("${odTxt(p)}<button data-h>","${odTxt(p)}<div data-arb></div><button data-h>")
R('<div class="phb" data-phb hidden></div><div class="phb" data-phb2 hidden></div>','<div class="phb" data-phb hidden></div><div class="phb" data-phb2 hidden></div><div class="arb" data-arb></div>')
R("const hs=()=>{d.querySelector('[data-hs]')","{const ab=d.querySelector('[data-arb]');if(ab)arBlock(ab,p,()=>{upd(p);save();stats();mark(p)})}\nconst hs=()=>{d.querySelector('[data-hs]')")
# просмотр: заполнить блок после построения карточки
a=s.index('function roPopup(p){');b=s.index('return d}',a)
s=s[:b]+"{const ab=d.querySelector('[data-arb]');if(ab)arBlock(ab,p,()=>{})}"+s[b:]
R('<style>#trd','<style>.arb{margin-top:4px}.arr{display:flex;align-items:center;gap:6px;margin:2px 0;font-size:13px}.arr span{flex:1}.arr b{min-width:18px;text-align:center}.arr button{width:30px;height:28px;padding:0}.arr small{min-width:62px;opacity:.65}[data-arp]{font-size:11px;padding:2px 6px;margin-left:6px}#trd')
open(fn,'w',encoding='utf-8').write(s);print('ok ar')
