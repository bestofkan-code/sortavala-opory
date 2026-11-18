#!/usr/bin/env python3
"""«История» в окне опоры больше не закрывает окно: история опоры раскрывается прямо в окне
(последние 40 изменений: дата, кто, что). «Вся история в панели» — прежний просмотр в панели
(если панель скрыта кнопкой «Скрыть таблицы/панель», она показывается).
  for f in redaktor.html prosmotr.html zamechaniya.html zamechaniya-prosmotr.html montazh.html uchastki.html; do python3 tools/patch_hinline.py $f; done
"""
import sys
path = sys.argv[1]
s = open(path, encoding='utf-8').read()
if 'HINLINE' in s:
    print('already applied', path); sys.exit(0)
n = s.count("d.querySelector('[data-h]').onclick=()=>hpole(p);")
assert n >= 1, path
s = s.replace("d.querySelector('[data-h]').onclick=()=>hpole(p);", "d.querySelector('[data-h]').onclick=e=>hInline(d,p,e.currentTarget);")
JS = r"""
/*HINLINE*/function hInline(d,p,btn){let x=d.querySelector('.hin');const t0=btn.dataset.t0||btn.textContent;btn.dataset.t0=t0;
 const up=()=>setTimeout(()=>{const pp=map._popup;if(pp&&pp.isOpen&&pp.isOpen()&&!pp.getElement().classList.contains('side')&&!pp.getElement().classList.contains('sheet'))pp.update()},0);
 if(x){x.remove();btn.textContent=t0;up();return}
 x=document.createElement('div');x.className='hin';x.innerHTML='<small>Загрузка истории…</small>';const br=d.querySelector('.brow');if(br)br.before(x);else btn.after(x);btn.textContent='Скрыть историю';up();
 const fin=html=>{x.innerHTML=html+'<button type=button class="hfull">Вся история в панели</button>';x.querySelector('.hfull').onclick=()=>{if(document.body.classList.contains('mfull')){const m=document.querySelector('.mfb');if(m)m.click()}setTimeout(()=>hpole(p),80)};up()};
 if(!CF){fin('<small>Онлайн-база не подключена.</small>');return}
 fetch(CF.u+'/rest/v1/history?select=*&uid=eq.'+encodeURIComponent(p.uid)+'&order=id.desc&limit=40',{headers:H()}).then(r=>r.json()).then(a=>{if(!Array.isArray(a))throw JSON.stringify(a);
  fin(a.length?a.map(h=>{const t=new Date(h.ts).toLocaleString('ru-RU',{day:'2-digit',month:'2-digit',year:'2-digit',hour:'2-digit',minute:'2-digit'}).replace(',','');let ds='';try{ds=hdesc(h)}catch(e){ds=h.op}
   return '<div class="hir"><small>'+t+(h.ed?' · '+esc(h.ed):'')+'</small><div>'+esc(ds||'изменение')+'</div></div>'}).join(''):'<small>Изменений пока нет.</small>')}).catch(e=>fin('<small>Не удалось загрузить историю: '+esc(String(e)).slice(0,120)+'</small>'))}
{const st=document.createElement('style');st.textContent='.pp .hin{margin:5px 0 0;padding:4px 6px;border:1px solid #374151;border-radius:7px;max-height:220px;overflow-y:auto;font-size:11.5px;line-height:1.3}.pp .hin .hir{padding:3px 0;border-bottom:1px solid rgba(127,127,127,.2)}.pp .hin .hir:last-of-type{border-bottom:0}.pp .hin small{color:#9aa3b5;font-size:10.5px}.pp .hin .hfull{width:100%;height:26px;margin-top:4px;font-size:11px}';document.head.appendChild(st)}
"""
i = s.index("const map=L.map('m',"); j = s.index(';', s.index('.setView(', i)) + 1
s = s[:j] + JS + s[j:]
open(path, 'w', encoding='utf-8').write(s); print('ok', path, n)
