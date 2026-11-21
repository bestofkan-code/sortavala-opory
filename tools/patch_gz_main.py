# Основная карта, блок хода работ: строка «Котлованы под заземление — N из 92» (работа 11; 92 комплекта по смете).
import sys
p=sys.argv[1];s=open(p,encoding='utf-8').read()
a="+sip+'<small style=\"color:#555;display:block;margin:-2px 0 4px\">Светильники, кронштейны и СИП — из сметы"
assert s.count(a)==1,s.count(a)
s=s.replace(a,"+sip+ln('Котлованы под заземление',B.filter(p=>wdone(p,11)).length,92,'#a16207')+'<small style=\"color:#555;display:block;margin:-2px 0 4px\">Светильники, кронштейны и СИП — из сметы")
b="(831 шт., 353/50/189 шт., 16 664 м)."
assert s.count(b)==1
s=s.replace(b,"(831 шт., 353/50/189 шт., 16 664 м), котлованы под заземление — по числу комплектов повторного заземления (92).")
open(p,'w',encoding='utf-8').write(s);print('ok gz',p)
