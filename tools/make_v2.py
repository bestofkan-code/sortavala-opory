#!/usr/bin/env python3
"""Builds the test version of the map with the new panel (redaktor2.html / prosmotr2.html)
from the current redaktor.html. Run from the repository root:  python3 tools/make_v2.py
"""
import re

SRC = 'redaktor.html'
s = open(SRC, encoding='utf-8').read()


def rep(old, new, count=1):
    global s
    n = s.count(old)
    if n != count:
        raise SystemExit(f'anchor found {n} times, expected {count}: {old[:90]!r}')
    s = s.replace(old, new)


def cut(start, end):
    """Return the markup between two anchors (start included, end excluded)."""
    i = s.index(start)
    j = s.index(end, i)
    return s[i:j]


# ---------------------------------------------------------------- sidebar: pull existing blocks out by their markup
side_start = s.index('<div id="s">')
side_end = s.index('<div id="m"></div>')
side = s[side_start:side_end]


def piece(a, b):
    i = side.index(a)
    j = side.index(b, i) if b else len(side)
    return side[i:j]


find_html = piece('<div class="r"><select id="qt"', '<h3>Ход работ</h3>')
stats_html = piece('<div id="bar">', '\n<div class="ed"><h3>Режим</h3>')
mode_opts = piece('<div class="r">Вид работ при отметке:', '\n</div><h3>Поворот карты</h3>')
rot_html = piece('<div class="r" id="rot">', '\n<div class="ed"><details class="sec"><summary>Рисование')
draw_html = piece('<div class="ed"><details class="sec"><summary>Рисование', '<div class="ed"><details class="sec"><summary>Дворы')
yard_html = piece('<div class="ed"><details class="sec"><summary>Дворы', '<div class="ed"><h3>Отмена действий</h3>')
undo_html = piece('<div class="r"><button id="un"', '<div class="r">Вы вошли как:')
who_html = piece('<div class="r">Вы вошли как:', '<details id="hx">')
hist_html = piece('<details id="hx">', '<h3>Фильтр по видам работ</h3>')
wf_html = piece('<div id="wf" class="r"></div>', '<h3>Показывать</h3>')
show_html = piece('<div class="r">ТП: <details id="ftd">', '\n<div class="ed"><h3>Привязка к карте')
shift_html = piece('<div class="r">шаг, м', '\n</div><h3>Печать карты в PDF</h3>')
print_html = piece('<div class="r"><select id="pf">', '<h3>Отчёт</h3>')
report_html = piece('<div class="r">с <input type="date" id="rf">', '\n<div class="ed"><h3>Онлайн-база')
base_html = piece('<div class="ed"><h3>Онлайн-база (Supabase)</h3>', None)
def strip_close(h):
    h = h.rstrip()
    assert h.endswith('</div>'), h[-40:]
    return h[:-6]


who_html = strip_close(who_html)
base_html = strip_close(base_html)

