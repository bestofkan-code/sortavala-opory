/* ---- карта бригады монтажников: только СИП, подрезка крон (своя работа 14), кронштейны, светильники, бронекабель ---- */
var CWF=[4].concat(CW);
function crewW(p,k,on,d){p.w=p.w||{};if(on)p.w[k]=d||LD();else delete p.w[k]}
function krTxt(p){const k=+p.kr||0;return k==2?'2-рожк.'+(+p.ka?' '+p.ka+'°':''):k==1?'1-рожк.':'—'}
function wkN(k){return(WK.find(w=>w[0]==k)||[0,''])[1]}
function crewCard(p){const d=document.createElement('div');d.className='pp';const cz=p.vk&&!p.x?CABS.get(spKey(p.uid,'tp:'+p.tp)):null;
d.innerHTML=`<div><b>${esc(p.id)}</b> <small>${p.t=='A'?'анкерная':'стандартная'} · ${+p.h||8} м</small></div>
<div class="cri">${p.x?(p.sx?'<b style="color:#60a5fa">старая опора — СИП идёт по ней</b>':'<b style="color:#f87171">исключена, не монтируется</b>'):p.done?'<b style="color:#4ade80">опора установлена</b>':'<b style="color:#fbbf24">опора ещё не установлена</b>'} · кронштейн <b>${krTxt(p)}</b>${+p.sv?' · светильников <b>'+p.sv+'</b>':''}${p.js?' · <b style="color:#f87171">совм. подвеска</b>':''}${p.pp?' · <b style="color:#9ca3af">предлагаемая</b>':''}</div>
${cz?`<div class="cri" style="color:#e879f9">Ввод КЛ: бронекабель от ${esc(tpn(p.tp))} ≈ ${Math.round(cz.d)} м — ${cabDone(p.tp)?'проложен':'ещё не проложен'} <button data-cab>${esc(tpn(p.tp))} ›</button></div>`:''}
<div class="wh"><span data-wn></span><span>нажмите — отметить, на дату — изменить</span></div><div class="wg" data-wg></div>
<label class="wde" data-wde hidden><span data-wdn></span><input type=date data-wdi></label><div class="phb" data-phb hidden></div>
<input type=text data-cwc value="${esc(p.wc||'')}" placeholder="Комментарий по работам" style="width:100%;box-sizing:border-box;margin-top:4px">
${p.note?'<div class="cri">Примечание: '+esc(p.note)+'</div>':''}
<div class="brow"><button data-h>История опоры</button></div>`;
const ch=()=>{upd(p);save();stats();mark(p)};let EK=0,PHO=false;const phb=d.querySelector('[data-phb]');
const ed=k=>{EK=k;const r=d.querySelector('[data-wde]');if(!k){r.hidden=true;return}const v=wd(p,k);d.querySelector('[data-wdn]').textContent='Дата: '+(WSN[k]||'');d.querySelector('[data-wdi]').value=/^\d{4}-/.test(v)?v:'';r.hidden=false};
const rw=()=>{const g=d.querySelector('[data-wg]');g.innerHTML=CW.map(k=>{const n=wkN(k),on=wdone(p,k),v=wd(p,k),dd=/^\d{4}-/.test(v)?v.slice(8,10)+'.'+v.slice(5,7):(on?'✓':'');return `<div class="wt${on?' on':''}"><button class="wn" data-w=${k} title="${esc(n)}"><i>✓</i>${WSN[k]||esc(n)}</button>${k==14?`<button class="wph" data-wph title="Фото до и после">${ppIco}${ppN(p.uid,14)||''}</button>`:''}${on?`<button class="wdt" data-wd=${k} title="Изменить дату">${dd}</button>`:''}</div>`}).join('');
 d.querySelector('[data-wn]').textContent='РАБОТЫ БРИГАДЫ · '+CW.filter(k=>wdone(p,k)).length+'/'+CW.length;
 g.querySelectorAll('[data-w]').forEach(b=>b.onclick=()=>{PSEL=Date.now();const k=+b.dataset.w;crewW(p,k,!wdone(p,k),$('md').value||LD());if(k==14&&wdone(p,14)){PHO=true;if(!ppL(p.uid,14,'after').length)toast('Подрезка крон: добавьте фото «до» и «после»')}if(k==14)setTimeout(()=>phb._r(),0);if(EK==k)ed(0);setTimeout(()=>{rw();ch()},0)});
 g.querySelectorAll('[data-wd]').forEach(b=>b.onclick=()=>ed(+b.dataset.wd));const wp=g.querySelector('[data-wph]');if(wp)wp.onclick=()=>{PHO=!PHO;phb._r()}};
ppBlock(phb,p,14,()=>PHO);
d.querySelector('[data-wdi]').onchange=e=>{PSEL=Date.now();if(!EK||!e.target.value)return;crewW(p,EK,true,e.target.value);rw();ch()};
rw();
d.querySelector('[data-cwc]').onchange=e=>{PSEL=Date.now();p.wc=e.target.value.trim();ch()};
d.querySelector('[data-h]').onclick=()=>hpole(p);
const cb=d.querySelector('[data-cab]');if(cb)cb.onclick=()=>{const c=tpPos(p.tp);if(c){map.closePopup();tpPopup(String(p.tp),L.latLng(c))}};
return d}
function crewStats(){const e=$('crw');if(!e)return;const A=P.filter(p=>tpOk(p)&&(!p.x||p.sx)),Q=A.filter(p=>!p.x),td=LD(),c=(L2,k)=>L2.filter(p=>wdone(p,k)).length,tdy=k=>A.filter(p=>String(wd(p,k)).slice(0,10)==td).length,st=Q.filter(p=>p.done).length;
const tps=[...new Set(A.map(p=>String(p.tp||'—')))].sort((a,b)=>a.localeCompare(b,'ru',{numeric:true}));let spL=0,spN=0;SP.forEach(r=>{if(r.len!=null&&r.len!==''){spL+=+r.len;spN++}});
const cabT=[...new Set([...CABS.values()].map(z=>z.tp))].filter(t=>!FTS.size||FTS.has(t)),cabD=cabT.filter(cabDone).length;
const bar=(a,b,col)=>`<div class="crb2"><i style="width:${b?Math.min(100,Math.round(a/b*100)):0}%;background:${col}"></i></div>`;
const row=(n,a,b,col,k)=>`<div class="crr"><span>${n}</span>${k&&tdy(k)?'<small>сегодня +'+tdy(k)+'</small>':''}<b>${a}${b!=null?' / '+b:''}</b></div>${b!=null?bar(a,b,col):''}`;
e.innerHTML=row('Опор установлено — можно работать',st,Q.length,'#22c55e')+row('СИП протянут (опор)',c(A,5),A.length,'#f97316',5)
+`<div class="crr"><span>СИП по пролётам (длина внесена)</span><b>${spN} пр. · ${Math.round(spL).toLocaleString('ru-RU')} м</b></div>`
+row('Кронштейн установлен',c(Q,12),Q.length,'#60a5fa',12)+row('Светильник установлен',c(Q,6),Q.length,'#facc15',6)+row('Подрезка крон (опор)',c(A,14),null,'',14)+row('Бронекабель проложен (ТП)',cabD,cabT.length,'#c026d3')
+'<table class="crt"><tr><th>ТП</th><th>опор стоит</th><th>СИП</th><th>кроншт.</th><th>светил.</th><th>брон.</th></tr>'+tps.map(t=>{const a=A.filter(p=>String(p.tp||'—')==t),q=a.filter(p=>!p.x);return `<tr><td>${esc(tpn(t))}</td><td>${q.filter(p=>p.done).length}/${q.length}</td><td>${c(a,5)}</td><td>${c(q,12)}</td><td>${c(q,6)}</td><td>${cabT.includes(t)?(cabDone(t)?'✓':'—'):''}</td></tr>`}).join('')+'</table>'
+'<div class="r" style="margin-top:6px"><button id="crx">Отчёт бригады (Excel)</button></div>';$('crx').onclick=crewXl}
function crewXl(){const fd=v=>/^\d{4}-/.test(v)?v.slice(8,10)+'.'+v.slice(5,7)+'.'+v.slice(0,4):(v?'да':''),A=P.filter(p=>tpOk(p)&&(!p.x||p.sx)).sort((a,b)=>String(a.tp).localeCompare(String(b.tp),'ru',{numeric:true})||(+a.n||0)-(+b.n||0)),wb=XLSX.utils.book_new(),sh=(rows,nm,w)=>{const ws=XLSX.utils.aoa_to_sheet(rows);ws['!cols']=w.map(x=>({wch:x}));XLSX.utils.book_append_sheet(wb,ws,nm)};
sh([['Опора','ТП','№','Тип','Опора стоит','Кронштейн (тип)','Подрезка крон','Кронштейн установлен','СИП протянут','Светильник установлен','Комментарий'],...A.map(p=>[p.id,tpn(p.tp),p.n||'',p.t=='A'?'анкерная':'стандартная',p.x?'старая (СИП по ней)':p.done?fd(p.date||'да'):'нет',krTxt(p),fd(wd(p,14)),fd(wd(p,12)),fd(wd(p,5)),fd(wd(p,6)),p.wc||''])],'По опорам',[16,10,5,12,14,12,12,12,12,12,30]);
const S=[...SP.values()].filter(r=>r.len!=null&&r.len!=='').sort((a,b)=>String(a.sd||'').localeCompare(String(b.sd||''))||String(a.id||'').localeCompare(String(b.id||''),'ru',{numeric:true}));
sh([['Пролёт','Длина СИП, м','Дата протяжки','Примечание','Кто внёс'],...S.map(r=>[r.id||r.uid,+r.len,fd(r.sd||''),r.note||'',r.ed||'']),['Итого',Math.round(S.reduce((a,r)=>a+(+r.len||0),0)*10)/10]],'СИП по пролётам',[34,12,14,30,16]);
const C=[...CABS.values()].sort((a,b)=>a.tp.localeCompare(b.tp,'ru',{numeric:true}));
sh([['ТП','Опора ввода','По карте, м','Проложен','Факт, м'],...C.map(z=>{const r=TPD.get(z.tp)||{},w=r.w||{};return[tpn(z.tp),z.p.id,Math.round(z.d),fd(w[1]||''),r.cab!=null?+r.cab:'']})],'Бронекабель',[16,16,12,12,10]);
const days={};A.forEach(p=>CW.forEach(k=>{const v=wd(p,k);if(/^\d{4}-/.test(v)){(days[v]=days[v]||{})[k]=(days[v][k]||0)+1}}));
sh([['Дата',...CW.map(wkN)],...Object.keys(days).sort().map(d=>[fd(d),...CW.map(k=>days[d][k]||0)])],'По дням',[12,14,14,14,14]);
XLSX.writeFile(wb,'Монтаж_бригада_'+LD()+'.xlsx')}
