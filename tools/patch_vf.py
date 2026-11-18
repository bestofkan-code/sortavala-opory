#!/usr/bin/env python3
"""Сверка котлованов на месте (колонка poles.vf jsonb).

vf = {d: дата, e: кто сверил, z: '24'|'30' — фактическая закладная (ЗФ-24/8 / ЗФ-30/8),
      c: комментарий, o: [lat, lon] — точка до переноса по GPS, mv: на сколько метров перенесена}
Нет vf — опора не сверена.

- В окне опоры (редактор, замечания, участки) блок «Сверка на месте»: галочка «котлован на месте,
  точка верна», фактическая закладная (по умолчанию — по типу опоры), «поставить по GPS» (опора
  сразу переносится в точку телефона), комментарий. На монтажной карте блока нет.
- На карте: зелёное кольцо — сверено, оранжевое — расхождение (другая закладная или сдвиг ≥ 3 м).
- Кнопка «Не сверены» (только забуренные/с закладной, без исключённых, серых, гравит.), счётчик,
  «Excel: сверка» — расхождения и не сверенные.
- В просмотре — строка о сверке в карточке.
Применять ко всем страницам:
  for f in redaktor.html prosmotr.html zamechaniya.html zamechaniya-prosmotr.html montazh.html uchastki.html; do python3 tools/patch_vf.py $f; done
"""
import sys
path = sys.argv[1]
s = open(path, encoding='utf-8').read()
if 'id="vfb"' in s:
    print('already applied', path); sys.exit(0)
def R(old, new, cnt=1):
    global s
    n = s.count(old); assert n == cnt, (path, old[:80], n); s = s.replace(old, new)

# --- синхронизация с базой
R("od:p.od||null,ar:p.ar||null};miss", "od:p.od||null,ar:p.ar||null,vf:p.vf||null};miss")
R("od:r.od||'',ar:r.ar||null,tp:r.tp,", "od:r.od||'',ar:r.ar||null,vf:r.vf||null,tp:r.tp,")
R("'sp','od','ar']", "'sp','od','ar','vf']")
R("var SF=['ar','od',", "var SF=['vf','ar','od',")

# --- кнопка и счётчик
R('<button class="b" id="nkb" style="border-color:#d97706">Не забурены котлованы</button><small id="nks"></small></div>',
  '<button class="b" id="nkb" style="border-color:#d97706">Не забурены котлованы</button><small id="nks"></small></div>'
  '<div class="r"><button class="b" id="vfb" style="border-color:#16a34a">Не сверены котлованы</button><button class="b" id="vfx">Excel: сверка</button><small id="vfs"></small></div>')

