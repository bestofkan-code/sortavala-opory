# Фильтр «Только ввод КЛ»: на карте остаются только опоры с отметкой «ввод КЛ» (люк, бронекабель от ТП)
import sys
fn=sys.argv[1];s=open(fn,encoding='utf-8').read()
def rep(a,b):
    global s
    assert s.count(a)==1,(s.count(a),a[:80]);s=s.replace(a,b)
rep('<div class="r"><button class="b" id="nbb"','<div class="r"><button class="b" id="vkb" style="border-color:#c026d3">Только ввод КЛ</button><small id="vks"></small></div><div class="r"><button class="b" id="nbb"')
rep("function vis(p){return ftyOk(p)&&visB(p)&&(!NB||nbOk(p))","function vis(p){return ftyOk(p)&&visB(p)&&(!VKF||vkOk(p))&&(!NB||nbOk(p))")
JS=r"""
var VKF=false;try{VKF=localStorage.getItem(KEY+'_vkf')==='1'}catch(e){}
function vkOk(p){return !!p.vk&&!p.x}
function vkUI(){const b=$('vkb');if(!b)return;b.style.background=VKF?'#c026d3':'';b.style.color=VKF?'#fff':'';b.textContent=VKF?'Показан только ввод КЛ ✕':'Только ввод КЛ';const L2=P.filter(p=>vkOk(p)&&tpOk(p)),n=L2.length,d=L2.filter(p=>p.done).length;$('vks').innerHTML='опоры с люком и бронекабелем от ТП: <b>'+n+'</b>'+(n?', установлено '+d:'')}
$('vkb').onclick=()=>{VKF=!VKF;try{localStorage.setItem(KEY+'_vkf',VKF?'1':'0')}catch(e){}vkUI();P.forEach(upd);numLabels();if(VKF){const L2=P.filter(p=>vkOk(p)&&tpOk(p));if(L2.length)map.fitBounds(L.latLngBounds(L2.map(p=>[p.lat,p.lon])).pad(.15),{maxZoom:17});else toast('Опор с вводом КЛ нет')}};setTimeout(vkUI,0);
{const _st2=stats;stats=function(){const r=_st2.apply(this,arguments);try{vkUI()}catch(e){}return r}}
"""
a="else toast('Таких опор нет: везде, где стоит закладная, отмечен и бетон')}};setTimeout(nbUI,0);"
rep(a,a+JS)
open(fn,'w',encoding='utf-8').write(s);print('ok')
