# Подрезка крон бригады (работа 14) на основной карте: блок «Подрезка крон — бригада» и фотоотчёты: наша / бригада / вся подрезка
import sys
fn=sys.argv[1];s=open(fn,encoding='utf-8').read()
def R(a,b,n=1):
    global s
    assert s.count(a)==n,(a[:90],s.count(a));s=s.replace(a,b)
# 1) фотоотчёт по списку работ KS (9 — наша, 14 — бригада)
a=s.index('async function ppReport(');b=s.index("$('ppr').onclick",a);t=s[a:b]
t=t.replace("async function ppReport(){","async function ppReport(KS,TT){KS=Array.isArray(KS)?KS:[PRK];TT=TT||PRT;",1)
t=t.replace("const L2=P.filter(p=>tpOk(p)&&!p.x&&(wdone(p,PRK)?(!(f||e)||ir(wd(p,PRK))):(!(f||e)&&ppN(p.uid,PRK)))).sort((a,b)=>String(a.tp).localeCompare(String(b.tp),'ru',{numeric:true})||(+a.n||0)-(+b.n||0));",
 "const L2=KS.flatMap(k=>P.filter(p=>tpOk(p)&&!p.x&&(wdone(p,k)?(!(f||e)||ir(wd(p,k))):(!(f||e)&&ppN(p.uid,k)))).map(p=>({...p,_k:k}))).sort((a,b)=>String(a.tp).localeCompare(String(b.tp),'ru',{numeric:true})||(+a.n||0)-(+b.n||0)||a._k-b._k);",1)
for x,y in [('wdone(p,PRK)','wdone(p,p._k)'),('wd(p,PRK)','wd(p,p._k)'),('ppN(p.uid,PRK)','ppN(p.uid,p._k)'),('ppL(p.uid,PRK,kind)','ppL(p.uid,p._k,kind)'),('g.fillText(PRT,50,62)','g.fillText(TT,50,62)'),("doc.save(PRT.replace(':','')","doc.save(TT.replace(':','')")]:
    t=t.replace(x,y)
assert 'PRK' not in t.replace('KS=Array.isArray(KS)?KS:[PRK]','')
t=t.replace("g.fillText((wdone(p,p._k)?'подрезка выполнена '","g.fillText((p._k==14?'бригада · ':(KS.length>1?'наша · ':''))+(wdone(p,p._k)?'подрезка выполнена '",1)
s=s[:a]+t+s[b:]
R("$('ppr').onclick=ppReport;","$('ppr').onclick=()=>ppReport([PRK]);")
# 2) кнопки отчётов рядом с нашим фотоотчётом
R('<div class="r"><button id="ppr">Фотоотчёт: подрезка крон (PDF)</button></div>',
  '<div class="r"><button id="ppr">Фотоотчёт: подрезка крон (PDF)</button></div><div class="r" id="ppr2w"><button id="ppr14">Фотоотчёт: подрезка бригады (PDF)</button><button id="pprall">Вся подрезка: наша + бригада (PDF)</button></div>')
R("$('ppr').onclick=()=>ppReport([PRK]);","$('ppr').onclick=()=>ppReport([PRK]);if($('ppr14'))$('ppr14').onclick=()=>ppReport([14],'Фотоотчёт: подрезка крон деревьев (бригада монтажников)');if($('pprall'))$('pprall').onclick=()=>ppReport([9,14],'Фотоотчёт: подрезка крон деревьев (наша и бригада)');")
# 3) блок «Подрезка крон — бригада»
js=r"""
function trGo(u){const q=P.find(p=>p.uid==u);if(!q)return;const m=mk.get(q);map.setView([q.lat,q.lon],Math.max(map.getZoom(),18));if(m&&lg.hasLayer(m))L.popup(PO()).setLatLng(m.getLatLng()).setContent(popup(q)).openOn(map);else toast('Опора '+q.id+' скрыта фильтром')}
function trUI(){if(document.body.classList.contains('crew'))return;let d=$('trd');if(!d){const sk=$('matd')||$('skd');if(!sk)return;sk.insertAdjacentHTML('afterend','<details id="trd"><summary><b>Подрезка крон — бригада</b> <span id="trs"></span></summary><div id="trw"></div></details>');d=$('trd')}
 const fd=v=>/^\d{4}-/.test(v||'')?v.slice(8,10)+'.'+v.slice(5,7)+'.'+v.slice(0,4):'';
 const A=P.filter(p=>!p.x&&(wdone(p,14)||ppN(p.uid,14))).sort((a,b)=>String(wd(b,14)||'').localeCompare(String(wd(a,14)||''))||String(a.tp).localeCompare(String(b.tp),'ru',{numeric:true})||(+a.n||0)-(+b.n||0));
 const D=A.filter(p=>wdone(p,14)),noA=D.filter(p=>!ppL(p.uid,14,'after').length).length,noB=D.filter(p=>!ppL(p.uid,14,'before').length).length,O=P.filter(p=>!p.x&&wdone(p,9)).length;
 $('trs').textContent='· '+D.length+' опор'+(noA?' · без фото «после»: '+noA:'');
 $('trw').innerHTML='<small>Бригада отмечает свою подрезку на монтажной карте (отдельно от нашей). Наша подрезка: '+O+' опор. Фото — в карточке опоры, блок «Подрезка крон (бригада) — фото».</small>'
 +(A.length?'<table class="trt"><tr><th>Опора</th><th>Дата</th><th>До</th><th>После</th></tr>'+A.map(p=>'<tr data-tru="'+p.uid+'"><td>'+esc(p.id)+'</td><td>'+(fd(wd(p,14))||'<span style="color:#9ca3af">не отмечена</span>')+'</td><td>'+(ppN(p.uid,14)?ppL(p.uid,14,'before').length:'')+'</td><td'+(wdone(p,14)&&!ppL(p.uid,14,'after').length?' style="color:#dc2626"':'')+'>'+(ppL(p.uid,14,'after').length||(wdone(p,14)?'нет':''))+'</td></tr>').join('')+'</table>':'<small>Пока нет отметок бригады.</small>')
 +(noB?'<small>Без фото «до»: '+noB+'</small>':'')+'<div class="r"><button data-trr=14>Фотоотчёт бригады (PDF)</button><button data-trr=all>Вся подрезка (PDF)</button></div><small>Отчёт берёт ТП и даты из фильтра.</small>';
 $('trw').querySelectorAll('[data-tru]').forEach(r=>r.onclick=()=>trGo(r.dataset.tru));
 $('trw').querySelectorAll('[data-trr]').forEach(b=>b.onclick=()=>{$('pprs')&&$('pprs').scrollIntoView({block:'nearest'});b.dataset.trr=='14'?$('ppr14').click():$('pprall').click()})}
"""
R("$('ppr').onclick=()=>ppReport([PRK]);",js+"$('ppr').onclick=()=>ppReport([PRK]);")
R("try{matUI()}catch(e){}","try{matUI()}catch(e){}try{trUI()}catch(e){}")
R("function ppRefresh(){","function ppRefresh(){try{trUI()}catch(e){}")
R('<style>select.od-d','<style>#trd .trt{width:100%;border-collapse:collapse;font-size:12px;margin:4px 0}#trd .trt td,#trd .trt th{padding:2px 4px;border-bottom:1px solid rgba(127,127,127,.25);text-align:left}#trd .trt tr[data-tru]{cursor:pointer}#trd .trt tr[data-tru]:hover{background:rgba(96,165,250,.15)}body.crew #trd,body.crew #ppr2w{display:none}select.od-d')
open(fn,'w',encoding='utf-8').write(s);print('ok tree main')
