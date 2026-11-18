#!/usr/bin/env python3
"""Окно опоры — быстрый набор, узкое вертикальное (после patch_card2.py / patch_card2b.py).

Сверху (всё одним нажатием):
  Тип опоры: Стандартная / Анкерная (= тип закладной ЗФ-24/8 / ЗФ-30/8)
  Кронштейн: нет / 1-р / 90° / 180°
  Старая опора: нет / демонт. / остаётся
  Отметки: Опора (работа 4), Светильник (6), СИП (5), Совм. подв., Заземл.
  Светильников ставится автоматически по кронштейну: нет — 0, 1-р — 1, 90° и 180° — 2.
  Сверка (строка из patch_card2), ⧉ в заголовке — скопировать координаты.
Ниже: «Все работы N/14» (все плитки работ, даты, фото, комментарий/примечание), «История», «Ещё»
(высота, фундамент, кронштейн/светильники вручную, ТП, №, адрес, исключение и т. д.).
Ширина окна 212 px. На телефоне — панель справа поверх карты (карта слева видна), карта сдвигается,
чтобы опора была в видимой части. Просмотр и монтажная карта — как были.
  for f in redaktor.html zamechaniya.html uchastki.html; do python3 tools/patch_card3.py $f; done
"""
import sys
path = sys.argv[1]
s = open(path, encoding='utf-8').read()
if 'CARD3' in s:
    print('already applied', path); sys.exit(0)
def R(old, new, cnt=1):
    global s
    n = s.count(old); assert n == cnt, (path, old[:90], n); s = s.replace(old, new)

R(";cmpCard(d,p);return d}", ";cmpCard(d,p);qkCard(d,p);return d}")
R("minWidth:250", "minWidth:200")
R("el.classList.add('sheet');", "const SD=!!el.querySelector('.qk');el.classList.add(SD?'side':'sheet');if(SD)sdPos(el);")
R("if(w&&!el.querySelector('.shh'))", "if(!SD&&w&&!el.querySelector('.shh'))")
R("setTimeout(()=>shPan(e.popup,el),30)", "setTimeout(()=>SD?sdPan(e.popup,el):shPan(e.popup,el),30)")

