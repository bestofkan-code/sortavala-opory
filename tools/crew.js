/* ---- карта бригады монтажников: только СИП, подрезка крон (своя работа 14), кронштейны, светильники, бронекабель ---- */
var CWF=[4].concat(CW),CRN=null;
/* на монтажной карте не показываем: исключённые опоры (кроме тех, по которым идёт СИП — Шуно Дорожная-2…7)
   и опоры на гравитационном фундаменте, через которые не проходит линия СИП */
function crNetUpd(){if(!NETC)return;const s=new Set();NETC.E.forEach(e=>{s.add(e[0].uid);s.add(e[1].uid)});const ch=!CRN||CRN.size!=s.size||[...s].some(u=>!CRN.has(u));CRN=s;if(ch&&typeof mk!='undefined'&&mk.size)setTimeout(()=>{P.forEach(upd);numLabels();stats()},0)}
function crHide(p){if(p.x&&!p.sx)return true;if(typeof TKONLY!='undefined'&&TKONLY&&!tkOf(p).length)return true;return isG(p)&&!!CRN&&!CRN.has(p.uid)}
function crewW(p,k,on,d){p.w=p.w||{};if(on)p.w[k]=d||LD();else delete p.w[k]}
var KRG=[['1-рожковые',353,p=>(+p.kr||0)==1],['2-рожк. 90°',50,p=>(+p.kr||0)==2&&+p.ka==90],['2-рожк. 180°',189,p=>(+p.kr||0)==2&&+p.ka==180],['2-рожк., угол не указан',null,p=>(+p.kr||0)==2&&+p.ka!=90&&+p.ka!=180],['тип не указан',null,p=>!(+p.kr)]],KLUM=831;
function lumN(p){return +p.sv||((+p.kr||0)==2?2:(+p.kr||0)==1?1:0)}
function krTbl(Q,ALL){const C=ALL?Q.filter(p=>!isG(p)):Q,G=ALL?Q.filter(isG):[],dif=(a,b)=>b==null||a==b?'':` <small style="color:${a>b?'#fbbf24':'#f87171'}">${a>b?'+':''}${a-b}</small>`;
 return '<table class="crt"><tr><th>Кронштейны</th>'+(ALL?'<th>итог</th>':'')+'<th>на карте</th><th>уст.</th></tr>'+KRG.map(([n,t,f])=>{const m=C.filter(f).length,i=Q.filter(p=>f(p)&&wdone(p,12)).length;if(t==null&&!m&&!i)return '';return `<tr><td>${n}</td>${ALL?'<td>'+(t??'—')+'</td>':''}<td>${m}${ALL?dif(m,t):''}</td><td>${i}</td></tr>`}).join('')
 +(()=>{const m=C.reduce((a,p)=>a+lumN(p),0),i=Q.filter(p=>wdone(p,6)).reduce((a,p)=>a+lumN(p),0);return `<tr style="font-weight:600"><td>Светильников</td>${ALL?'<td>'+KLUM+'</td>':''}<td>${m}${ALL?dif(m,KLUM):''}</td><td>${i}</td></tr>`})()+'</table>'
 +(ALL&&G.length?`<small style="display:block;opacity:.7;margin-top:2px">«На карте» — опоры по контракту. Ещё на гравит. фундаменте на линии СИП: ${KRG.slice(0,3).map(([n,t,f])=>n+' '+G.filter(f).length).join(', ')}.</small>`:'')}
