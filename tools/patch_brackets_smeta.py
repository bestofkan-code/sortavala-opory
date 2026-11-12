#!/usr/bin/env python3
"""Кронштейны крупнее и в цвет типа + сверка со сметой и подсказки.
- На карте рожки длиннее и толще, с белой обводкой; цвет — тип: 1-рожк. тёмный, 2-рожк. 180° фиолетовый,
  2-рожк. 90° оранжевый (угол не указан — красный), как на монтажной карте. Сплошной — кронштейн установлен, пунктир — проект;
  жёлтый кружок на конце — светильник установлен. Легенда обновлена.
- Подсчёты «Проверки кронштейнов» и «Проверки котлованов» — без серых (предлагаемых) опор,
  как «Контракт и выполнение»: только опоры карты без исключённых, серых и гравитационных.
- В «Проверке кронштейнов» вверху — «Сверка со сметой»: опор 592, 1-рожк. 353, 2-рожк. 90° 50, 180° 189;
  и «Подсказки до сметы»: какой тип поставить опорам без типа и у каких опор сменить тип, чтобы выйти на смету
  (по схеме линии: развилка или угол — 90°, рядом другая линия — 180°, прямой участок — 1-рожк.;
  установленные кронштейны не трогаются). «Применить» — сменить тип (в редакторе).
Применяется к redaktor.html (один раз, после patch_main_brackets.py и patch_main_fundament.py).
"""
import sys

path = sys.argv[1]
s = open(path, encoding='utf-8').read()
if 'function kcSug(' in s:
    print('already applied')
    sys.exit(0)


def R(old, new, cnt=1):
    global s
    n = s.count(old)
    assert n == cnt, (old[:80], n)
    s = s.replace(old, new)


# 1) рожки на карте
a = s.index('function armsSVG(p,sc){')
b = s.index('return v}', a) + len('return v}')
s = s[:a] + r'''function armCol(p){const n=armN(p);return n==1?'#0f172a':+p.ka==180?'#7c3aed':+p.ka==90?'#ea580c':'#dc2626'}
function armsSVG(p,sc){sc=sc||1;const n=armN(p);if(!n)return '';const ins=wdone(p,12),sv=Math.min(2,+p.sv||0),L=23*sc,S0=6.5*sc,R=4.4*sc,col=armCol(p);let v='';
 armAng(n,+p.ka).forEach((a,i)=>{const r=a*Math.PI/180,c=Math.cos(r),sn=Math.sin(r),x=(L*c).toFixed(1),y=(L*sn).toFixed(1),x0=(S0*c).toFixed(1),y0=(S0*sn).toFixed(1);
  v+=`<line x1="${x0}" y1="${y0}" x2="${x}" y2="${y}" stroke="#fff" stroke-opacity=".9" stroke-width="${(ins?7.5:6.5)*sc}" stroke-linecap="round"/>`;
  v+=ins?`<line x1="${x0}" y1="${y0}" x2="${x}" y2="${y}" stroke="${col}" stroke-width="${4.4*sc}" stroke-linecap="round"/>`:`<line x1="${x0}" y1="${y0}" x2="${x}" y2="${y}" stroke="${col}" stroke-width="${3.4*sc}" stroke-dasharray="${4.6*sc} ${2.6*sc}"/>`;
  v+=i<sv?`<circle cx="${x}" cy="${y}" r="${R}" fill="#facc15" stroke="#854d0e" stroke-width="${1.4*sc}"/>`:`<circle cx="${x}" cy="${y}" r="${R*.8}" fill="#fff" stroke="${col}" stroke-width="${1.8*sc}"/>`});return v}''' + s[b:]

# легенда: старые значки кронштейнов → новые
a = s.index('<svg width="24" height="24" viewBox="-17 -17 34 34" style="vertical-align:middle;overflow:visible"><line x1="0.0" y1="-6.5" x2="0.0" y2="-15.0" stroke="#475569"')
b = s.index('светильник 1 из 2<br>', a) + len('светильник 1 из 2<br>')
import math


