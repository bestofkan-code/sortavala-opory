import sys
f='redaktor.html';t=open(f).read()
R=[
("function kmShow(m,p){if(m=='ks')","function kmShow(m,p){if(m=='cz')return wdone(p,16);if(m=='ks')",1),
("function kmPole(m,p){if(m=='ks')","function kmPole(m,p){if(m=='cz')return{uid:'p0',t:'S',done:true};if(m=='ks')",1),
("function kmLeg(m){const N=['n','Номер опоры'],O=['p','Опора',{t:'S'}];","function kmLeg(m){const N=['n','Номер опоры'],O=['p','Опора',{t:'S'}];if(m=='cz')return[['p','Цоколь установлен (опора залита зеленым)',{t:'S',done:true}],N];",1),
("ks:['выполненные работы на опорах',","cz:['установленные цоколи','Схема: установленные цоколи опор','Установленные цоколи опор','Установленные цоколи'],ks:['выполненные работы на опорах',",1),
('<option value="ks">','<option value="cz">установленные цоколи</option><option value="ks">',1),
]
for a,b,n in R:
  c=t.count(a)
  if c!=n:sys.exit(f'{c}x: {a[:60]}')
  t=t.replace(a,b)
open(f,'w').write(t);print('ok')
