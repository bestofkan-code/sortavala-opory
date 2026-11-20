# Режим «Смена ТП»: выбираете ТП (из списка или «взять с опоры»), затем нажимаете опоры — каждая сразу
# переходит в выбранную ТП (номер сохраняется, если свободен, иначе следующий свободный). «Отменить последнее».
import sys
p=sys.argv[1];s=open(p,encoding='utf-8').read()
def R(a,b,n=1):
    global s
    assert s.count(a)==n,(a[:90],s.count(a));s=s.replace(a,b)
R('<button class="b" data-m="line">Линии</button>','<button class="b" data-m="line">Линии</button><button class="b" data-m="retp" style="border-color:#a3e635">Смена ТП</button>')
R('<small id="lmh" style="display:none;color:#9db4ff">',
  '<div id="rtp" hidden style="margin:4px 0;padding:6px 8px;border:1px solid #a3e635;border-radius:8px"><b>Смена ТП</b><div class="r" style="align-items:center;gap:6px;margin-top:4px"><span>Перенести в</span><select id="rtps" style="flex:1;min-width:0"></select></div><div class="r" style="gap:6px"><button id="rtpp">Взять ТП с опоры</button><button id="rtpu" disabled>Отменить последнее</button></div><small id="rtpi" style="display:block;color:#9db4ff">Нажимайте на опоры — каждая сразу перейдёт в выбранную ТП. Номер сохраняется, если свободен, иначе ставится следующий свободный. «Взять ТП с опоры» — следующее нажатие выберет ТП той опоры.</small></div><small id="lmh" style="display:none;color:#9db4ff">')
R("else if(mode=='line')leTap(p);","else if(mode=='retp')rtpTap(p);else if(mode=='line')leTap(p);")
JS=r"""
/* ---- режим «Смена ТП» ---- */
var RTPU=[],RTPPICK=false;
function rtpFill(){const e=$('rtps');if(!e)return;const v=e.value;e.innerHTML='<option value="">— выберите ТП —</option>'+tpList().map(t=>'<option value="'+esc(t)+'">'+esc(tpn(t))+'</option>').join('');if(v)e.value=v;e.style.borderLeft='6px solid '+(e.value?tpCol(e.value):'#475569')}
function rtpApply(p,t,n){p.tp=t;p.n=n;p.id=pid(t,n);upd(p);save();stats();mark(p);lines();try{numLabels()}catch(e){}}
function rtpTap(p){if(RTPPICK){RTPPICK=false;$('rtpp').classList.remove('on');rtpFill();$('rtps').value=String(p.tp||'');rtpFill();toast('Выбрана '+tpn(p.tp)+' — теперь нажимайте опоры для переноса');return}
 const t=$('rtps').value;if(!t){toast('Сначала выберите ТП в списке или нажмите «Взять ТП с опоры»');return}if(String(p.tp||'')==t){toast(p.id+' уже в '+tpn(t));return}
 const used=new Set(P.filter(q=>q!==p&&String(q.tp||'')==t).map(q=>+q.n));let n=+p.n;if(!n||used.has(n))n=Math.max(0,...used)+1;
 const o={p,tp:p.tp,n:p.n,id:p.id};RTPU.push(o);$('rtpu').disabled=false;rtpApply(p,t,n);toast(o.id+' → '+p.id)}
setTimeout(()=>{if(!$('rtp'))return;document.querySelectorAll('#modes button').forEach(b=>b.addEventListener('click',()=>{$('rtp').hidden=mode!='retp';if(mode=='retp')rtpFill();else{RTPPICK=false}}));
 $('rtps').onchange=rtpFill;$('rtpp').onclick=()=>{RTPPICK=!RTPPICK;$('rtpp').classList.toggle('on',RTPPICK);if(RTPPICK)toast('Нажмите на опору нужной ТП')};
 $('rtpu').onclick=()=>{const o=RTPU.pop();if(!o)return;const cur=o.p.id;rtpApply(o.p,o.tp,o.n);o.p.id=o.id;upd(o.p);mark(o.p);toast('Отменено: '+cur+' → '+o.id);$('rtpu').disabled=!RTPU.length}},0);
"""
R("function add(p){const m=L.marker(",JS+"\nfunction add(p){const m=L.marker(")
open(p,'w',encoding='utf-8').write(s);print('ok retp',p)
