import sys
FILES=['redaktor.html','prosmotr.html','montazh.html','zamechaniya.html','zamechaniya-prosmotr.html','uchastki.html']
R=[
("SH=SH0.filter(p=>!p.x),","SH=SH0.filter(p=>!p.x&&!(o.kro&&(isG(p)||p.pp))),"),
("cabPaths().forEach(z=>{g.save();g.strokeStyle='#c026d3'","(o.kro?[]:cabPaths()).forEach(z=>{g.save();g.strokeStyle='#c026d3'"),
("DLC.forEach(sg=>{const ua='p'+sg[0][0]","(o.kro?[]:DLC).forEach(sg=>{const ua='p'+sg[0][0]"),
("NT.E.filter(e=>(e[2]!='d'||e.pts)&&SHS.has(e[0])","NT.E.filter(e=>!o.kro&&(e[2]!='d'||e.pts)&&SHS.has(e[0])"),
("rlinks().filter(([a,b])=>SHS.has(a)&&SHS.has(b))","rlinks().filter(([a,b])=>!o.kro&&SHS.has(a)&&SHS.has(b))"),
("try{S2.forEach(z=>{const gg=s2Geo(z)","try{(o.kro?[]:S2).forEach(z=>{const gg=s2Geo(z)"),
("try{HK.forEach(z=>{const [x,y]=C(+z.lat,+z.lon);hkCv(g,x,y,u*.12)})}","try{(o.kro?[]:HK).forEach(z=>{const [x,y]=C(+z.lat,+z.lon);hkCv(g,x,y,u*.12)})}"),
("SH.forEach(p=>dpole(g,...C(p.lat,p.lon),p,r));","SH.forEach(p=>dpole(g,...C(p.lat,p.lon),o.kro?{uid:'p0',t:p.t,kr:p.kr,ka:p.ka,w:{12:'x'}}:p,r));"),
("T('опоры, кронштейны, СИП-4 4×25',px,y,(A3?4.4:3.8)*u);","T(o.kro?'опоры и кронштейны':'опоры, кронштейны, СИП-4 4×25',px,y,(A3?4.4:3.8)*u);"),
("T('Условные обозначения (как на карте)',px,y,(A3?4.6:4)*u);","T(o.kro?'Условные обозначения':'Условные обозначения (как на карте)',px,y,(A3?4.6:4)*u);"),
("['t','Трансформаторная подстанция']];","['t','Трансформаторная подстанция']];if(o.kro){LGI.length=0;LGI.push(['p','Кронштейн 1-рожковый — 353 шт.',{t:'S',kr:1,w:{12:'x'}}],['p','Кронштейн 2-рожковый 90° — 50 шт.',{t:'S',kr:2,ka:90,w:{12:'x'}}],['p','Кронштейн 2-рожковый 180° — 189 шт.',{t:'S',kr:2,ka:180,w:{12:'x'}}])}"),
("const half=Math.ceil(LGI.length/2),cwd=pw/2,","const half=o.kro?LGI.length:Math.ceil(LGI.length/2),cwd=o.kro?pw:pw/2,"),
("g.fillText('Положение опор приблизительное.',px,y)}","g.fillText(o.kro?'Количество — по смете, всего 592 шт.':'Положение опор приблизительное.',px,y)}"),
('<label><input type="checkbox" id="pdlg"> условные обозначения</label>','<label><input type="checkbox" id="pdlg"> условные обозначения</label> <label title="Только опоры контракта и кронштейны по типам, номера опор; в условных обозначениях — типы кронштейнов с количеством по смете"><input type="checkbox" id="pdko"> только кронштейны (для стройконтроля)</label>'),
("legend:$('pdlg').checked,","legend:$('pdlg').checked||($('pdko')&&$('pdko').checked),kro:!!($('pdko')&&$('pdko').checked),"),
]
for f in FILES:
    s=open(f,encoding='utf-8').read()
    if 'o.kro' in s: print('skip',f); continue
    for a,b in R:
        if s.count(a)!=1: sys.exit(f'{f}: {a[:50]} count {s.count(a)}')
        s=s.replace(a,b)
    open(f,'w',encoding='utf-8').write(s); print('ok',f)
