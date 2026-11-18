#!/usr/bin/env python3
"""Окно опоры компактнее (после patch_vf.py и patch_nozoom.py).

1. Параметры опоры (тип, высота, фундамент, кронштейн, светильники, старая опора, заземл./совм./ввод КЛ)
   свёрнуты в строку-сводку; ✎ — раскрыть для правки (запоминается). Если у кронштейна не указан угол — блок открыт.
2. Сверка на месте — одна строка: «✓ Всё верно», «📍 GPS», «≠» (другая закладная, комментарий).
   После сверки — строка «✓ Сверено 18.11 · ЗФ-24/8 · кто», ✎ — подробности, «Снять сверку».
3. Работы: показаны выполненные и те, что относятся к опоре (закладная: котлован, закладная, бетон;
   гравит.: грав. фундамент; опора, кронштейн, СИП, светильник; котл. заземл. — если заземление;
   демонтаж старой — если «демонтир.»). Остальные — под «Ещё работы (N)». Подсказка под заголовком убрана.
   Координаты, «Копировать», «Яндекс» — в меню «Ещё».
4. Телефон (ширина < 700 px): окно опоры — панель снизу во всю ширину. Полоска сверху: нажать или
   потянуть вверх — панель выше, потянуть вниз — ниже / закрыть. Карта сдвигается, чтобы опора была видна над панелью.
  for f in redaktor.html prosmotr.html zamechaniya.html zamechaniya-prosmotr.html montazh.html uchastki.html; do python3 tools/patch_card2.py $f; done
"""
import sys
path = sys.argv[1]
s = open(path, encoding='utf-8').read()
if 'CARD2' in s:
    print('already applied', path); sys.exit(0)
def R(old, new, cnt=1):
    global s
    n = s.count(old); assert n == cnt, (path, old[:90], n); s = s.replace(old, new)

# --- работы: фильтр и «Ещё работы»
R("const rw=()=>{const g=d.querySelector('[data-wg]');g.innerHTML=WK.map(",
  "let WALL=false;const rw=()=>{const g=d.querySelector('[data-wg]');const WV=WK.filter(([k])=>WALL||wShow(p,k)),WH=WK.filter(([k])=>!wShow(p,k)).length;g.innerHTML=WV.map(")
R("${ppN(p.uid,k)||''}</button>`:''}${on?`<button class=\"wdt\" data-wd=${k} title=\"Изменить дату\">${dd}</button>`:''}</div>`}).join('');\n d.querySelector('[data-wn]')",
  "${ppN(p.uid,k)||''}</button>`:''}${on?`<button class=\"wdt\" data-wd=${k} title=\"Изменить дату\">${dd}</button>`:''}</div>`}).join('')+(WH?`<button type=button class=\"wall\" data-wall>${WALL?'Скрыть лишние ▴':'Ещё работы ('+WH+') ▾'}</button>`:'');{const wa=g.querySelector('[data-wall]');if(wa)wa.onclick=()=>{WALL=!WALL;rw()}}\n d.querySelector('[data-wn]')")
R("\nrw();\nd.querySelector('[data-more]')", "\nrw();d._rw=rw;\nd.querySelector('[data-more]')")
R(";return d}\nvar FTS=", ";cmpCard(d,p);return d}\nvar FTS=")