def arm_svg(angs, col, ins, sv):
    v = ''
    for i, ang in enumerate(angs):
        r = math.radians(ang); c, sn = math.cos(r), math.sin(r)
        x, y, x0, y0 = 23 * c, 23 * sn, 6.5 * c, 6.5 * sn
        v += f'<line x1="{x0:.1f}" y1="{y0:.1f}" x2="{x:.1f}" y2="{y:.1f}" stroke="#fff" stroke-opacity=".9" stroke-width="{7.5 if ins else 6.5}" stroke-linecap="round"/>'
        v += (f'<line x1="{x0:.1f}" y1="{y0:.1f}" x2="{x:.1f}" y2="{y:.1f}" stroke="{col}" stroke-width="4.4" stroke-linecap="round"/>' if ins else
              f'<line x1="{x0:.1f}" y1="{y0:.1f}" x2="{x:.1f}" y2="{y:.1f}" stroke="{col}" stroke-width="3.4" stroke-dasharray="4.6 2.6"/>')
        v += (f'<circle cx="{x:.1f}" cy="{y:.1f}" r="4.4" fill="#facc15" stroke="#854d0e" stroke-width="1.4"/>' if i < sv else
              f'<circle cx="{x:.1f}" cy="{y:.1f}" r="3.5" fill="#fff" stroke="{col}" stroke-width="1.8"/>')
    return ('<svg width="34" height="30" viewBox="-26 -27 52 40" style="vertical-align:middle;overflow:visible">' + v +
            '<circle r="6" fill="#fff" stroke="#111" stroke-width="2"/></svg>')


leg = (arm_svg([-90], '#0f172a', False, 0) + '1-рожк. &nbsp; ' +
       arm_svg([-180, 0], '#7c3aed', False, 0) + '2-рожк. 180° &nbsp; ' +
       arm_svg([-135, -45], '#ea580c', False, 0) + '2-рожк. 90°<br>' +
       arm_svg([-180, 0], '#7c3aed', True, 0) + 'сплошной — кронштейн установлен, пунктир — проект &nbsp; ' +
       arm_svg([-180, 0], '#7c3aed', True, 1) + 'жёлтый — светильник (1 из 2)<br>')
s = s[:a] + leg + s[b:]

# 2) без серых опор в проверках
R("function kcIss(p){const r=[],t=kcT(p),k12=wdone(p,12),k6=wdone(p,6),sv=+p.sv||0,kr=+p.kr||0;\n",
  "function kcIss(p){const r=[],t=kcT(p),k12=wdone(p,12),k6=wdone(p,6),sv=+p.sv||0,kr=+p.kr||0;if(p.pp)return r;\n", 1)
R("function kcData(){const C=P.filter(p=>!p.x&&!isG(p)),G=new Map();", "function kcData(){const C=P.filter(p=>!p.x&&!isG(p)&&!p.pp),G=new Map();", 1)
R("function fdData(){const C=P.filter(p=>!p.x&&!isG(p)),G=new Map();", "function fdData(){const C=P.filter(p=>!p.x&&!isG(p)&&!p.pp),G=new Map();", 1)
R("const pl=P.filter(p=>(!p.x&&!isG(p))||kcIss(p).length)", "const pl=P.filter(p=>(!p.x&&!isG(p)&&!p.pp)||kcIss(p).length)", 1)
R("const pl=P.filter(p=>(!p.x&&!isG(p))||fdIss(p).length)", "const pl=P.filter(p=>(!p.x&&!isG(p)&&!p.pp)||fdIss(p).length)", 1)
R("Опоры на гравитационном фундаменте и исключённые не считаются.", "Серые, исключённые и опоры на гравитационном фундаменте не считаются.", 1)

# 3) сверка со сметой и подсказки
R('<table id="kct"></table><div id="kcl"></div>', '<div id="kcm"></div><table id="kct"></table><div id="kcl"></div>', 1)
R('.kcg button{padding:2px 6px;font-size:11.5px;border-radius:9px}',
  '.kcg button{padding:2px 6px;font-size:11.5px;border-radius:9px}'
  '#kcm{margin:4px 0 6px;font-size:12px}#kcm table{width:100%;border-collapse:collapse;margin:3px 0}#kcm td,#kcm th{padding:2px 4px;text-align:right;border-bottom:1px solid rgba(127,127,127,.22);font-variant-numeric:tabular-nums}'
  '#kcm th{font-size:11px;font-weight:600;opacity:.85}#kcm td:first-child,#kcm th:first-child{text-align:left}#kcm .kcw{margin:4px 0;padding:4px 6px;border-radius:6px;background:rgba(245,158,11,.14);border:1px solid rgba(245,158,11,.5)}'
  '#kcm .kcs{display:flex;flex-wrap:wrap;align-items:center;gap:4px;padding:3px 0;border-bottom:1px dashed rgba(127,127,127,.25)}#kcm .kcs small{flex-basis:100%;opacity:.75}#kcm .kcs button{padding:1px 6px;font-size:11.5px}'
  '#kcm i.kd{display:inline-block;width:10px;height:10px;border-radius:2px;margin-right:3px;vertical-align:-1px}', 1)
