import sys,re
FILES=['redaktor.html','prosmotr.html','montazh.html','zamechaniya.html','zamechaniya-prosmotr.html','uchastki.html']
R=[
('<button class="b" id="gzb" style="border-color:#65a30d">Нужен котлован под заземление</button><small id="gzs"></small>',
 '<span id="gzb" class="gzr"><b style="font-size:12px;margin-right:4px">Заземление:</b><button class="b" data-gz="1" style="border-color:#65a30d" title="Показать только опоры, где котлован под заземление ещё не выкопан">Осталось</button><button class="b" data-gz="2" style="border-color:#65a30d" title="Показать только опоры, где заземление выполнено">Выполнены</button><button class="b" data-gz="3" style="border-color:#65a30d" title="Показать все опоры под повторное заземление">Все</button></span><small id="gzs" style="display:block"></small>'),
("var GZF=false;try{GZF=localStorage.getItem(KEY+'_gzf')==='1'}catch(e){}",
 "var GZF=0;try{GZF=+(localStorage.getItem(KEY+'_gzf')||0)||0;if(GZF<0||GZF>3)GZF=0}catch(e){}"),
("function gzOk(p){return gzEl(p)&&!wdone(p,11)}",
 "function gzDn(p){return wdone(p,11)||wdone(p,15)}function gzOk(p){return gzEl(p)&&!gzDn(p)}function gzDone(p){return gzEl(p)&&gzDn(p)}function gzPass(p){return GZF==1?gzOk(p):GZF==2?gzDone(p):gzEl(p)}"),
("(!GZF||gzOk(p))","(!GZF||gzPass(p))"),
]
GZUI_RE=re.compile(r"function gzUI\(\)\{.*?\(выкопано '\+\(E\.length-n\)\+'\)'\}",re.S)
GZUI_NEW="function gzUI(){const b=$('gzb');if(!b)return;b.querySelectorAll('button[data-gz]').forEach(x=>{const on=+x.dataset.gz==GZF;x.style.background=on?'#65a30d':'';x.style.color=on?'#fff':''});const E=P.filter(p=>gzEl(p)&&tpOk(p)),d=E.filter(gzDn).length;$('gzs').innerHTML='выполнено <b>'+d+'</b> из '+E.length+' · осталось <b>'+(E.length-d)+'</b>'+(GZF?' · <a href=\"#\" data-gz=\"0\">показать все опоры</a>':'')}"
HND_RE=re.compile(r"<script>\(function\(\)\{const b=document\.getElementById\('gzb'\);if\(!b\)return;b\.onclick=.*?setTimeout\(gzUI,3000\)\}\)\(\);</script>",re.S)
HND_NEW="<script>(function(){const b=document.getElementById('gzb');if(!b)return;const set=v=>{GZF=GZF==v?0:v;try{localStorage.setItem(KEY+'_gzf',String(GZF))}catch(e){}gzUI();P.forEach(upd);numLabels();if(GZF){const L2=P.filter(p=>gzPass(p)&&tpOk(p));if(L2.length)map.fitBounds(L.latLngBounds(L2.map(p=>[p.lat,p.lon])).pad(.15),{maxZoom:17});else toast(GZF==1?'Все котлованы под заземление выкопаны':'Таких опор нет')}};b.onclick=e=>{const x=e.target.closest('[data-gz]');if(x)set(+x.dataset.gz)};const s2=document.getElementById('gzs');if(s2)s2.onclick=e=>{const x=e.target.closest('[data-gz]');if(x){e.preventDefault();GZF=1;set(0)}};try{const _s=stats;stats=function(){const r=_s.apply(this,arguments);try{gzUI()}catch(e){}return r}}catch(e){}setTimeout(gzUI,0);setTimeout(gzUI,3000)})();</script>"
for f in FILES:
    s=open(f,encoding='utf-8').read()
    for a,b in R:
        c=s.count(a)
        if c<1: sys.exit(f'{f}: miss {a[:50]}')
        s=s.replace(a,b)
    s,n1=GZUI_RE.subn(lambda m:GZUI_NEW,s); s,n2=HND_RE.subn(lambda m:HND_NEW,s)
    if n1!=1 or n2!=1: sys.exit(f'{f}: gzUI {n1} handler {n2}')
    open(f,'w',encoding='utf-8').write(s); print('ok',f)