# --- сверка: новая компактная отрисовка
a = s.index('function vfDraw(b,p){'); b = s.index('\nvar VS=false', a)
VFD = r"""function vfDraw(b,p){const v=p.vf,bad=vfBad(p),op=!!b._op,ex=vfExp(p),cz=(v&&v.z)||ex;b.className='vfb'+(v?(bad?' bad':' ok'):'');
 const dm=x=>/^\d{4}-/.test(x||'')?x.slice(8,10)+'.'+x.slice(5,7):(x||'');
 const det=`<div class="vfd"><label>Закладная факт.<select data-vz>${['24','30'].map(z=>`<option value="${z}" ${cz==z?'selected':''}>${VFZ[z]}${z==ex?' — по типу':''}</option>`).join('')}</select></label><input type=text data-vc placeholder="Комментарий к сверке" value="${esc((v&&v.c)||'')}"><div class="vfr">${v?'<button type=button data-vg>📍 Точка по GPS</button><button type=button data-vun>Снять сверку</button>':'<button type=button data-vy class="vfy">✓ Сохранить сверку</button>'}</div></div>`;
 b.innerHTML=v?`<div class="vfl"><span class="vfs">✓ Сверено ${dm(v.d)} · ${VFS[cz]}${v.e?' · '+esc(v.e):''}${v.mv?' · перенос '+v.mv+' м':''}${bad?' · <b>'+bad+'</b>':''}${v.c?' · '+esc(v.c):''}</span><button type=button data-vt>${op?'▴':'✎'}</button></div>${op?det:''}`
 :`<div class="vfl"><span class="vfn">Сверка</span><button type=button data-vy class="vfy">✓ Всё верно</button><button type=button data-vg>📍 GPS</button><button type=button data-vt title="Другая закладная или комментарий">${op?'▴':'≠'}</button></div>${op?det:''}`;
 const ch=()=>{upd(p);save();stats();mark(p);vfDraw(b,p)},q=x=>b.querySelector(x),zv=()=>{const e=q('[data-vz]');return e?e.value:cz};
 q('[data-vt]').onclick=()=>{b._op=!op;vfDraw(b,p)};
 b.querySelectorAll('[data-vy]').forEach(e=>e.onclick=()=>{const c=q('[data-vc]');vfSet(p,{z:zv(),c:c?c.value.trim():((v&&v.c)||'')});b._op=false;ch();if(vfBad(p))toast(p.id+': '+vfBad(p))});
 if(v){if(q('[data-vz]'))q('[data-vz]').onchange=e=>{vfSet(p,{z:e.target.value});ch();if(vfBad(p))toast(p.id+': '+vfBad(p))};
  if(q('[data-vc]'))q('[data-vc]').onchange=e=>{vfSet(p,{c:e.target.value.trim()});ch()};
  if(q('[data-vun]'))q('[data-vun]').onclick=()=>{if(p.vf&&p.vf.mv&&!confirm('Снять сверку? Опора останется в новой точке (старая — в истории опоры).'))return;p.vf=null;b._op=false;ch()}}
 const gb=q('[data-vg]');if(gb)gb.onclick=e=>{if(!navigator.geolocation)return alert('Геолокация недоступна на этом устройстве');const bt=e.target,t0=bt.textContent;bt.disabled=true;bt.textContent='Определяю…';
  navigator.geolocation.getCurrentPosition(g=>{bt.disabled=false;bt.textContent=t0;const c=L.latLng(g.coords.latitude,g.coords.longitude),a=Math.round(g.coords.accuracy||0),dd=Math.round(map.distance([p.lat,p.lon],c));
   if(a>25&&!confirm('Точность GPS сейчас плохая: ±'+a+' м. Лучше подождать на открытом месте и нажать ещё раз. Всё равно перенести?'))return;
   if(!confirm('Перенести опору '+p.id+' на '+dd+' м в точку, где вы стоите (точность ±'+a+' м)?'))return;
   const o=(p.vf&&p.vf.o)||[p.lat,p.lon];p.lat=c.lat;p.lon=c.lng;vfSet(p,{o,mv:Math.round(map.distance(o,c)),z:zv()});const m=mk.get(p);if(m)m.setLatLng(c);lines();ch();toast(p.id+' перенесена на '+dd+' м и отмечена как сверенная')},
   er=>{bt.disabled=false;bt.textContent=t0;alert('Не удалось определить место: '+(er.code==1?'нет разрешения на геолокацию в браузере':er.message))},{enableHighAccuracy:true,timeout:20000,maximumAge:0})}}"""
s = s[:a] + VFD + s[b:]