function krTxt(p){const k=+p.kr||0;return k==2?'2-рожк.'+(+p.ka?' '+p.ka+'°':''):k==1?'1-рожк.':'—'}
function wkN(k){return(WK.find(w=>w[0]==k)||[0,''])[1]}
function crewCard(p){const d=document.createElement('div');d.className='pp';const cz=p.vk&&!p.x?CABS.get(spKey(p.uid,'tp:'+p.tp)):null;
d.innerHTML=`<div><b>${esc(p.id)}</b> <small>${p.t=='A'?'анкерная':'стандартная'} · ${+p.h||8} м</small></div>
<div class="cri">${p.x?(p.sx?'<b style="color:#60a5fa">старая опора — СИП идёт по ней</b>':'<b style="color:#f87171">исключена, не монтируется</b>'):p.done?'<b style="color:#4ade80">опора установлена</b>':'<b style="color:#fbbf24">опора ещё не установлена</b>'} · кронштейн <b>${krTxt(p)}</b>${+p.sv?' · светильников <b>'+p.sv+'</b>':''}${p.js?' · <b style="color:#f87171">совм. подвеска</b>':''}${p.pp?' · <b style="color:#9ca3af">предлагаемая</b>':''}</div>
${typeof tkOf=='function'&&tkOf(p).length?'<div class="cri" style="color:#22d3ee">Задание: '+tkOf(p).map(t=>'<b>«'+esc(t.name||'')+'»</b> — '+esc(tkWN(t))+(t.d2?', до '+fdm(t.d2):'')).join('; ')+'</div>':''}
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
function crewStats(){const e=$('crw');if(!e)return;const A=P.filter(p=>tpOk(p)&&!crHide(p)),Q=A.filter(p=>!p.x),td=LD(),c=(L2,k)=>L2.filter(p=>wdone(p,k)).length,tdy=k=>A.filter(p=>String(wd(p,k)).slice(0,10)==td).length,st=Q.filter(p=>p.done).length;
const ALL=!FTS.size&&!(typeof TKONLY!='undefined'&&TKONLY),K=592,NP=ALL?K:Q.length,NA=ALL?K:A.length,nets=new Set([...CABS.values()].map(z=>z.tp)).size,sxn=P.filter(p=>p.x&&p.sx).length,KS=K+sxn-nets;
const tps=[...new Set(A.map(p=>String(p.tp||'—')))].sort((a,b)=>a.localeCompare(b,'ru',{numeric:true}));let spL=0,spN=0;SP.forEach(r=>{if(r.len!=null&&r.len!==''){spL+=+r.len;spN++}});
const cabT=[...new Set([...CABS.values()].map(z=>z.tp))].filter(t=>!FTS.size||FTS.has(t)),cabD=cabT.filter(cabDone).length;
const bar=(a,b,col)=>`<div class="crb2"><i style="width:${b?Math.min(100,Math.round(a/b*100)):0}%;background:${col}"></i></div>`;
const row=(n,a,b,col,k,u)=>`<div class="crr"><span>${n}</span>${k&&tdy(k)?'<small>сегодня +'+tdy(k)+'</small>':''}<b>${a}${b!=null?' / '+b:''}${u||''}</b></div>${b!=null?bar(a,b,col):''}`;
e.innerHTML=(ALL?`<small style="display:block;opacity:.8;margin-bottom:2px">Итог по контракту: <b>${K} опор</b> и <b>${KS} пролётов СИП</b> (${K} опор + ${sxn} старых опор Шуно Дорожная, по которым идёт СИП, минус ${nets} линий от ТП).</small>`:'<small style="display:block;opacity:.8;margin-bottom:2px">Счёт по выбранным опорам (фильтр ТП или задания).</small>')
+row('Опор установлено — можно работать',st,NP,'#22c55e')+row('СИП протянут (опор)',c(A,5),NA,'#f97316',5)
+row('СИП по пролётам (длина внесена)',spN,ALL?KS:null,'#f97316',0,' пр.')+`<div class="crr" style="margin-top:2px"><span></span><small style="color:inherit;opacity:.8">${Math.round(spL).toLocaleString('ru-RU')} м внесено</small></div>`
+row('Кронштейн установлен',c(Q,12),NP,'#60a5fa',12)+row('Светильник установлен',c(Q,6),NP,'#facc15',6)+row('Подрезка крон (опор)',c(A,14),null,'',14)+row('Бронекабель проложен (ТП)',cabD,cabT.length,'#c026d3')
+krTbl(Q,ALL)
+'<table class="crt"><tr><th>ТП</th><th>опор стоит</th><th>СИП</th><th>кроншт.</th><th>светил.</th><th>брон.</th></tr>'+tps.map(t=>{const a=A.filter(p=>String(p.tp||'—')==t),q=a.filter(p=>!p.x);return `<tr><td>${esc(tpn(t))}</td><td>${q.filter(p=>p.done).length}/${q.length}</td><td>${c(a,5)}</td><td>${c(q,12)}</td><td>${c(q,6)}</td><td>${cabT.includes(t)?(cabDone(t)?'✓':'—'):''}</td></tr>`}).join('')+'</table>'
+(ALL&&NETC?`<small style="display:block;opacity:.7;margin-top:4px">Сейчас на карте на линии СИП: ${CRN?CRN.size:'—'} опор, ${NETC.E.length} пролётов (вместе с опорами на гравит. фундаменте).</small>`:'')
+'<div class="r" style="margin-top:6px"><button id="crx">Отчёт бригады (Excel)</button></div>';$('crx').onclick=crewXl}
function crewXl(){const fd=v=>/^\d{4}-/.test(v)?v.slice(8,10)+'.'+v.slice(5,7)+'.'+v.slice(0,4):(v?'да':''),A=P.filter(p=>tpOk(p)&&!crHide(p)).sort((a,b)=>String(a.tp).localeCompare(String(b.tp),'ru',{numeric:true})||(+a.n||0)-(+b.n||0)),wb=XLSX.utils.book_new(),sh=(rows,nm,w)=>{const ws=XLSX.utils.aoa_to_sheet(rows);ws['!cols']=w.map(x=>({wch:x}));XLSX.utils.book_append_sheet(wb,ws,nm)};
sh([['Опора','ТП','№','Тип','Опора стоит','Кронштейн (тип)','Подрезка крон','Кронштейн установлен','СИП протянут','Светильник установлен','Комментарий'],...A.map(p=>[p.id,tpn(p.tp),p.n||'',p.t=='A'?'анкерная':'стандартная',p.x?'старая (СИП по ней)':p.done?fd(p.date||'да'):'нет',krTxt(p),fd(wd(p,14)),fd(wd(p,12)),fd(wd(p,5)),fd(wd(p,6)),p.wc||''])],'По опорам',[16,10,5,12,14,12,12,12,12,12,30]);
const S=[...SP.values()].filter(r=>r.len!=null&&r.len!=='').sort((a,b)=>String(a.sd||'').localeCompare(String(b.sd||''))||String(a.id||'').localeCompare(String(b.id||''),'ru',{numeric:true}));
sh([['Пролёт','Длина СИП, м','Дата протяжки','Примечание','Кто внёс'],...S.map(r=>[r.id||r.uid,+r.len,fd(r.sd||''),r.note||'',r.ed||'']),['Итого',Math.round(S.reduce((a,r)=>a+(+r.len||0),0)*10)/10]],'СИП по пролётам',[34,12,14,30,16]);
const C=[...CABS.values()].sort((a,b)=>a.tp.localeCompare(b.tp,'ru',{numeric:true}));
sh([['ТП','Опора ввода','По карте, м','Проложен','Факт, м'],...C.map(z=>{const r=TPD.get(z.tp)||{},w=r.w||{};return[tpn(z.tp),z.p.id,Math.round(z.d),fd(w[1]||''),r.cab!=null?+r.cab:'']})],'Бронекабель',[16,16,12,12,10]);
{const Qx=A.filter(p=>!p.x),C=Qx.filter(p=>!isG(p));sh([['Кронштейн','Итог по контракту','На карте (по контракту)','На гравит. фундаменте','Установлено'],...KRG.map(([n,t,f])=>[n,t??'',C.filter(f).length,Qx.filter(p=>isG(p)&&f(p)).length,Qx.filter(p=>f(p)&&wdone(p,12)).length]),['Светильников',KLUM,C.reduce((a,p)=>a+lumN(p),0),Qx.filter(isG).reduce((a,p)=>a+lumN(p),0),Qx.filter(p=>wdone(p,6)).reduce((a,p)=>a+lumN(p),0)]],'Кронштейны',[26,16,20,20,12])}
const days={};A.forEach(p=>CW.forEach(k=>{const v=wd(p,k);if(/^\d{4}-/.test(v)){(days[v]=days[v]||{})[k]=(days[v][k]||0)+1}}));
sh([['Дата',...CW.map(wkN)],...Object.keys(days).sort().map(d=>[fd(d),...CW.map(k=>days[d][k]||0)])],'По дням',[12,14,14,14,14]);
XLSX.writeFile(wb,'Монтаж_бригада_'+LD()+'.xlsx')}
