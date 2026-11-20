# PDF-план: исключённые опоры (p.x) не рисуются и не попадают в границы плана и легенду.
# Линии СИП, идущие через исключённые опоры «СИП по ней» (p.sx), остаются.
import sys
p=sys.argv[1];s=open(p,encoding='utf-8').read()
def R(a,b):
    global s
    assert s.count(a)==1,(a[:80],s.count(a));s=s.replace(a,b)
R("const SH=o.only||P,SHS=new Set(SH),lw=.3*u,U=new Map(SH.map(p=>[p.uid,p]))",
  "const SH0=o.only||P,SHL=SH0.filter(p=>!p.x||p.sx),SH=SH0.filter(p=>!p.x),SHS=new Set(SHL),lw=.3*u,U=new Map(SHL.map(p=>[p.uid,p]))")
R("const BB=o.bb||{s:Math.min(...P.map(p=>p.lat)),n:Math.max(...P.map(p=>p.lat)),w:Math.min(...P.map(p=>p.lon)),e:Math.max(...P.map(p=>p.lon))}",
  "const PB=P.filter(p=>!p.x),BB=o.bb||{s:Math.min(...PB.map(p=>p.lat)),n:Math.max(...PB.map(p=>p.lat)),w:Math.min(...PB.map(p=>p.lon)),e:Math.max(...PB.map(p=>p.lon))}")
R("['Исключена из проекта',{t:'S',x:1}],['Исключена, СИП по ней',{t:'S',x:1,sx:1}],","")
R("L2=P.filter(p=>tpOk(p)&&(!sp||vis(p)));","L2=P.filter(p=>!p.x&&tpOk(p)&&(!sp||vis(p)));")
R("const L2=P.filter(p=>worked(p)&&tpOk(p)&&wmatch(p));","const L2=P.filter(p=>!p.x&&worked(p)&&tpOk(p)&&wmatch(p));")
open(p,'w',encoding='utf-8').write(s);print('ok noexcl',p)
