import sys,re
f='redaktor.html';t=open(f).read()
i=t.find('function kmLeg(m){');j=t.find('return[]}',i)+len('return[]}')
assert i>0 and j>i and t.count('function kmLeg(m){')==1
NEW=r"""function kmCnt(){const Q=P.filter(p=>!p.x&&!isG(p)&&!p.pp),c={k1:0,k90:0,k180:0,lum:0,gz:0,cz:0,sip:0,s2:0,hk:0,ar:[0,0,0,0]};
 Q.forEach(p=>{if(kmShow('mnt',p)){const q=kmPole('mnt',p);if(q.w&&q.w[12]){if(+q.kr==1)c.k1++;else if(+q.ka==90)c.k90++;else c.k180++}c.lum+=+q.sv||0}if(kmShow('gz',p))c.gz++;if(kmShow('cz',p))c.cz++});
 try{const C=sipCalc(),ok=p=>!p.x&&wdone(p,5);C.ED.forEach(x=>{if(ok(x.a)&&ok(x.b))c.sip+=x.len});(C.S2X||[]).forEach(z=>{if(z.done)c.s2+=z.len})}catch(e){}
 c.hk=(HK||[]).length;try{(S2||[]).forEach(z=>{c.hk+=s2Geo(z).pts.filter(q=>q.hook).length})}catch(e){}
 P.filter(p=>!p.x).forEach(p=>{const r=p.ar;let a=[0,0,0,0];if(r&&(r.h||r.a||r.pc||('s' in r))){const v=arV(p);a=[v.h,v.a,v.s,v.pc]}else if(wdone(p,5)){const pl=arPlan(p);a=[pl.h,pl.a,pl.a?0:1,pl.pc]}a.forEach((v,i)=>c.ar[i]+=+v||0)});
 c.sip=Math.round(c.sip);c.s2=Math.round(c.s2);return c}
const kmN=v=>(+v||0).toLocaleString('ru-RU');
function kmArTxt(c){return 'Арматура СИП: крюки — '+kmN(c.ar[0])+' шт., анкерные зажимы — '+kmN(c.ar[1])+' шт., поддерживающие зажимы — '+kmN(c.ar[2])+' шт., прокалывающие зажимы СИП–СИП — '+kmN(c.ar[3])+' шт.'}
var KMW={kro:'Кронштейны по типам (по смете)',mnt:'Монтаж кронштейнов и светильников',sip:'Монтаж СИП-4 4×25 по опорам с арматурой',gz:'Повторное заземление (комплект)',cz:'Монтаж цоколей опор',ks:'Монтаж кронштейнов, светильников, цоколей, СИП-4 4×25 с арматурой; повторное заземление (комплект)'};
function kmLeg(m){const N=['n','Номер опоры'],O=['p','Опора',{t:'S'}],c=m=='kro'?null:kmCnt(),sh=' шт.';
 const MNT=()=>[['p','Кронштейн 1-рожковый установлен — '+kmN(c.k1)+sh,{t:'S',kr:1,w:{12:'x'}}],['p','Кронштейн 2-рожковый 90° установлен — '+kmN(c.k90)+sh,{t:'S',kr:2,ka:90,w:{12:'x'}}],['p','Кронштейн 2-рожковый 180° установлен — '+kmN(c.k180)+sh,{t:'S',kr:2,ka:180,w:{12:'x'}}],['p','Светильник установлен (желтый кружок) — '+kmN(c.lum)+sh,{t:'S',kr:2,ka:180,sv:2,w:{12:'x'}}]];
 const SIPL=()=>[['l','СИП-4 4×25 протянут — '+kmN(c.sip)+' м','#2563eb',[]],...(S2.length?[['l','СИП 2-я цепь (по опорам другого ТП) — '+kmN(c.s2)+' м','#f97316',[]]]:[]),...(c.hk?[['h','Крюк в своде арки — '+kmN(c.hk)+sh]]:[])];
 const GZ=()=>[['z','Повторное заземление (комплект) выполнено (зеленое кольцо) — '+kmN(c.gz)+' компл.']],CZ=()=>[['p','Цоколь установлен (опора залита зеленым) — '+kmN(c.cz)+sh,{t:'S',done:true}]];
 if(m=='kro')return[['p','Кронштейн 1-рожковый — 353 шт.',{t:'S',kr:1,w:{12:'x'}}],['p','Кронштейн 2-рожковый 90° — 50 шт.',{t:'S',kr:2,ka:90,w:{12:'x'}}],['p','Кронштейн 2-рожковый 180° — 189 шт.',{t:'S',kr:2,ka:180,w:{12:'x'}}]];
 if(m=='mnt')return[...MNT(),N];if(m=='sip')return[O,...SIPL(),N];if(m=='gz')return[O,...GZ(),N];if(m=='cz')return[...CZ(),N];
 if(m=='ks')return[O,...MNT(),...CZ(),...SIPL(),...GZ(),N];return[]}"""
t=t[:i]+NEW+t[j:]
R=[
("T('План-схема участка работ',px,y,(A3?6.2:5.2)*u);y+=(A3?6.5:5.6)*u;T(o.km?KMT[o.km][0]:'опоры, кронштейны, СИП-4 4×25',px,y,(A3?4.4:3.8)*u);y+=5*u;\ng.font=`${3.2*u}px ${F}`;wrap((o.title||'Общий план')+' · по состоянию на '+date,pw)",
 "if(o.km){const fz=(A3?5.6:4.8)*u;g.font=`${fz}px ${F}`;wrap(KMW[o.km]||'',pw).forEach(l=>{T(l,px,y,fz);y+=fz*1.2});y+=.8*u}else{T('План-схема участка работ',px,y,(A3?6.2:5.2)*u);y+=(A3?6.5:5.6)*u;T('опоры, кронштейны, СИП-4 4×25',px,y,(A3?4.4:3.8)*u);y+=5*u}\ng.font=`${3.2*u}px ${F}`;wrap(o.km?(o.km=='kro'?'По состоянию на '+date:'Выполнено по состоянию на '+date):(o.title||'Общий план')+' · по состоянию на '+date,pw)",1),
("g.fillText(o.km=='kro'?'Количество — по смете, всего 592 шт.':o.km?'По отметкам монтажа на дату листа.':'Положение опор приблизительное.',px,y)",
 "if(o.km=='sip'||o.km=='ks'){wrap(kmArTxt(kmCnt()),pw).forEach(l=>{g.fillText(l,px,y);y+=3.6*u})}else g.fillText(o.km=='kro'?'Количество — по смете, всего 592 шт.':o.km?'':'Положение опор приблизительное.',px,y)",1),
("T('КАР/00230/26',sx+100*u,sy+7.5*u,5*u,'center');","if(!o.km)T('КАР/00230/26',sx+100*u,sy+7.5*u,5*u,'center');",1),
("gz:['повторное заземление опор','Схема: повторное заземление (котлованы)','Повторное заземление опор (котлованы)','Повторное заземление опор']","gz:['повторное заземление (комплект)','Схема: повторное заземление (комплект)','Повторное заземление (комплект)','Повторное заземление (комплект)']",1),
('<option value="gz">повторное заземление (котлованы)</option>','<option value="gz">повторное заземление (комплект)</option>',1),
]
for a,b,n in R:
  c=t.count(a)
  if c!=n:sys.exit(f'{c}x: {a[:70]}')
  t=t.replace(a,b)
open(f,'w').write(t);print('ok')