JS = r"""
/*CARD2*/function wShow(p,k){if(wdone(p,k))return true;const G=isG(p);switch(k){case 1:case 2:case 3:return !G;case 10:return G;case 11:return !!p.g;case 4:case 12:case 5:case 6:return true;case 8:return p.od=='d';default:return false}}
function cmpCard(d,p){const g=d.querySelector('.g3p');
 if(g){const sm=document.createElement('div');sm.className='psum';g.before(sm);let op=false;try{op=localStorage.getItem(KEY+'_pexp')==='1'}catch(e){}
  const draw=()=>{const kr=krv(p),kt=kr=='0'?'без кроншт.':kr=='2'?'2-р: угол?':((KRO.find(x=>x[0]==kr)||[0,kr])[1]),need=kr=='2';
   const a=[p.t=='A'?'анкер.':'станд.',(+p.h||8)+' м',isG(p)?'гравит.':'закладная',need?'<b style="color:#f59e0b">'+kt+'</b>':kt,(+p.sv||0)+' св.'];
   if(p.od)a.push(p.od=='d'?'<span style="color:#f87171">ст. опора: демонт.</span>':'<span style="color:#4ade80">ст. опора: ост.</span>');
   if(p.g)a.push('заземл.');if(p.js)a.push('<b style="color:#f87171">совм.</b>');if(p.vk)a.push('<b style="color:#e879f9">ввод КЛ</b>');
   sm.innerHTML=`<span class="pst">${a.join(' · ')}</span><button type=button data-pe title="${op?'Свернуть':'Изменить параметры опоры'}">${op?'▴':'✎'}</button>`;g.hidden=!op&&!need;
   sm.onclick=()=>{op=!op;try{localStorage.setItem(KEY+'_pexp',op?'1':'0')}catch(e){}draw()}};
  draw();g.addEventListener('change',()=>setTimeout(()=>{draw();if(d._rw)d._rw()},0))}
 const y=d.querySelector('.yco'),mb=d.querySelector('[data-mb]');if(y&&mb)mb.prepend(y);
 const h=d.querySelector('.wh span:last-child');if(h)h.remove()}
{const st=document.createElement('style');st.textContent=`#shhost{position:fixed!important;left:0;right:0;bottom:0;height:0;overflow:visible!important;background:none!important;outline:none;z-index:1500}.pp .g3p[hidden]{display:none!important}.psum{display:flex;align-items:center;gap:6px;margin:4px 0;padding:4px 6px;border:1px solid #374151;border-radius:7px;cursor:pointer;font-size:12px;line-height:1.3}.psum .pst{flex:1;min-width:0}.psum button{flex:none;padding:2px 9px;height:26px}
.pp .wg{grid-template-columns:repeat(3,minmax(0,1fr))!important}.pp .wg .wall{grid-column:1/-1;height:26px;font-size:11.5px;opacity:.85}
.vfb{padding:4px 6px!important;margin:4px 0!important}.vfl{display:flex;align-items:center;gap:5px;flex-wrap:wrap}.vfl .vfn{font-weight:700;font-size:12px;margin-right:2px}.vfl .vfs{flex:1;min-width:0;font-size:12px}.vfl button{height:28px;padding:2px 9px;font-size:12px}.vfl .vfy{background:#16a34a;color:#fff;border-color:#15803d;font-weight:600}
.vfd{margin-top:5px;display:flex;flex-direction:column;gap:4px}.vfd label{display:flex;flex-direction:column;font-size:11px}.vfd .vfr{margin:0}
.leaflet-popup.sheet{position:fixed!important;left:0!important;right:0!important;bottom:0!important;top:auto!important;transform:none!important;margin:0!important;z-index:1500;transition:none!important;display:flex!important;flex-direction:column;padding:0!important}
.leaflet-popup.sheet .leaflet-popup-content-wrapper{flex:1}
.leaflet-popup.sheet .leaflet-popup-tip-container{display:none}
.leaflet-popup.sheet .leaflet-popup-content-wrapper{border-radius:14px 14px 0 0;padding:0 0 env(safe-area-inset-bottom);box-shadow:0 -6px 24px rgba(0,0,0,.45)}
.leaflet-popup.sheet .leaflet-popup-content{width:auto!important;margin:0 12px 10px!important;max-height:var(--shh,52vh)!important;height:auto!important;overflow-y:auto!important;overscroll-behavior:contain}
.leaflet-popup.sheet.full .leaflet-popup-content{--shh:86vh}.leaflet-popup.sheet .pp.fix{width:auto!important;max-width:none!important}
.leaflet-popup.sheet .shh{height:22px;display:flex;align-items:center;justify-content:center;touch-action:none;cursor:grab}.leaflet-popup.sheet .shh i{width:42px;height:5px;border-radius:3px;background:#6b7280}
.leaflet-popup.sheet .leaflet-popup-close-button{top:2px!important;right:6px!important;width:34px!important;height:30px!important;font-size:24px!important;z-index:2}`;document.head.appendChild(st)}
const SHEET=()=>innerWidth<700;
function shPan(pp,el){const ll=pp.getLatLng&&pp.getLatLng();if(!ll)return;const c=map.getContainer().getBoundingClientRect(),t=el.getBoundingClientRect().top,vb=Math.min(c.bottom,t)-c.top,pt=map.latLngToContainerPoint(ll);if(vb<60)return;const ty=Math.max(40,vb*.45);if(pt.y<30||pt.y>vb-30||pt.x<20||pt.x>c.width-20)map.panBy([pt.x-c.width/2,pt.y-ty],{animate:true})}
map.on('popupopen',e=>{if(!SHEET())return;const el=e.popup.getElement();if(!el||!el.querySelector('.pp[data-uid]'))return;el.classList.add('sheet');let hs=document.getElementById('shhost');if(!hs){hs=document.createElement('div');hs.id='shhost';hs.className='leaflet-container';document.body.appendChild(hs)}hs.appendChild(el);
 const w=el.querySelector('.leaflet-popup-content-wrapper');if(w&&!el.querySelector('.shh')){const hd=document.createElement('div');hd.className='shh';hd.innerHTML='<i></i>';w.prepend(hd);
  let y0=null;const tog=f=>{el.classList.toggle('full',f)};hd.onclick=()=>tog(!el.classList.contains('full'));
  hd.addEventListener('touchstart',ev=>{y0=ev.touches[0].clientY},{passive:true});
  hd.addEventListener('touchend',ev=>{if(y0==null)return;const dy=ev.changedTouches[0].clientY-y0;y0=null;if(dy<-25)tog(true);else if(dy>25){if(el.classList.contains('full'))tog(false);else map.closePopup()}},{passive:true})}
 setTimeout(()=>shPan(e.popup,el),30)});
addEventListener('resize',()=>{const el=document.querySelector('.leaflet-popup.sheet');if(el&&!SHEET())map.closePopup()});
"""
R("const map=L.map('m',", "const map=L.map('m',")  # sanity
i = s.index("const map=L.map('m',"); j = s.index(';', s.index('.setView(', i)) + 1
s = s[:j] + JS + s[j:]
# телефон: не двигать карту под всплывающее окно — панель снизу
R("autoPanPadding:[10,10],offset:L.point(0,-12)});", "autoPan:innerWidth>=700,autoPanPadding:[10,10],offset:L.point(0,-12)});")
open(path, 'w', encoding='utf-8').write(s); print('ok', path)