# --- логика
JS = r"""
{const st=document.createElement('style');st.textContent='.vfb{border:1px solid #4b5563;border-radius:8px;padding:6px 8px;margin:6px 0;font-size:12.5px}.vfb.ok{border-color:#16a34a;background:rgba(22,163,74,.12)}.vfb.bad{border-color:#f97316;background:rgba(249,115,22,.14)}.vft{font-weight:700;margin-bottom:3px}.vfc{display:flex;gap:6px;align-items:center;font-size:13px;padding:3px 0}.vfc input{width:20px;height:20px}.vfr{display:flex;flex-wrap:wrap;gap:6px;align-items:flex-end;margin:4px 0}.vfr label{display:flex;flex-direction:column;font-size:11px}.vfr button{padding:7px 10px}.vfb input[type=text]{width:100%;margin-top:2px}.vfb small{display:block;margin-top:3px;opacity:.85}';document.head.appendChild(st)}
const VF_ON=!RO&&!/montazh/i.test(location.pathname);
const VFZ={'24':'ЗФ-24/8 (СФГ-400)','30':'ЗФ-30/8 (СФГ-700)'},VFS={'24':'ЗФ-24/8','30':'ЗФ-30/8'};
function vfEl(p){return !p.x&&!p.pp&&!isG(p)&&(wdone(p,1)||wdone(p,2))}
function vfExp(p){return p.t=='A'?'30':'24'}
function vfBad(p){const v=p.vf;if(!v)return '';const a=[];if(v.z&&v.z!=vfExp(p))a.push('закладная '+VFS[v.z]+' вместо '+VFS[vfExp(p)]);if(+v.mv>=3)a.push('точка перенесена на '+v.mv+' м');return a.join(', ')}
function vfRing(p){if(!p.vf)return '';return `<circle r="17.5" fill="none" stroke="${vfBad(p)?'#f97316':'#16a34a'}" stroke-width="3"/>`}
function vfToday(){return new Date(Date.now()-new Date().getTimezoneOffset()*6e4).toISOString().slice(0,10)}
function vfTxt(p){const v=p.vf;if(!v)return vfEl(p)?'<div style="font-size:11.5px;color:#9ca3af">Сверка на месте: не сверена</div>':'';const b=vfBad(p);
 return `<div style="font-size:11.5px;color:${b?'#ea580c':'#15803d'}">Сверено ${esc(v.d||'')}${v.e?' · '+esc(v.e):''}: закладная ${VFS[v.z||vfExp(p)]}${b?' · <b>'+b+'</b>':''}${v.c?' · '+esc(v.c):''}</div>`}
function vfH(p){return VF_ON&&(vfEl(p)||p.vf)?'<div class="vfb" data-vfb></div>':''}
function vfSet(p,ch){p.vf=Object.assign({},p.vf||{z:vfExp(p)},ch,{d:vfToday(),e:WHO||''})}
function vfDraw(b,p){const v=p.vf,bad=vfBad(p);b.className='vfb'+(v?(bad?' bad':' ok'):'');
 b.innerHTML=`<div class="vft">Сверка на месте</div><label class="vfc"><input type=checkbox data-vok ${v?'checked':''}> котлован на месте, точка на карте верна</label>
<div class="vfr"><label>Закладная факт.<select data-vz>${['24','30'].map(z=>`<option value="${z}" ${((v&&v.z)||vfExp(p))==z?'selected':''}>${VFZ[z]}${z==vfExp(p)?' — по типу':''}</option>`).join('')}</select></label><button type=button data-vg>📍 Точка не там — поставить по GPS</button></div>
<input type=text data-vc placeholder="Комментарий к сверке" value="${esc((v&&v.c)||'')}">${v?`<small>Сверено ${esc(v.d||'')}${v.e?' · '+esc(v.e):''}${v.mv?' · перенесена на '+v.mv+' м':''}${bad?' · <b>'+bad+'</b>':''}</small>`:''}`;
 const ch=()=>{upd(p);save();stats();mark(p);vfDraw(b,p)};
 b.querySelector('[data-vok]').onchange=e=>{if(e.target.checked)vfSet(p,{z:b.querySelector('[data-vz]').value});else{if(p.vf&&p.vf.mv&&!confirm('Снять сверку? Опора останется в новой точке (старая — в истории опоры).')){e.target.checked=true;return}p.vf=null}ch()};
 b.querySelector('[data-vz]').onchange=e=>{vfSet(p,{z:e.target.value});ch();if(vfBad(p))toast(p.id+': '+vfBad(p))};
 b.querySelector('[data-vc]').onchange=e=>{vfSet(p,{c:e.target.value.trim()});ch()};
 b.querySelector('[data-vg]').onclick=e=>{if(!navigator.geolocation)return alert('Геолокация недоступна на этом устройстве');const bt=e.target;bt.disabled=true;bt.textContent='Определяю место…';
  navigator.geolocation.getCurrentPosition(g=>{bt.disabled=false;bt.textContent='📍 Точка не там — поставить по GPS';const c=L.latLng(g.coords.latitude,g.coords.longitude),a=Math.round(g.coords.accuracy||0),dd=Math.round(map.distance([p.lat,p.lon],c));
   if(a>25&&!confirm('Точность GPS сейчас плохая: ±'+a+' м. Лучше подождать на открытом месте и нажать ещё раз. Всё равно перенести?'))return;
   if(!confirm('Перенести опору '+p.id+' на '+dd+' м в точку, где вы стоите (точность ±'+a+' м)?'))return;
   const o=(p.vf&&p.vf.o)||[p.lat,p.lon];p.lat=c.lat;p.lon=c.lng;vfSet(p,{o,mv:Math.round(map.distance(o,c)),z:b.querySelector('[data-vz]').value});const m=mk.get(p);if(m)m.setLatLng(c);lines();ch();toast(p.id+' перенесена на '+dd+' м и отмечена как сверенная')},
   er=>{bt.disabled=false;bt.textContent='📍 Точка не там — поставить по GPS';alert('Не удалось определить место: '+(er.code==1?'нет разрешения на геолокацию в браузере':er.message))},{enableHighAccuracy:true,timeout:20000,maximumAge:0})}}
var VS=false;try{VS=localStorage.getItem(KEY+'_vs')==='1'}catch(e){}
function vsOk(p){return vfEl(p)&&!p.vf}
function vfUI(){const b=$('vfb');if(!b)return;b.style.background=VS?'#16a34a':'';b.style.color=VS?'#fff':'';b.textContent=VS?'Показаны не сверенные ✕':'Не сверены котлованы';
 const E=P.filter(p=>vfEl(p)&&tpOk(p)),n=E.filter(p=>p.vf).length,k=E.filter(p=>vfBad(p)).length;$('vfs').innerHTML='сверено <b>'+n+'</b> из '+E.length+(k?', расхождений <b style="color:#ea580c">'+k+'</b>':'')}
function vfXl(){const E=P.filter(p=>vfEl(p)&&tpOk(p)),wb=XLSX.utils.book_new(),H=['Опора','ТП','Тип опоры','Закладная по типу','Закладная факт.','Перенесена, м','Сверено','Кто','Комментарий','Широта','Долгота'];
 const row=p=>{const v=p.vf||{};return [p.id,p.tp||'',p.t=='A'?'анкерная':'станд.',VFS[vfExp(p)],v.z?VFS[v.z]:'',v.mv||'',v.d||'',v.e||'',v.c||'',+(+p.lat).toFixed(6),+(+p.lon).toFixed(6)]};
 const S=(a,b)=>String(a.id).localeCompare(String(b.id),'ru',{numeric:true});
 XLSX.utils.book_append_sheet(wb,XLSX.utils.aoa_to_sheet([['Расхождения при сверке котлованов'],H.concat(['Что не так']),...E.filter(p=>vfBad(p)).sort(S).map(p=>row(p).concat([vfBad(p)]))]),'Расхождения');
 XLSX.utils.book_append_sheet(wb,XLSX.utils.aoa_to_sheet([['Не сверены'],H,...E.filter(p=>!p.vf).sort(S).map(row)]),'Не сверены');
 XLSX.utils.book_append_sheet(wb,XLSX.utils.aoa_to_sheet([['Все сверенные'],H,...E.filter(p=>p.vf).sort(S).map(row)]),'Сверенные');
 XLSX.writeFile(wb,'Сверка котлованов '+vfToday()+'.xlsx')}
"""
R("function vis(p){return ftyOk(p)&&visB(p)&&(!NB||nbOk(p))&&(!GY||gyOk(p))&&(!NK||nkOk(p))}",
  JS + "function vis(p){return ftyOk(p)&&visB(p)&&(!NB||nbOk(p))&&(!GY||gyOk(p))&&(!NK||nkOk(p))&&(!VS||vsOk(p))}")

