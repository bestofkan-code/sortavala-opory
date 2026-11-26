import sys
f='redaktor.html';t=open(f).read()
R=[
("function kmShow(m,p){return m=='mnt'?","function kmShow(m,p){if(m=='ks')return wdone(p,12)||wdone(p,6)||wdone(p,5)||(!!p.g&&wdone(p,11))||wdone(p,16);return m=='mnt'?",1),
("function kmPole(m,p){if(m=='kro')","function kmPole(m,p){if(m=='ks'){const k=wdone(p,12)||wdone(p,6);return{uid:'p0',t:'S',kr:k?p.kr:0,ka:p.ka,w:k?{12:'x'}:{},sv:k?lumI(p):0,done:wdone(p,16)}}if(m=='kro')",1),
("function kmLeg(m){const N=['n','Номер опоры'],O=['p','Опора',{t:'S'}];","function kmLeg(m){const N=['n','Номер опоры'],O=['p','Опора',{t:'S'}];if(m=='ks')return[O,['p','Кронштейн 1-рожковый установлен',{t:'S',kr:1,w:{12:'x'}}],['p','Кронштейн 2-рожковый 90° установлен',{t:'S',kr:2,ka:90,w:{12:'x'}}],['p','Кронштейн 2-рожковый 180° установлен',{t:'S',kr:2,ka:180,w:{12:'x'}}],['p','Светильник установлен (желтый кружок)',{t:'S',kr:2,ka:180,sv:2,w:{12:'x'}}],['p','Цоколь установлен (опора залита зеленым)',{t:'S',done:true}],['l','СИП-4 4×25 протянут, арматура СИП смонтирована','#2563eb',[]],...(S2.length?[['l','СИП 2-я цепь (по опорам другого ТП)','#f97316',[]]]:[]),...(S2.length||HK.length?[['h','Крюк в своде арки']]:[]),['z','Котлован заземления выполнен (зеленое кольцо)'],N];",1),
("gz:['повторное заземление опор',","ks:['выполненные работы на опорах','Схема выполненных работ: кронштейны, светильники, цоколи, СИП с арматурой, заземление','Выполненные работы на опорах — к КС','Выполненные работы к КС'],gz:['повторное заземление опор',",1),
("(o.km&&o.km!='sip'?[]:S2)","(o.km&&o.km!='sip'&&o.km!='ks'?[]:S2)",1),
("(o.km&&o.km!='sip'?[]:HK)","(o.km&&o.km!='sip'&&o.km!='ks'?[]:HK)",1),
("if(o.km=='sip'){try{const RR=sipCalc()","if(o.km=='sip'||o.km=='ks'){try{const RR=sipCalc()",1),
("if(o.km=='gz'){g.save();g.strokeStyle='#15803d'","if(o.km=='gz'||o.km=='ks'){g.save();g.strokeStyle='#15803d'",1),
('<option value="gz">повторное заземление (котлованы)</option>','<option value="gz">повторное заземление (котлованы)</option><option value="ks">все выполненные работы (к КС)</option>',1),
]
for a,b,n in R:
  c=t.count(a)
  if c!=n:sys.exit(f'{c}x: {a[:60]}')
  t=t.replace(a,b)
open(f,'w').write(t);print('ok')