new_side = f'''<div id="s">
<div class="sh"><b>Опоры освещения, Сортавала</b><span id="onl"></span></div>
<div class="vw">Режим просмотра. Редактирование недоступно.</div>
<nav id="tabs" aria-label="Разделы панели">
<button data-tab="work" class="on"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M14 7l3-3 3 3-3 3M17 4v9a4 4 0 0 1-4 4H4"/></svg>Работа</button>
<button data-tab="prog"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 20V10M10 20V4M16 20v-7M22 20H2"/></svg>Ход работ</button>
<button data-tab="filt"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M3 5h18l-7 8v6l-4-2v-4z"/></svg>Фильтры</button>
<button data-tab="rep"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6 9V3h12v6M6 18H4v-7h16v7h-2M7 14h10v7H7z"/></svg>Отчёты</button>
<button data-tab="more"><svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="5" cy="12" r="1.5"/><circle cx="12" cy="12" r="1.5"/><circle cx="19" cy="12" r="1.5"/></svg>Ещё</button>
</nav>
<div id="tbody">
<section class="tab" data-tab="work">
<h3>Найти опору</h3>{find_html}
<div class="ed"><h3>Что делаем</h3><div id="modes" class="seg"><button class="b on" data-m="view">Смотрю</button><button class="b" data-m="mark">Отмечаю</button><button class="b" data-m="edit">Двигаю</button><button class="b" data-m="add">Добавляю</button><button class="b" data-m="excl">Исключаю</button></div>
<div id="mopts">{mode_opts}</div></div>
<h3>Быстрые фильтры</h3><div id="qf" class="r"></div><small id="qfs"></small>
<h3>Сегодня</h3><div id="today" class="card"></div>
<div class="ed"><h3>Отмена действий</h3>{undo_html}</div>
</section>
<section class="tab" data-tab="prog" hidden>
<div id="kpi" class="card"></div>
<h3>По подстанциям <small id="tps">отстающие сверху</small></h3><div id="tpl"></div><button id="tpm" class="lnk">показать все ТП</button>
<h3>Темп за неделю</h3><div id="pace"></div>
<details class="sub"><summary>Подробнее: таблицы и обозначения</summary>{stats_html}</details>
</section>
<section class="tab" data-tab="filt" hidden>
<h3>Показывать</h3>{show_html}
<h3>Виды работ</h3>{wf_html}
</section>
<section class="tab" data-tab="rep" hidden>
<h3>Печать карты</h3>{print_html}
<h3>Отчёт за период</h3>{report_html}
{yard_html}
</section>
<section class="tab" data-tab="more" hidden>
{hist_html}
{draw_html}
<details class="sec"><summary>Поворот карты</summary>{rot_html}</details>
<div class="ed"><details class="sec"><summary>Привязка к карте (сдвиг всей сети)</summary>{shift_html}</details></div>
<div class="ed"><h3>Вход</h3>{who_html}</div>
{base_html}
</section>
</div>
</div>'''
s = s[:side_start] + new_side + s[side_end:]