R("{const _st=stats;stats=function(){const r=_st.apply(this,arguments);try{nbUI();gyUI();nkUI()}catch(e){}return r}}",
  "{const _st=stats;stats=function(){const r=_st.apply(this,arguments);try{nbUI();gyUI();nkUI();vfUI()}catch(e){}return r}}\n"
  "$('vfb').onclick=()=>{VS=!VS;try{localStorage.setItem(KEY+'_vs',VS?'1':'0')}catch(e){}vfUI();P.forEach(upd);numLabels();"
  "if(VS){const L2=P.filter(p=>vsOk(p)&&tpOk(p));if(L2.length)map.fitBounds(L.latLngBounds(L2.map(p=>[p.lat,p.lon])).pad(.15),{maxZoom:18});else toast('Все забуренные котлованы сверены')}};"
  "$('vfx').onclick=vfXl;setTimeout(vfUI,0);")

# --- значок: кольцо сверки
R('style="overflow:visible">${ready(p)?', 'style="overflow:visible">${vfRing(p)}${ready(p)?')

# --- окно опоры (редактор)
R("""<input type=checkbox data-vk ${p.vk?'checked':''}> <b style="color:#e879f9">ввод КЛ</b></label></div></div>""",
  """<input type=checkbox data-vk ${p.vk?'checked':''}> <b style="color:#e879f9">ввод КЛ</b></label></div></div>${vfH(p)}""")
R("{const e=d.querySelector('[data-od]');if(e)e.onchange=",
  "{const b=d.querySelector('[data-vfb]');if(b)vfDraw(b,p)}\n{const e=d.querySelector('[data-od]');if(e)e.onchange=")
# --- просмотр
R("${odTxt(p)}", "${odTxt(p)}${vfTxt(p)}")

open(path, 'w', encoding='utf-8').write(s); print('ok', path)
