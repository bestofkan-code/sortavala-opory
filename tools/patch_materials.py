#!/usr/bin/env python3
"""Блок «Материалы на складе»: поставки из таблицы materials_in (Supabase) и расход по карте.
  Пришло — сумма поставок по коду (упаковки пересчитываются в штуки).
  Ушло — расход по нормам на уже смонтированное (опоры с отметкой «Протянут СИП» и «Установлен светильник»):
    анкерные/поддерживающие зажимы, колпачки, проколы СИП–СИП, перемычка PEN (НКИ, ПуГВ 1×6, болт, шайбы), ремешки.
  Остаток = пришло − ушло. Цены видят только редакторы (не бригада): RLS mi_read.
Применяется к redaktor.html (один раз): python3 tools/patch_materials.py redaktor.html
"""
import sys
path = sys.argv[1]
s = open(path, encoding='utf-8').read()
if 'function matUI(' in s:
    print('already applied'); sys.exit(0)
def R(old, new, cnt=1):
    global s
    n = s.count(old); assert n == cnt, (old[:80], n); s = s.replace(old, new)

JS = r"""
<style>#matd table{width:100%;border-collapse:collapse;font-size:12px}#matd td,#matd th{padding:2px 4px;border-bottom:1px solid #e5e7eb;text-align:right}#matd td:first-child,#matd th:first-child{text-align:left}
#matd .neg{color:#dc2626;font-weight:700}#matd .dc{font-size:11px;color:#555;margin:4px 0}.dk #matd td,.dk #matd th{border-color:#334155}.dk #matd .dc{color:#94a3b8}</style>
<script>
var MATI=[],MATK={anc:'анкерные зажимы на смонтированном СИП',sus:'поддерживающие зажимы',cap:'по 4 на каждый конец СИП',ct70:'по 4 на ответвление',nki:'1 на перемычку PEN',pugv:'перемычка PEN',grover:'1 на перемычку',washer:'1 на перемычку',bolt:'1 на перемычку',strap:'2 у поддерживающего, по 1 у анкерного и каждого прокола',zoi:'3 на светильник'};
async function matPull(){if(!CF||RO)return;try{const r=await fetch(CF.u+'/rest/v1/materials_in?select=*&order=doc_date.asc,id.asc',{headers:H()}),j=await r.json();if(Array.isArray(j)){MATI=j;matUI()}}catch(e){}}
function matUse(){const C=sipCalc(),E=C.ED.filter(e=>wdone(e.a,5)&&wdone(e.b,5)),deg=new Map(),inst=new Set(),ND=new Map([...C.ND.values()].map(d=>[d.p,d])),br=new Map();
 E.forEach(e=>{deg.set(e.a,(deg.get(e.a)||0)+1);deg.set(e.b,(deg.get(e.b)||0)+1);inst.add(e.a.uid+'|'+e.b.uid);inst.add(e.b.uid+'|'+e.a.uid)});
 (C.PCS||[]).forEach(pc=>{const a=C.U.get(pc.nodes[0]),b=C.U.get(pc.nodes[1]);if(!a||!b)return;const d=ND.get(a);if(d&&d.role==='branch'&&inst.has(a.uid+'|'+b.uid))br.set(a,(br.get(a)||0)+1)});
 const o={anc:0,sus:0,cap:0,ct70:0,bond:0,zoi:0,len:0,span:E.length};
 deg.forEach((k,p)=>{const d=ND.get(p)||{},b=br.get(p)||0,m=k-b,an=d.role==='anchor'||d.role==='corner'||(d.turn||0)>=45;
  if(m===1){o.anc++;if(!d.root)o.cap+=4}else if(m>=2){if(an)o.anc+=2;else o.sus++}
  if(b){o.anc+=b;if(m>=1)o.ct70+=4*b;else o.cap+=4*b}
  o.bond++;if(wdone(p,6))o.zoi+=3*(+p.sv||Math.max(1,+p.kr||1))});
 E.forEach(e=>o.len+=e.len);
 o.strap=o.sus*2+o.anc+o.zoi+o.bond+o.ct70;o.nki=o.grover=o.washer=o.bolt=o.bond;o.pugv=Math.round(o.bond*SIPN.pen*10)/10;return o}
function matUI(){let d=$('matd');if(!d){const sk=$('skd');if(!sk||RO)return;sk.insertAdjacentHTML('afterend','<details id="matd" open><summary><b>Материалы на складе</b> <span id="mats"></span></summary><div id="matw"></div></details>');d=$('matd')}
 if(!MATI.length){d.style.display='none';return}d.style.display='';
 let U={};try{U=matUse()}catch(e){}
 const G=new Map(),f=v=>(Math.round(v*10)/10).toLocaleString('ru-RU'),un=u=>u=='упак'?'шт':u;
 MATI.forEach(r=>{const k=r.code||r.name,g=G.get(k)||{name:r.name,unit:un(r.unit),q:0,key:r.mkey,docs:new Set()};g.q+=(+r.qty||0)*(+r.per||1);g.docs.add(r.doc);G.set(k,g)});
 let h='<table><tr><th>Позиция</th><th>Пришло</th><th>Ушло</th><th>Остаток</th></tr>',neg=0;
 [...G.values()].forEach(g=>{const u=g.key&&U[g.key]!=null?U[g.key]:null,rest=u==null?null:g.q-u;if(rest!=null&&rest<0)neg++;
  h+=`<tr><td>${esc(g.name)}</td><td>${f(g.q)} ${esc(g.unit)}</td><td title="${esc(MATK[g.key]||'расход по карте не считается')}">${u==null?'—':f(u)}</td><td class="${rest!=null&&rest<0?'neg':''}">${rest==null?'—':f(rest)}</td></tr>`});
 h+='</table>';
 const D=new Map();MATI.forEach(r=>{const x=D.get(r.doc)||{date:r.doc_date,sup:r.supplier,n:0,sum:0,st:r.status};x.n++;x.sum+=+r.sum_nds||0;D.set(r.doc,x)});
 h+='<div class="dc"><b>Поставки:</b><br>'+[...D.entries()].map(([k,x])=>`${esc(k)}${x.date?' от '+x.date.split('-').reverse().join('.'):''} · ${x.n} поз. · ${x.sum.toLocaleString('ru-RU',{minimumFractionDigits:2,maximumFractionDigits:2})} ₽ с НДС${x.st?' · '+esc(x.st):''}`).join('<br>')+'</div>';
 h+=`<div class="dc">«Ушло» — расход по нормам на уже смонтированное по отметкам карты: СИП протянут на ${U.bond||0} опорах (${U.span||0} ${(n=>n%10==1&&n%100!=11?'пролёт':n%10>=2&&n%10<=4&&(n%100<12||n%100>14)?'пролёта':'пролётов')(U.span||0)}, ≈ ${f(U.len||0)} м), проколов ЗОИ на светильники — ${U.zoi||0}. «—» — для позиции норма расхода по карте не задана. Учёт поставок начат 13.11.2026; более ранние поставки не внесены, поэтому остаток верен, только если этих позиций до учёта на складе не было.</div>`;
 $('matw').innerHTML=h;$('mats').textContent=neg?' · не хватает: '+neg:''}
setTimeout(matPull,3000);setInterval(matPull,120000);
</script>
"""
anchor = '</script></body></html>'
i = s.rfind(anchor); assert i > 0
s = s[:i + len('</script>')] + JS + s[i + len('</script>'):]
R("try{kcUI()}catch(e){}", "try{kcUI()}catch(e){}try{matUI()}catch(e){}")
open(path, 'w', encoding='utf-8').write(s); print('ok', path)