# ---------------------------------------------------------------- styles
CSS = r'''
[hidden]{display:none!important}
#s{display:flex;flex-direction:column;padding:0!important}
#s .sh{display:flex;justify-content:space-between;align-items:center;padding:12px 14px 8px}#s .sh b{font-size:15px}#onl{font-size:12px;color:#4ade80}
#s .vw{margin:0 14px 8px}
#tabs{display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:4px;padding:0 10px 8px;border-bottom:1px solid #232838;position:sticky;top:0;background:inherit;z-index:2}
#tabs button{display:flex;flex-direction:column;align-items:center;gap:3px;padding:7px 0;border:0!important;border-radius:10px;background:transparent!important;color:#9aa3b5!important;font-size:11px;font-weight:500}
#tabs button svg{width:18px;height:18px;fill:none;stroke:currentColor;stroke-width:2;stroke-linecap:round;stroke-linejoin:round}
#tabs button.on{background:#1f2a4a!important;color:#fff!important;font-weight:600}
#tbody{flex:1;overflow:auto;padding:4px 14px 16px}
.card{background:#161a24;border:1px solid #232838;border-radius:12px;padding:10px 12px;display:flex;flex-direction:column;gap:6px}
.seg{display:flex;flex-wrap:wrap;gap:3px;background:#0c0f15;border:1px solid #2c3346;border-radius:10px;padding:3px}
.dk .seg button{flex:1 1 auto;border:0;background:transparent;font-size:12px;padding:7px 6px}.dk .seg button.on{background:#4f7cff;color:#fff}
#mopts .r{margin:6px 0}
#qf button{border-radius:999px!important;font-size:12px}#qf button.on{background:#24325c!important;border-color:#4f7cff!important;color:#fff!important}
.kr{display:flex;flex-direction:column;gap:3px}.kr .t{display:flex;justify-content:space-between}.kb{height:6px;border-radius:3px;background:#2c3346;overflow:hidden;display:flex}.kb i{display:block;height:100%}
#tpl{display:grid;grid-template-columns:72px minmax(0,1fr) 46px;gap:6px 8px;align-items:center;font-size:12px}#tpl .kb{height:8px;border-radius:4px}#tpl .n{text-align:right;color:#c3cad8}#tpl .z{color:#f87171}
#tpl span.nm{cursor:pointer}#tpl span.nm:hover{color:#9db4ff}
.lnk{background:none!important;border:0!important;color:#9db4ff!important;padding:4px 0!important;font-size:12px}
#pace .bars{display:flex;align-items:flex-end;gap:5px;height:56px}#pace .bars span{flex:1;background:#2563eb;border-radius:3px 3px 0 0;position:relative;min-height:2px}
#pace .bars span b{position:absolute;top:-15px;left:0;right:0;text-align:center;font-size:10px;color:#c3cad8;font-weight:500}
#pace .ax{display:flex;justify-content:space-between;color:#9aa3b5;font-size:11px;margin-top:3px}#pace .lg{color:#9aa3b5;font-size:11px;margin-top:2px}
#mbn{position:fixed;left:50%;top:calc(12px + env(safe-area-inset-top,0px));transform:translateX(-50%);z-index:1100;display:none;align-items:center;gap:10px;padding:7px 7px 7px 14px;border-radius:12px;background:#4f7cff;color:#fff;font-size:13px;box-shadow:0 8px 24px rgba(0,0,0,.3);max-width:calc(100vw - 32px)}
#mbn button{background:#fff!important;color:#1e3a8a!important;border:0!important;font-weight:700;border-radius:8px;padding:6px 12px}
#leg{position:fixed;left:calc(352px);bottom:calc(30px + env(safe-area-inset-bottom,0px));z-index:1000;background:rgba(22,26,36,.95);color:#c3cad8;border-radius:12px;padding:8px 12px;font-size:12px;display:flex;flex-direction:column;gap:4px;box-shadow:0 4px 14px rgba(0,0,0,.25)}
  .pr #leg,.pr #mbn{display:none!important}
#leg b{color:#eef1f7;font-weight:600;cursor:pointer}#leg i{display:inline-block;width:12px;height:12px;border-radius:50%;vertical-align:-2px;margin-right:6px;box-sizing:border-box}#leg.cl .li{display:none}
.tpc{display:flex;flex-direction:column;align-items:center;gap:2px;font-family:Commissioner,system-ui,sans-serif}
.tpc .ring{width:52px;height:52px;border-radius:50%;display:flex;align-items:center;justify-content:center;box-shadow:0 4px 12px rgba(0,0,0,.3)}
.tpc .ring b{width:36px;height:36px;border-radius:50%;background:#161a24;color:#fff;font-size:11px;display:flex;align-items:center;justify-content:center;text-align:center;line-height:1}
.tpc span{background:#161a24;color:#eef1f7;padding:1px 6px;border-radius:6px;font-size:11px;white-space:nowrap}
.c2{display:flex;flex-direction:column;gap:8px;min-width:240px}.c2 .hd{display:flex;justify-content:space-between;align-items:baseline;gap:8px}.c2 .hd b{font-size:15px}
.c2 .stg{display:flex;flex-direction:column;gap:3px}.c2 .stg .t{display:flex;justify-content:space-between;font-size:12px}.c2 .sb{display:flex;gap:3px}.c2 .sb span{flex:1;height:5px;border-radius:3px;background:#2c3346}
.c2 .nx{background:#16a34a!important;border-color:#16a34a!important;color:#fff!important;font-weight:700;padding:9px!important;font-size:13px!important;border-radius:10px!important;margin:0!important}
.c2 details>summary{color:#9db4ff;font-size:12px;cursor:pointer}
@media(max-width:700px){
 body{display:block!important}#m{position:fixed!important;inset:0}
 #s{position:fixed;left:0;right:0;bottom:0;width:auto!important;height:46vh!important;z-index:1200;border-radius:18px 18px 0 0;border-right:0!important;box-shadow:0 -8px 30px rgba(0,0,0,.35);padding-bottom:env(safe-area-inset-bottom,0px)!important}
 body.sc #s{height:auto!important}body.sc #tbody,body.sc #s .vw{display:none}
 #s .sh{padding:6px 14px 4px}#s .sh:before{content:"";position:absolute;left:50%;top:5px;width:40px;height:4px;margin-left:-20px;border-radius:2px;background:#3a4154}
 #leg{left:10px;bottom:calc(46vh + 12px)}body.sc #leg{bottom:110px}
 #gloc{bottom:calc(46vh + 12px)!important}body.sc #gloc{bottom:110px!important}
 #oqf{bottom:calc(46vh + 60px)!important}
}
'''
s = s.replace('</style>', CSS + '</style>', 1)

# ---------------------------------------------------------------- stage colours on the map and in the PDF plan
rep("function icon(p){const f=p.done?'#16a34a':(p.x?'#ef4444':'#fff'),s=p.x?'#b91c1c':(p.done?'#14532d':'#111');",
    "function icon(p){const sg=stage(p),f=p.x?'#ef4444':SGF[sg],s=p.x?'#b91c1c':SGS[sg];")