R("$('kcl').onclick=e=>{const b=e.target.closest('[data-kc]');",
  r"""var KCT={'1':353,'90':50,'180':189},KCP=592,KCGEO=null,KCGT=0,KCC={'1':'#0f172a','90':'#ea580c','180':'#7c3aed'};
function kcGeo(){if(KCGEO&&Date.now()-KCGT<15000)return KCGEO;const N=netEdges(),E=N.E||N,lat0=61.71,kx=Math.cos(lat0*Math.PI/180)*111320,ky=110540,xy=p=>[(p.lon-30.7)*kx,(p.lat-lat0)*ky];
 const adj=new Map();E.forEach(e=>{[[e[0],e[1]],[e[1],e[0]]].forEach(([a,b])=>{if(!adj.has(a.uid))adj.set(a.uid,[]);adj.get(a.uid).push(b)})});
 const S=E.map(e=>({a:e[0].uid,b:e[1].uid,A:xy(e[0]),B:xy(e[1])})),ds=(q,g)=>{const[ax,ay]=g.A,[bx,by]=g.B,[px,py]=q,dx=bx-ax,dy=by-ay,l=dx*dx+dy*dy;let t=l?((px-ax)*dx+(py-ay)*dy)/l:0;t=Math.max(0,Math.min(1,t));return Math.hypot(px-ax-t*dx,py-ay-t*dy)};
 const F=new Map();P.filter(p=>!p.x&&!isG(p)&&!p.pp).forEach(p=>{const nb=adj.get(p.uid)||[],deg=nb.length,q=xy(p);let ang=null;
  if(deg==2){const a=xy(nb[0]),c=xy(nb[1]),v1=[a[0]-q[0],a[1]-q[1]],v2=[c[0]-q[0],c[1]-q[1]],m=Math.hypot(...v1)*Math.hypot(...v2);if(m)ang=Math.round(Math.acos(Math.max(-1,Math.min(1,(v1[0]*v2[0]+v1[1]*v2[1])/m)))*180/Math.PI)}
  const h2=new Set([p.uid]);nb.forEach(z=>{h2.add(z.uid);(adj.get(z.uid)||[]).forEach(w=>h2.add(w.uid))});let par=1e9;S.forEach(g=>{if(h2.has(g.a)||h2.has(g.b))return;const d=ds(q,g);if(d<par)par=d});
  F.set(p.uid,{deg,ang,par:Math.round(par)})});KCGEO=F;KCGT=Date.now();return F}
function kcFit(f,t){f=f||{};const a=f.ang;if(t=='90')return (f.deg>=3?2:0)+(a!=null&&a<135?1.5:0)+(a!=null&&a<100?.5:0);if(t=='180')return f.par<45?(45-f.par)/15:0;return (f.deg<=1||a==null||a>=155?1:0)+(f.par>=60?1:0)}
function kcWhy(f,t){f=f||{};if(t=='90')return f.deg>=3?'развилка линий':f.ang!=null&&f.ang<135?'угол линии '+f.ang+'°':'по схеме угла нет — проверить на месте';
 if(t=='180')return f.par<45?'рядом другая линия в '+f.par+' м — свет на обе стороны':'другой линии рядом нет — проверить, нужен ли свет с двух сторон';
 return (f.deg<=1?'конец линии':f.ang!=null&&f.ang<135?'угол линии '+f.ang+'°':'прямой участок')+(f.par>=60?', других линий рядом нет':'')}
function kcSug(){const F=kcGeo(),C=P.filter(p=>!p.x&&!isG(p)&&!p.pp),cur={'1':0,'90':0,'180':0},U=[],S=[];
 C.forEach(p=>{const t=kcT(p);if(cur[t]!=null)cur[t]++;else U.push(p)});const c0={...cur},T=Object.keys(KCT);
 U.forEach(p=>{const f=F.get(p.uid),pr=T.slice().sort((a,b)=>kcFit(f,b)-kcFit(f,a)),t=pr.find(x=>cur[x]<KCT[x])||pr[0];cur[t]++;S.push({p,from:kcT(p),to:t,why:kcWhy(f,t)})});
 const used=new Set(S.map(x=>x.p.uid));let g=0;
 while(g++<300){const ov=T.filter(t=>cur[t]>KCT[t]),un=T.filter(t=>cur[t]<KCT[t]);if(!ov.length||!un.length)break;let best=null;
  C.forEach(p=>{const x=kcT(p);if(!ov.includes(x)||used.has(p.uid)||wdone(p,12))return;const f=F.get(p.uid);un.forEach(y=>{const d=kcFit(f,y)-kcFit(f,x);if(!best||d>best.d)best={p,x,y,d,f}})});
  if(!best)break;used.add(best.p.uid);cur[best.x]--;cur[best.y]++;S.push({p:best.p,from:best.x,to:best.y,why:kcWhy(best.f,best.y)})}
 return{S,c0,cur,n:C.length,u:U.length}}
function kcSm(){const e=$('kcm');if(!e)return;const r=kcSug(),dl=v=>v==0?'<td class="ok">✓</td>':`<td class="bad">${v>0?'+':''}${v}</td>`,nm={'1':'1-рожк.','90':'2-рожк. 90°','180':'2-рожк. 180°','?':'без типа','2?':'2-рожк. без угла'};
 let h='<b>Сверка со сметой</b><table><tr><th></th><th>На карте</th><th>Смета</th><th>±</th>'+(r.S.length?'<th title="если применить подсказки">после</th>':'')+'</tr>'+
  `<tr><td>Опоры</td><td>${r.n}</td><td>${KCP}</td>${dl(r.n-KCP)}${r.S.length?'<td>'+r.n+'</td>':''}</tr>`+
  Object.keys(KCT).map(t=>`<tr><td><i class="kd" style="background:${KCC[t]}"></i>${nm[t]}</td><td>${r.c0[t]}</td><td>${KCT[t]}</td>${dl(r.c0[t]-KCT[t])}${r.S.length?`<td class="${r.cur[t]==KCT[t]?'ok':'bad'}">${r.cur[t]}</td>`:''}</tr>`).join('')+
  (r.u?`<tr><td>Тип не указан</td><td class="bad">${r.u}</td><td>0</td>${dl(r.u)}${r.S.length?'<td class="ok">0</td>':''}</tr>`:'')+'</table>';
 if(r.n!=KCP)h+=`<div class="kcw">${r.n<KCP?`На карте на <b>${KCP-r.n}</b> опор меньше контракта (592). Типы кронштейнов не выйдут на смету, пока не добавлены опоры — не хватит ${KCP-r.n} кронштейнов того типа, что останется в минусе.`:`На карте на <b>${r.n-KCP}</b> опор больше контракта (592) — лишние опоры надо исключить или сделать серыми.`}</div>`;
 if(r.S.length){h+=`<b style="display:block;margin-top:6px">Подсказки до сметы — ${r.S.length}</b><small style="display:block;opacity:.75">По схеме линии: развилка или угол — 90°, рядом другая линия — 180°, прямой участок — 1-рожк. Установленные кронштейны не трогаются. Проверьте на месте или по спутнику.</small>`+
  r.S.map(x=>`<div class="kcs"><button data-kc="${esc(x.p.uid)}">${esc(x.p.id)}</button><span>${nm[x.from]||x.from} → <b style="color:${KCC[x.to]}">${nm[x.to]}</b></span>${RO?'':`<button data-kca="${esc(x.p.uid)}" data-to="${x.to}" title="Сменить тип кронштейна на опоре">Применить</button>`}<small>${esc(x.why)}</small></div>`).join('')}
 else if(r.n==KCP)h+='<div class="ok" style="margin:4px 0"><b>Типы кронштейнов совпадают со сметой ✓</b></div>';
 e.innerHTML=h}
{const _ku=kcUI;kcUI=function(){_ku.apply(this,arguments);try{if($('kcd').open)kcSm()}catch(er){console.warn('kcSm',er)}}}
$('kcd').addEventListener('toggle',()=>{if($('kcd').open){KCGEO=null;try{kcSm()}catch(er){}}});
$('kcm').onclick=e=>{const a=e.target.closest('[data-kca]');if(a){if(RO)return;const p=P.find(o=>o.uid==a.dataset.kca);if(!p)return;const t=a.dataset.to;if(wdone(p,12)&&!confirm('Кронштейн на '+p.id+' уже отмечен установленным. Всё равно сменить тип?'))return;
  p.kr=t=='1'?1:2;p.ka=t=='1'?null:+t;upd(p);save();stats();mark(p);toast(p.id+': кронштейн — '+(t=='1'?'1-рожковый':'2-рожковый '+t+'°'));return}
 const b=e.target.closest('[data-kc]');if(!b)return;const p=P.find(o=>o.uid==b.dataset.kc);if(!p)return;map.setView([p.lat,p.lon],Math.max(map.getZoom(),19));const m=mk.get(p);if(m&&lg.hasLayer(m))L.popup(PO()).setLatLng(m.getLatLng()).setContent(popup(p)).openOn(map);else toast('Опора скрыта фильтром')};
$('kcl').onclick=e=>{const b=e.target.closest('[data-kc]');""", 1)

open(path, 'w', encoding='utf-8').write(s)
print('ok', path)