JS = r"""
/*CARD3*/function svFor(p){const k=krv(p);return k=='0'?0:k=='1'?1:2}
function sdPos(el){const c=map.getContainer().getBoundingClientRect(),t=Math.max(8,Math.round(c.top+8));el.style.setProperty('--sdt',t+'px');el.style.setProperty('--sdh',Math.max(300,innerHeight-t-8)+'px')}
function sdPan(pp,el){const ll=pp.getLatLng&&pp.getLatLng();if(!ll)return;const c=map.getContainer().getBoundingClientRect(),r=el.getBoundingClientRect(),vw=Math.max(80,r.left-c.left),vb=Math.min(c.height,innerHeight-c.top),pt=map.latLngToContainerPoint(ll);if(pt.x>vw-20||pt.x<20||pt.y<30||pt.y>vb-30)map.panBy([pt.x-vw/2,pt.y-Math.min(c.height,vb)/2],{animate:true})}
function qkCard(d,p){const id=d.firstElementChild;if(!id)return;const q=document.createElement('div');q.className='qk';id.after(q);d.classList.add('qkm');
 if(p.lat!=null)id.insertAdjacentHTML('beforeend',` <button type=button class="qc" data-yco="${ycoS(p)}" title="Скопировать координаты для Яндекс Карт">⧉</button>`);
 const mb=d.querySelector('[data-mb]'),g=d.querySelector('.g3p'),ps=d.querySelector('.psum'),sq=d.querySelector('[data-sq]');if(ps)ps.remove();if(mb&&g){g.hidden=false;mb.prepend(g)}if(mb&&sq)mb.appendChild(sq);
 const brow=d.querySelector('.brow'),ws=document.createElement('div');ws.className='wsec';ws.hidden=true;['.wh','[data-wg]','[data-wde]','[data-phb]','[data-phb2]','[data-arb]','.g2i'].forEach(x=>{const e=d.querySelector(x);if(e)ws.appendChild(e)});brow.before(ws);
 const wb=document.createElement('button');wb.type='button';wb.className='qw';brow.prepend(wb);const wbT=()=>{wb.textContent=(ws.hidden?'Работы ':'Скрыть ')+WK.filter(([k])=>wdone(p,k)).length+'/'+WK.length};wbT();const up=()=>setTimeout(()=>{const pp=map._popup;if(pp&&pp.isOpen&&pp.isOpen()&&!pp.getElement().classList.contains('side'))pp.update()},0);wb.onclick=()=>{ws.hidden=!ws.hidden;wbT();up()};{const mo=d.querySelector('[data-more]');if(mo)mo.addEventListener('click',up)}
 const dm=v=>/^\d{4}-/.test(v||'')?v.slice(8,10)+'.'+v.slice(5,7):'';
 const seg=(lab,key,o,cur)=>`<div class="ql">${lab}</div><div class="qs" data-q="${key}">${o.map(([v,t])=>`<button type=button data-v="${v}"${cur==v?' class="on"':''}>${t}</button>`).join('')}</div>`;
 const tg=(key,lab,on,sub)=>`<button type=button class="qt${on?' on':''}" data-q="${key}"><span>${on?'✓ ':''}${lab}</span>${sub?`<small>${sub}</small>`:''}</button>`;
 const sync=()=>{const v=(x,val)=>{const e=d.querySelector(x);if(e)e.value=val},c=(x,val)=>{const e=d.querySelector(x);if(e)e.checked=val};v('[data-k=t]',p.t=='A'?'A':'S');const kr=d.querySelector('[data-kr]');if(kr&&krv(p)!='2')kr.value=krv(p);v('[data-sv]',+p.sv||0);const od=d.querySelector('[data-od]');if(od){od.value=p.od||'';od.className='od-'+(p.od||'n')}c('[data-k=g]',!!p.g);c('[data-k=js]',!!p.js);const h=d.querySelector('[data-hs]');if(h)h.textContent='лин. '+(p.line||'-')+' · '+(p.t=='A'?'анкер.':'станд.')+' · '+(+p.h||8)+' м'};
 const draw=()=>{const sv=+p.sv||0;q.innerHTML=seg('Тип опоры','t',[['S','Стандартная'],['A','Анкерная']],p.t=='A'?'A':'S')+seg('Кронштейн','kr',[['0','нет'],['1','1-р'],['2-90','90°'],['2-180','180°']],krv(p))+seg('Старая опора','od',[['','нет'],['d','демонт.'],['k','остаётся']],p.od||'')
  +`<div class="qg">${tg('w4','Опора',wdone(p,4),dm(wd(p,4)))}${tg('w6','Светильник',wdone(p,6),wdone(p,6)?'×'+sv:'')}${tg('w5','СИП',wdone(p,5),dm(wd(p,5)))}${tg('js','Совм. подв.',!!p.js)}${tg('g','Заземл.',!!p.g)}</div>`};
 const after=()=>setTimeout(()=>{draw();sync();if(d._rw)d._rw();wbT()},0);
 q.onclick=e=>{const b=e.target.closest&&e.target.closest('button');if(!b||!q.contains(b))return;PSEL=Date.now();const qs=b.closest('[data-q]'),key=qs.dataset.q,v=b.dataset.v,dt=$('md').value||LD();
  if(key=='t')p.t=v;
  else if(key=='kr'){const[a,c]=v.split('-');p.kr=+a;p.ka=c?+c:null;if(wdone(p,6))p.sv=svFor(p)||1;try{kcOver(p)}catch(er){}}
  else if(key=='od')p.od=v;
  else if(key=='js'){p.js=!p.js;lines()}
  else if(key=='g')p.g=!p.g;
  else if(key[0]=='w'){const n=+key.slice(1),on=!wdone(p,n);setW(p,n,on,dt);if(n==6&&on)p.sv=svFor(p)||1}
  upd(p);save();stats();mark(p);after()};
 d.addEventListener('change',e=>{if(!q.contains(e.target))after()});ws.addEventListener('click',()=>setTimeout(()=>{draw();wbT()},30));
 draw()}
{const st=document.createElement('style');st.textContent=`.pp.qkm,.pp.qkm.cw,.pp.fix.qkm{width:212px!important}
.qkm .pph b{font-size:13px}.qkm [data-hs]{display:none}.qkm .pph>div:first-child{padding-right:22px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}.qkm .qc{height:22px;min-width:24px;padding:0 5px;font-size:12px;margin-left:4px;vertical-align:1px}
.qk{margin:2px 0 0}.qk .ql{font-size:11px;color:#9aa3b5;margin:4px 0 1px}
.qk .qs{display:flex;border:1px solid #475569;border-radius:6px;overflow:hidden}.qk .qs button{flex:1;min-width:0;height:26px;padding:0 1px;margin:0;font-size:11px;border:0;border-left:1px solid #334155;border-radius:0;background:transparent;color:inherit;white-space:nowrap}.qk .qs button:first-child{border-left:0}
.qk .qs button.on{background:#1d4ed8;color:#fff;font-weight:600}
.qk .qg{display:grid;grid-template-columns:1fr 1fr;gap:3px;margin-top:6px}.qk .qt{display:flex;align-items:center;justify-content:space-between;gap:2px;height:28px;margin:0;padding:0 5px;font-size:11px;border-radius:6px;text-align:left;white-space:nowrap;overflow:hidden}
.qk .qt.on{background:rgba(22,163,74,.22);border-color:#16a34a;color:#86efac;font-weight:600}.qk .qt small{font-size:10px;opacity:.85;font-weight:400}
.qkm .vfb{margin:6px 0 0!important}.qkm .vfn{display:none}.qkm .vfl{gap:3px}.qkm .vfl button{height:26px;padding:0 6px;font-size:11px}.qkm .vfl .vfy{flex:1}.qkm .vfl .vfs{font-size:11px}
.qkm .wsec{margin-top:5px}.pp.qkm .wg{grid-template-columns:repeat(2,minmax(0,1fr))!important}.qkm .g2i{display:flex;flex-direction:column;gap:3px}
.qkm .brow{display:grid;grid-template-columns:1fr auto auto;gap:3px;margin-top:6px}.qkm .brow button{height:26px;padding:0 6px;font-size:11px;margin:0}
.qkm .more .g3p{grid-template-columns:1fr 1fr}
.leaflet-popup.side{position:fixed!important;right:6px!important;left:auto!important;top:var(--sdt,70px)!important;bottom:auto!important;transform:none!important;margin:0!important;z-index:1500;transition:none!important}
.leaflet-popup.side .leaflet-popup-tip-container{display:none}.leaflet-popup.side .leaflet-popup-content-wrapper{box-shadow:0 4px 18px rgba(0,0,0,.45)}
.leaflet-popup.side .leaflet-popup-content{max-height:var(--sdh,70vh)!important;height:auto!important;overflow-y:auto!important;overscroll-behavior:contain;margin:8px!important;width:auto!important}`;document.head.appendChild(st)}
"""
i = s.index("const map=L.map('m',"); j = s.index(';', s.index('.setView(', i)) + 1
s = s[:j] + JS + s[j:]
open(path, 'w', encoding='utf-8').write(s); print('ok', path)
