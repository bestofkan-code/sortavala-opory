# 1) Поиск опоры / ТП: кнопка-лупа под «СП» (слева), аккуратная панель: «97-3», «ТП29 36», «шд 8», «ктп 163-5», «97» (вся ТП).
#    Выбор — карта приближается, опора подсвечивается и открывается её окно; ТП — показывается вся ТП.
# 2) При открытии карты все разделы боковой панели свёрнуты (план работ, склад, материалы, контракт, проверки…).
import sys
p=sys.argv[1];s=open(p,encoding='utf-8').read()
def R(a,b,n=1):
    global s
    assert s.count(a)==n,(a[:90],s.count(a));s=s.replace(a,b)
# --- свернуть разделы
R('<details id="pld" open>','<details id="pld">')
R('<details id="skd" open>','<details id="skd">')
R('<details id="ktd" open>','<details id="ktd">')
R('<details id="matd" open>','<details id="matd">')
R("try{if(localStorage.getItem(KEY+'_kc')==='1')$('kcd').open=true}catch(e){}","")
R("try{if(localStorage.getItem(KEY+'_fd')==='1')$('fdd').open=true}catch(e){}","")
# --- поиск
A="toast(RLON?'Линии совместной подвески показаны':'Линии совместной подвески скрыты — красные точки у опор остаются')};return d}});new C().addTo(map)}"
JS=r"""
/* ---- поиск опоры / ТП ---- */
{document.head.insertAdjacentHTML('beforeend','<style>.srw{position:relative}.srp{position:absolute;left:40px;top:0;width:290px;max-width:calc(100vw - 70px);background:#161a24;color:#eef1f7;border:1px solid #2c3346;border-radius:12px;box-shadow:0 10px 28px rgba(0,0,0,.45);padding:8px;font:13px Commissioner,system-ui,sans-serif;z-index:1000}.srp input{width:100%;box-sizing:border-box;background:#0f1218;color:#eef1f7;border:1px solid #39415a;border-radius:8px;padding:8px 10px;font:14px Commissioner,system-ui,sans-serif;outline:none}.srp input:focus{border-color:#4f7cff}.srl{max-height:300px;overflow:auto;margin-top:6px}.sri{display:flex;align-items:center;gap:8px;padding:7px 8px;border-radius:8px;cursor:pointer}.sri:hover,.sri.on{background:#232a3b}.sri i{width:10px;height:10px;border-radius:50%;flex:none}.sri b{font-weight:600}.sri small{margin-left:auto;color:#9aa3b5;white-space:nowrap}.srh{color:#9aa3b5;font-size:11px;padding:4px 2px 0}</style>');
 const nz=x=>String(x||'').toLowerCase().replace(/ё/g,'е').replace(/шуно\s*дорожная/g,'шд').replace(/ктп\s*/g,'ктп').replace(/тп\s*№?\s*/g,'').replace(/№/g,'').replace(/[\s\/_.]+/g,'-').replace(/-+/g,'-').replace(/^-|-$/g,'');
 const C=L.Control.extend({options:{position:'topleft'},onAdd(){const d=L.DomUtil.create('div','leaflet-bar srw');d.innerHTML='<a href="#" title="Найти опору или ТП" style="display:flex;align-items:center;justify-content:center"><svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round"><circle cx="10.5" cy="10.5" r="6.5"/><path d="M15.5 15.5L21 21"/></svg></a><div class="srp" hidden><input type="search" placeholder="Опора или ТП: 97-3, 29 36, шд 8" autocomplete="off" enterkeyhint="search"><div class="srl"></div><div class="srh">Номер опоры через дефис или пробел. Только номер ТП — покажу всю ТП.</div></div>';
  L.DomEvent.disableClickPropagation(d);L.DomEvent.disableScrollPropagation(d);const a=d.querySelector('a'),pn=d.querySelector('.srp'),inp=pn.querySelector('input'),ls=pn.querySelector('.srl');let R0=[],sel=0;
  const close=()=>{pn.hidden=true};a.onclick=e=>{e.preventDefault();pn.hidden=!pn.hidden;if(!pn.hidden){inp.focus();inp.select();run()}};
  document.addEventListener('click',e=>{if(!pn.hidden&&!d.contains(e.target))close()});
  const flash=ll=>{const c=L.circleMarker(ll,{radius:26,color:'#facc15',weight:4,fill:false,interactive:false}).addTo(map);let k=0;const t=setInterval(()=>{k++;c.setStyle({opacity:k%2?.25:1});if(k>7){clearInterval(t);map.removeLayer(c)}},350)};
  const go=r=>{if(!r)return;close();if(r.t){const ps=P.filter(q=>String(q.tp||'')==r.t&&!q.x);if(ps.length)map.fitBounds(L.latLngBounds(ps.map(q=>[q.lat,q.lon])).pad(.12),{maxZoom:18});toast(tpn(r.t)+': опор '+ps.length);return}
   const q=r.p,ll=[q.lat,q.lon];map.setView(ll,Math.max(map.getZoom(),18.5));flash(ll);const m=mk.get(q);
   setTimeout(()=>{if(m&&map.hasLayer(m)&&(typeof mode=='undefined'||mode=='view'))m.fire('click');else if(m&&!map.hasLayer(m))toast(q.id+' скрыта фильтром — показал место на карте')},450)};
  const run=()=>{const v=nz(inp.value);R0=[];if(v){const tps=tpList(),tq=tps.filter(t=>{const z=nz(tpn(t)),z2=nz(t);return z==v||z2==v||(v.length>=2&&(z.startsWith(v)||z2.startsWith(v)))});
    tq.slice(0,3).forEach(t=>R0.push({t,s:-1}));const sc=q=>{const z=nz(q.id);if(z==v)return 0;if(z.startsWith(v+'-'))return 1;if(z.startsWith(v))return 2;if(z.includes(v))return 3;return 9};
    P.map(q=>[q,sc(q)]).filter(x=>x[1]<9).sort((x,y)=>x[1]-y[1]||String(x[0].id).localeCompare(String(y[0].id),'ru',{numeric:true})).slice(0,40).forEach(([q,k])=>R0.push({p:q,s:k}));
    if(R0.length>1&&R0[0].t&&R0.some(r=>r.p&&r.s==0))R0.sort((x,y)=>x.s-y.s)}sel=0;
   ls.innerHTML=!v?'':(R0.length?R0.map((r,i)=>r.t?'<div class="sri'+(i==sel?' on':'')+'" data-i="'+i+'"><i style="background:'+tpCol(r.t)+';border-radius:3px"></i><b>'+esc(SHD(tpn(r.t)))+'</b><small>вся ТП · '+P.filter(q=>String(q.tp||'')==r.t&&!q.x).length+' оп.</small></div>':'<div class="sri'+(i==sel?' on':'')+'" data-i="'+i+'"><i style="background:'+tpCol(r.p.tp)+'"></i><b>'+esc(SHD(r.p.id))+'</b><small>'+(r.p.x?'исключена':r.p.done?'установлена':'не установлена')+'</small></div>').join(''):'<div class="srh">Ничего не нашёл</div>');
   ls.querySelectorAll('[data-i]').forEach(e=>e.onclick=()=>go(R0[+e.dataset.i]))};
  inp.oninput=run;inp.onkeydown=e=>{if(e.key=='Enter'){e.preventDefault();go(R0[sel])}else if(e.key=='Escape')close();else if(e.key=='ArrowDown'||e.key=='ArrowUp'){e.preventDefault();if(!R0.length)return;sel=(sel+(e.key=='ArrowDown'?1:-1)+R0.length)%R0.length;ls.querySelectorAll('.sri').forEach((x,i)=>x.classList.toggle('on',i==sel));const o=ls.querySelector('.sri.on');if(o)o.scrollIntoView({block:'nearest'})}};
  return d}});new C().addTo(map)}
"""
R(A,A+JS)
open(p,'w',encoding='utf-8').write(s);print('ok search',p)