rep("const fill=done?'#16a34a':(p.x?'#ef4444':'#fff'),st=done?'#14532d':(p.x?'#b91c1c':'#111'),lw=Math.max(1.5,r*.3);",
    "const fill=p.x?'#ef4444':SGF[stage(p)],st=p.x?'#b91c1c':SGS[stage(p)],lw=Math.max(1.5,r*.3);")

# quick filters take part in visibility
rep("function vis(p){return tpOk(p)&&", "function vis(p){return tpOk(p)&&qfOk(p)&&")

# stats() also refreshes the new blocks
rep("function stats(){try{paInfo()}catch(e){}", "function stats(){stats0();try{v2stats()}catch(e){console.error(e)}}\nfunction stats0(){try{paInfo()}catch(e){}")

# pole card by stages
rep("function popup(p){if(RO)return roPopup(p);", "function popup(p){return card2(p,popup0(p))}\nfunction popup0(p){if(RO)return roPopup(p);")

# mode switch also updates the banner and the option rows
rep("document.body.classList.toggle('edm',mode=='edit');map.closePopup()});",
    "document.body.classList.toggle('edm',mode=='edit');map.closePopup();modeUI()});")

BLOCK = r'''
/* ================= v2: new panel ================= */
var SGF=['#ffffff','#2563eb','#16a34a','#eab308'],SGS=['#111827','#1e3a8a','#14532d','#713f12'],QF='',TPALL=false,TPL=L.layerGroup(),TODAYN={};
function found(p){return wdone(p,2)||wdone(p,10)||wdone(p,3)}
function stage(p){return ready(p)?3:p.done?2:found(p)?1:0}
function dtoday(){const d=new Date();return d.getFullYear()+'-'+String(d.getMonth()+1).padStart(2,'0')+'-'+String(d.getDate()).padStart(2,'0')}
function didToday(p){const t=dtoday();return p.date==t||Object.values(p.w||{}).includes(t)}
var QFS=[['none','Не начаты',p=>!p.x&&stage(p)==0&&!wdone(p,1)],['found','Фундамент есть, опоры нет',p=>!p.x&&found(p)&&!p.done],['nolamp','Опора без светильника',p=>!p.x&&p.done&&!(+p.sv>0)],['today','Сделано сегодня',p=>didToday(p)],['yard','Во дворах',p=>!!p.yd]];
function qfOk(p){if(!QF)return true;const q=QFS.find(x=>x[0]==QF);return q?q[2](p):true}
function qfRender(){$('qf').innerHTML=QFS.map(([k,n,f])=>{const c=P.filter(p=>tpOk(p)&&f(p)).length;return '<button data-q="'+k+'" class="'+(QF==k?'on':'')+'">'+n+' · '+c+'</button>'}).join('');$('qfs').textContent=QF?'Показаны только эти опоры. Нажмите ещё раз, чтобы снять.':''}
$('qf').onclick=e=>{const b=e.target.closest('button[data-q]');if(!b)return;QF=QF==b.dataset.q?'':b.dataset.q;P.forEach(upd);numLabels();stats();if(QF){const q=P.filter(vis);if(q.length)map.fitBounds(L.latLngBounds(q.map(p=>[p.lat,p.lon])).pad(.1))}};
function bar(segs){return '<div class="kb">'+segs.map(([w,c])=>'<i style="width:'+Math.max(0,Math.min(100,w))+'%;background:'+c+'"></i>').join('')+'</div>'}
function kpiRow(nm,v,of,c){return '<div class="kr"><div class="t"><span>'+nm+'</span><span><b style="color:'+c+'">'+v+'</b> <small>из '+of+' · '+Math.round(v/of*100)+'%</small></span></div>'+bar([[v/of*100,c]])+'</div>'}
function tpShort(t){t=String(t);return t.replace(/^КТП\s*/,'').replace(/^Шуно.*/,'Шуно')}
function v2stats(){const K=592,A=P.filter(p=>!p.x);
$('kpi').innerHTML='<div class="t" style="display:flex;justify-content:space-between"><b>По контракту</b><small>'+K+' опор · весь объект</small></div>'
+kpiRow('Закладные',A.filter(p=>wdone(p,2)).length,K,'#60a5fa')+kpiRow('Опоры',A.filter(p=>p.done).length,K,'#4ade80')
+kpiRow('Кронштейны',A.filter(p=>wdone(p,12)).length,K,'#c3cad8')+kpiRow('Светильники',A.reduce((a,p)=>a+(+p.sv||0),0),K,'#fde047');
const g={};A.forEach(p=>{if(!p.tp)return;(g[p.tp]=g[p.tp]||[]).push(p)});let rows=Object.entries(g).map(([t,a])=>{const n=a.length,d=a.filter(p=>p.done).length,f=a.filter(p=>!p.done&&found(p)).length;return{t,n,d,f,k:(d*2+f)/n}}).sort((x,y)=>x.k-y.k||y.n-x.n);
const all=rows.length;if(!TPALL)rows=rows.slice(0,6);
$('tpl').innerHTML=rows.map(r=>'<span class="nm" data-tp="'+esc(r.t)+'">'+esc(tpn(r.t))+'</span>'+bar([[r.d/r.n*100,'#16a34a'],[r.f/r.n*100,'#2563eb']])+'<span class="n '+(r.d+r.f?'':'z')+'">'+r.d+'/'+r.n+'</span>').join('');
$('tpm').textContent=TPALL?'свернуть':'показать все '+all+' ТП';
const days=[];for(let i=6;i>=0;i--){const d=new Date();d.setDate(d.getDate()-i);const s=d.getFullYear()+'-'+String(d.getMonth()+1).padStart(2,'0')+'-'+String(d.getDate()).padStart(2,'0');days.push(s)}
const zc=days.map(d=>A.filter(p=>wd(p,2)==d).length),pc=days.map(d=>A.filter(p=>p.date==d).length),mx=Math.max(1,...zc.map((z,i)=>z+pc[i]));
const avg=Math.round(zc.reduce((a,b)=>a+b,0)/7*10)/10;
$('pace').innerHTML='<div class="bars">'+days.map((d,i)=>'<span title="'+d+': закладных '+zc[i]+', опор '+pc[i]+'" style="height:'+((zc[i]+pc[i])/mx*100)+'%;background:linear-gradient(to top,#16a34a '+(pc[i]/Math.max(1,zc[i]+pc[i])*100)+'%,#2563eb 0)"><b>'+(zc[i]+pc[i]||'')+'</b></span>').join('')+'</div><div class="ax"><span>'+days[0].slice(8)+'.'+days[0].slice(5,7)+'</span><span>сегодня</span></div><div class="lg">синий — закладные, зелёный — опоры · закладных в среднем '+avg+' в день</div>';
const t=dtoday(),tw=WK.map(([k,n])=>[n,A.filter(p=>wd(p,k)==t).length]).filter(x=>x[1]),who=Object.entries(TODAYN).sort((a,b)=>b[1]-a[1]);
$('today').innerHTML=(tw.length?tw.map(([n,c])=>'<div style="display:flex;justify-content:space-between"><span>'+n+'</span><b style="color:#9db4ff">'+c+'</b></div>').join(''):'<small>Сегодня ещё нет отметок.</small>')
+(who.length?'<small>'+who.map(([n,c])=>esc(n)+' '+c).join(' · ')+'</small>':'')+(tw.length?'<button id="tdc" class="lnk" style="align-self:flex-start">скопировать для отчёта</button>':'');
const c=$('tdc');if(c)c.onclick=()=>{const s='Сортавала, освещение, '+t.split('-').reverse().join('.')+':\n'+tw.map(([n,c])=>'— '+n+': '+c).join('\n')+'\nВсего по контракту: закладных '+A.filter(p=>wdone(p,2)).length+', опор '+A.filter(p=>p.done).length+' из '+K;try{navigator.clipboard.writeText(s).then(()=>toast('Скопировано'),()=>prompt('Скопируйте текст:',s))}catch(e){prompt('Скопируйте текст:',s)}};
qfRender();legend();if(map.getZoom()<ZC)tpClusters()}
$('tpm').onclick=()=>{TPALL=!TPALL;v2stats()};
$('tpl').onclick=e=>{const n=e.target.closest('[data-tp]');if(!n)return;const a=P.filter(p=>p.tp==n.dataset.tp);if(a.length)map.fitBounds(L.latLngBounds(a.map(p=>[p.lat,p.lon])).pad(.1))};
async function todayWho(){if(!CF)return;try{const t=dtoday(),r=await fetch(CF.u+'/rest/v1/history?select=ed&ts=gte.'+t+'T00:00:00%2B03:00',{headers:H()}),j=await r.json();if(!Array.isArray(j))return;const m={};j.forEach(x=>{if(x.ed&&x.ed!='система'&&!/^Claude/.test(x.ed))m[x.ed]=(m[x.ed]||0)+1});TODAYN=m;v2stats()}catch(e){}}
setTimeout(todayWho,2500);setInterval(todayWho,60000);
/* legend with counts */
function legend(){let g=$('leg');if(!g){g=document.createElement('div');g.id='leg';document.body.appendChild(g);g.onclick=e=>{if(e.target.closest('b')){g.classList.toggle('cl');try{localStorage.setItem(KEY+'_legc',g.classList.contains('cl')?'1':'')}catch(x){}}};try{if(localStorage.getItem(KEY+'_legc')||innerWidth<700)g.classList.add('cl')}catch(x){}}
const A=P.filter(p=>!p.x&&tpOk(p)),c=[0,0,0,0];A.forEach(p=>c[stage(p)]++);const nm=['не начата','фундамент готов','опора стоит','горит, готова'];
g.innerHTML='<b>Этап опоры ▾</b>'+c.map((n,i)=>'<span class="li"><i style="background:'+SGF[i]+';border:2px solid '+SGS[i]+(i==3?';box-shadow:0 0 0 4px rgba(250,204,21,.45)':'')+'"></i>'+nm[i]+' · '+n+'</span>').join('')}
/* ТП badges when zoomed out */
var ZC=15;
function tpClusters(){TPL.clearLayers();const g={};P.forEach(p=>{if(p.x||!p.tp||!tpOk(p))return;(g[p.tp]=g[p.tp]||[]).push(p)});
Object.entries(g).forEach(([t,a])=>{const n=a.length,d=a.filter(p=>p.done).length,f=a.filter(p=>!p.done&&found(p)).length,la=a.reduce((s,p)=>s+p.lat,0)/n,lo=a.reduce((s,p)=>s+p.lon,0)/n,pd=d/n*100,pf=(d+f)/n*100;
const html='<div class="tpc"><div class="ring" style="background:conic-gradient(#16a34a 0 '+pd+'%,#2563eb '+pd+'% '+pf+'%,#cbd5e1 '+pf+'% 100%)'+(d+f?'':';box-shadow:0 0 0 3px #f87171,0 4px 12px rgba(0,0,0,.3)')+'"><b>'+esc(tpShort(t))+'</b></div><span>'+d+'/'+n+'</span></div>';
L.marker([la,lo],{icon:L.divIcon({html,className:'',iconSize:[60,72],iconAnchor:[30,30]}),title:tpn(t)+': опор стоит '+d+' из '+n}).on('click',()=>map.fitBounds(L.latLngBounds(a.map(p=>[p.lat,p.lon])).pad(.1))).addTo(TPL)})}
function zoomMode(){if(map.getZoom()<ZC){if(map.hasLayer(lg))map.removeLayer(lg);if(map.hasLayer(ll))map.removeLayer(ll);if(!map.hasLayer(TPL))TPL.addTo(map);tpClusters()}else{if(map.hasLayer(TPL))map.removeLayer(TPL);if(!map.hasLayer(lg))lg.addTo(map);if($('fl').checked&&!map.hasLayer(ll))ll.addTo(map)}}
map.on('zoomend',zoomMode);
/* pole card by stages */
function stagesOf(p){return[['Фундамент',isG(p)?[1,10]:[1,2,3]],['Опора',[4]],['Монтаж',[12,5,6]]]}
function nextWork(p){for(const[,ks]of stagesOf(p))for(const k of ks)if(!wdone(p,k))return k;return null}
function card2(p,old){const w=document.createElement('div');w.className='c2';const sg=stagesOf(p),nk=nextWork(p),nm=k=>(WK.find(x=>x[0]==k)||[0,''])[1];
const title=old.firstElementChild;const sub=[p.t=='A'?'анкерная':'станд.',isG(p)?'гравит.':'закладная'];if(+p.kr)sub.push(p.kr==2?'2 рожка':'1 рожок');if(p.x)sub.push('исключена');
w.innerHTML='<div class="hd"><b>'+esc(p.id)+'</b><small>'+sub.join(' · ')+'</small></div>'+sg.map(([n,ks])=>{const dn=ks.filter(k=>wdone(p,k)).length,last=ks.map(k=>wd(p,k)).filter(v=>/^\d{4}-/.test(v)).sort().pop();
return '<div class="stg"><div class="t"><b>'+n+'</b><small style="color:'+(dn==ks.length?'#4ade80':'#9aa3b5')+'">'+(dn==ks.length?'готово'+(last?' · '+last.slice(8)+'.'+last.slice(5,7):''):dn+' из '+ks.length)+'</small></div><div class="sb">'+ks.map(k=>'<span title="'+esc(nm(k))+'" style="'+(wdone(p,k)?'background:'+(n=='Фундамент'?'#2563eb':n=='Опора'?'#16a34a':'#eab308'):'')+'"></span>').join('')+'</div></div>'}).join('')
+(!RO&&nk&&!p.x?'<button class="nx">Следующее: '+esc(nm(nk))+'</button>':'');
if(title&&!RO)title.remove();const det=document.createElement('details');det.innerHTML='<summary>'+(RO?'все работы и даты':'все работы, даты и настройки опоры')+'</summary>';det.appendChild(old);w.appendChild(det);
const b=w.querySelector('.nx');if(b)b.onclick=()=>{setW(p,nk,true,$('md').value||dtoday());upd(p);save();stats();mark(p);const m=mk.get(p);L.popup(PO()).setLatLng(m?m.getLatLng():[p.lat,p.lon]).setContent(popup(p)).openOn(map);toast(p.id+': '+nm(nk))};
return w}
/* mode banner and options */
function modeUI(){if(RO)return;const mb=$('mbn')||(()=>{const d=document.createElement('div');d.id='mbn';d.innerHTML='<span id="mbt"></span><button id="mbx">Готово</button>';document.body.appendChild(d);$('mbx').onclick=()=>document.querySelector('#modes [data-m=view]').click();return d})();
const t={mark:'<b>Отмечаю:</b> '+esc(($('mw').selectedOptions[0]||{}).text||'')+', '+($('md').value||'').split('-').reverse().join('.')+' · нажимайте на опоры',edit:'<b>Двигаю опоры:</b> перетащите опору, карта спросит подтверждение',add:'<b>Добавляю опоры:</b> нажмите на карту, где поставить новую',excl:'<b>Исключаю:</b> нажатие исключает опору или возвращает её'}[mode];
mb.style.display=t?'flex':'none';if(t)$('mbt').innerHTML=t;
document.querySelectorAll('#mopts .r').forEach((r,i)=>{r.hidden=!((mode=='mark'&&i<2)||(mode=='add'&&i==2))})}
if(!RO){$('mw').innerHTML=WK.map(([k,n])=>'<option value="'+k+'"'+(k==4?' selected':'')+'>'+n+'</option>').join('');$('mw').onchange=$('md').onchange=modeUI;modeUI()}
/* tabs */
function tab(t){document.querySelectorAll('#tabs button').forEach(b=>b.classList.toggle('on',b.dataset.tab==t));document.querySelectorAll('#tbody .tab').forEach(s=>s.hidden=s.dataset.tab!=t);try{localStorage.setItem(KEY+'_tab',t)}catch(e){}}
$('tabs').onclick=e=>{const b=e.target.closest('button[data-tab]');if(!b)return;if(innerWidth<=700&&b.classList.contains('on')){document.body.classList.toggle('sc');setTimeout(()=>map.invalidateSize(),50);return}document.body.classList.remove('sc');tab(b.dataset.tab);setTimeout(()=>map.invalidateSize(),50)};
try{const t=localStorage.getItem(KEY+'_tab');if(t&&document.querySelector('#tabs [data-tab="'+t+'"]'))tab(t)}catch(e){}
if(innerWidth<=700)document.body.classList.add('sc');
setInterval(()=>{const t=($('ss').textContent||'');$('onl').textContent=/синхрониз/.test(t)?'● онлайн':(/нет связи/.test(t)?'● нет связи':'');$('onl').style.color=/нет связи|ошибка/.test(t)?'#f87171':'#4ade80'},2000);
setTimeout(()=>{map.invalidateSize();zoomMode()},300);
'''
rep('\nredraw();stats();map.fitBounds', BLOCK + 'redraw();stats();map.fitBounds')

# the old fixed stats widths: let #leg sit next to the panel
open('redaktor2.html', 'w', encoding='utf-8').write(s)
open('prosmotr2.html', 'w', encoding='utf-8').write(s.replace('const RO=/*RO*/false', 'const RO=true'))
print('ok', len(s))
