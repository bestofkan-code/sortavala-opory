import sys
FILES=['redaktor.html','prosmotr.html','montazh.html','zamechaniya.html','zamechaniya-prosmotr.html','uchastki.html']
KM_DEF=r"""var KMT={kro:['опоры и кронштейны','План-схема: опоры и кронштейны по типам','Кронштейны по типам — для сверки после монтажа','Кронштейны по типам на опорах'],mnt:['установленные кронштейны и светильники','Схема: установленные кронштейны и светильники','Установленные кронштейны и светильники','Установленные кронштейны и светильники'],sip:['протянутый СИП-4 4×25','Схема: протянутый СИП-4 4×25 по опорам','Протянутый СИП-4 4×25 по опорам','Протянутый СИП по опорам'],gz:['повторное заземление опор','Схема: повторное заземление (котлованы)','Повторное заземление опор (котлованы)','Повторное заземление опор']};
function kmPole(m,p){if(m=='kro')return{uid:'p0',t:'S',kr:p.kr,ka:p.ka,w:{12:'x'}};if(m=='mnt'){const k=wdone(p,12)||wdone(p,6);return{uid:'p0',t:'S',kr:k?p.kr:0,ka:p.ka,w:k?{12:'x'}:{},sv:k?lumI(p):0}}if(m=='gz')return{uid:'p0',t:'S',g:!!(p.g&&wdone(p,11))};return{uid:'p0',t:'S'}}
function kmLeg(m){const N=['n','Номер опоры'],O=['p','Опора',{t:'S'}];if(m=='kro')return[['p','Кронштейн 1-рожковый — 353 шт.',{t:'S',kr:1,w:{12:'x'}}],['p','Кронштейн 2-рожковый 90° — 50 шт.',{t:'S',kr:2,ka:90,w:{12:'x'}}],['p','Кронштейн 2-рожковый 180° — 189 шт.',{t:'S',kr:2,ka:180,w:{12:'x'}}]];if(m=='mnt')return[O,['p','Кронштейн 1-рожковый установлен',{t:'S',kr:1,w:{12:'x'}}],['p','Кронштейн 2-рожковый 90° установлен',{t:'S',kr:2,ka:90,w:{12:'x'}}],['p','Кронштейн 2-рожковый 180° установлен',{t:'S',kr:2,ka:180,w:{12:'x'}}],['p','Светильник установлен (жёлтый кружок)',{t:'S',kr:2,ka:180,sv:2,w:{12:'x'}}],N];if(m=='sip')return[O,['l','СИП-4 4×25 протянут','#2563eb',[]],N];if(m=='gz')return[O,['p','Повторное заземление выполнено',{t:'S',g:1}],N];return[]}
"""
R=[("SH=SH0.filter(p=>!p.x&&!(o.kro&&(isG(p)||p.pp))),","SH=SH0.filter(p=>!p.x&&!(o.km&&(isG(p)||p.pp))),"),
("(o.kro?[]:cabPaths())","(o.km?[]:cabPaths())"),("(o.kro?[]:DLC)","(o.km?[]:DLC)"),
("NT.E.filter(e=>!o.kro&&","NT.E.filter(e=>!o.km&&"),("rlinks().filter(([a,b])=>!o.kro&&","rlinks().filter(([a,b])=>!o.km&&"),
("try{(o.kro?[]:S2)","try{(o.km?[]:S2)"),
("try{(o.kro?[]:HK).forEach(z=>{const [x,y]=C(+z.lat,+z.lon);hkCv(g,x,y,u*.12)})}catch(e){}","try{(o.km?[]:HK).forEach(z=>{const [x,y]=C(+z.lat,+z.lon);hkCv(g,x,y,u*.12)})}catch(e){}if(o.km=='sip'){try{const RR=sipCalc();g.save();g.strokeStyle='#2563eb';g.lineWidth=lw*3.4;g.lineCap='round';g.lineJoin='round';RR.ED.filter(e=>e.kind!='u'&&wdone(e.a,5)&&wdone(e.b,5)).forEach(e=>{g.beginPath();epath(e.a,e.b,e.e&&e.e.pts).forEach((q,i)=>i?g.lineTo(...C(q[0],q[1])):g.moveTo(...C(q[0],q[1])));g.stroke()});g.restore()}catch(e){console.warn('kmsip',e)}}"),
("o.kro?{uid:'p0',t:'S',kr:p.kr,ka:p.ka,w:{12:'x'}}:p","o.km?kmPole(o.km,p):p"),
("T(o.kro?'опоры и кронштейны':'опоры, кронштейны, СИП-4 4×25'","T(o.km?KMT[o.km][0]:'опоры, кронштейны, СИП-4 4×25'"),
("T(o.kro?'Условные обозначения':","T(o.km?'Условные обозначения':"),
("if(o.kro){LGI.length=0;LGI.push(['p','Кронштейн 1-рожковый — 353 шт.',{t:'S',kr:1,w:{12:'x'}}],['p','Кронштейн 2-рожковый 90° — 50 шт.',{t:'S',kr:2,ka:90,w:{12:'x'}}],['p','Кронштейн 2-рожковый 180° — 189 шт.',{t:'S',kr:2,ka:180,w:{12:'x'}}])}","if(o.km){LGI.length=0;LGI.push(...kmLeg(o.km))}"),
("const half=o.kro?LGI.length:Math.ceil(LGI.length/2),cwd=o.kro?pw:pw/2,","const half=o.km?LGI.length:Math.ceil(LGI.length/2),cwd=o.km?pw:pw/2,"),
("g.fillText(o.kro?'Количество — по смете, всего 592 шт.':'Положение опор приблизительное.',px,y)}","g.fillText(o.km=='kro'?'Количество — по смете, всего 592 шт.':o.km?'По отметкам монтажа на дату листа.':'Положение опор приблизительное.',px,y)}"),
("let L2=wrap(o.kro?'План-схема: опоры и кронштейны по типам':","let L2=wrap(o.km?KMT[o.km][1]:"),
("title:($('pdko')&&$('pdko').checked)?'Кронштейны по типам — для сверки после монтажа':ar.title,","title:KMV()?KMT[KMV()][2]:ar.title,"),
("legend:$('pdlg').checked||($('pdko')&&$('pdko').checked),kro:!!($('pdko')&&$('pdko').checked),","legend:$('pdlg').checked||!!KMV(),km:KMV(),"),
("doc.save(($('pdko')&&$('pdko').checked)?'Кронштейны по типам на опорах — '+new Date().toLocaleDateString('ru-RU')+'.pdf':ar.file);","doc.save(KMV()?KMT[KMV()][3]+' — '+new Date().toLocaleDateString('ru-RU')+'.pdf':ar.file);"),
('<label title="Только опоры контракта и кронштейны по типам, номера опор; в условных обозначениях — типы кронштейнов с количеством по смете"><input type="checkbox" id="pdko"> только кронштейны (для стройконтроля)</label>',
 '</div><div class="r">Лист для стройконтроля: <select id="pdko" style="flex:1;min-width:0"><option value="">— обычный план —</option><option value="kro">кронштейны по типам (по смете)</option><option value="mnt">установленные кронштейны и светильники</option><option value="sip">протянутый СИП по опорам</option><option value="gz">повторное заземление (котлованы)</option></select>'),
("async function buildPlan(o){","const KMV=()=>{const e=document.getElementById('pdko');return e&&e.value||''};"+KM_DEF+"async function buildPlan(o){"),
]
for f in FILES:
    s=open(f,encoding='utf-8').read()
    if 'function kmPole' in s: print('skip',f); continue
    for a,b in R:
        if s.count(a)!=1: sys.exit(f'{f}: {a[:60]} count {s.count(a)}')
        s=s.replace(a,b)
    if 'o.kro' in s: sys.exit(f+' leftover o.kro')
    open(f,'w',encoding='utf-8').write(s); print('ok',f)
