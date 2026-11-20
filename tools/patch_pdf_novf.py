# PDF-план: сверка не учитывается — фильтр «Не сверены котлованы» не влияет на состав плана и имя файла
# (значок сверки на PDF-плане и так не рисуется: dpole его не выводит).
import sys
p=sys.argv[1];s=open(p,encoding='utf-8').read()
def R(a,b):
    global s
    assert s.count(a)==1,(a[:80],s.count(a));s=s.replace(a,b)
R("if(v('VS'))a.push('не сверены котлованы');","")
R("function pdfArea0(){","function pdfVis(p){const s0=VS;VS=false;try{return vis(p)}finally{VS=s0}}\nfunction pdfArea0(){")
R("L2=P.filter(p=>!p.x&&tpOk(p)&&(!sp||vis(p)));","L2=P.filter(p=>!p.x&&tpOk(p)&&(!sp||pdfVis(p)));")
open(p,'w',encoding='utf-8').write(s);print('ok novf',p)
