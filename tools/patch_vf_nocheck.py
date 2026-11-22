# Сверка на месте: зелёная галочка у сверенной опоры на карте не рисуется.
# Остаются: красный крестик — не сверена, оранжевый «!» — сверена с расхождением.
import sys
p=sys.argv[1];s=open(p,encoding='utf-8').read()
if 'vfBad(p);if(!b)return' in s: print('already',p);sys.exit(0)
a="const b=vfBad(p),x=(typeof mode!='undefined'&&mode=='sp')?17:12.5,"
assert s.count(a)==1,(p,s.count(a))
s=s.replace(a,"const b=vfBad(p);if(!b)return '';const x=(typeof mode!='undefined'&&mode=='sp')?17:12.5,")
open(p,'w',encoding='utf-8').write(s);print('ok vf_nocheck',p)
