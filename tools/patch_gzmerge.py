import sys
FILES=['redaktor.html','prosmotr.html','montazh.html','zamechaniya.html','zamechaniya-prosmotr.html','uchastki.html']
R=[('[11, "Котлован под заземление"], [15, "Повторное заземление"], ','[11, "Повторное заземление"], ',1),
   ("[11,'Котлован под заземление']","[11,'Повторное заземление']",1),
   ('title="Показать только опоры, где котлован под заземление ещё не выкопан"','title="Показать только опоры, где повторное заземление ещё не выполнено"',1),
   ("row('Котлован под заземление',","row('Повторное заземление',",0),
   ("toast(GZF==1?'Все котлованы под заземление выкопаны'","toast(GZF==1?'Повторное заземление выполнено на всех опорах'",1)]
for f in FILES:
    s=open(f,encoding='utf-8').read()
    for a,b,req in R:
        c=s.count(a)
        if req and c!=1: sys.exit(f'{f}: {a[:40]} count {c}')
        s=s.replace(a,b)
    open(f,'w',encoding='utf-8').write(s); print('ok',f)
