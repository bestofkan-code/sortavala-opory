#!/usr/bin/env python3
"""Монтажная карта, панель бригады: «Светильников установлено» — штук по кронштейнам (lumI), а не опор;
план — по кронштейнам опор в выборке (2-рожк. = 2, 1-рожк. = 1). Кронштейны — опоры с кронштейном в выборке.
Применение: python3 tools/patch_crewlum.py montazh.html"""
import sys
p=sys.argv[1];s=open(p,encoding='utf-8').read()
old="row('Кронштейн установлен',c(Q,12),NP,'#60a5fa',12)+row('Светильник установлен',c(Q,6),NP,'#facc15',6)"
if old not in s: print('skip',p);sys.exit(0)
new=("row('Кронштейнов установлено',c(Q,12),Q.filter(p=>+p.kr>0).length,'#60a5fa',12)"
     "+row('Светильников установлено (шт.)',Q.reduce((t,p)=>t+lumI(p),0),Q.reduce((t,p)=>t+(+p.kr==2?2:+p.kr==1?1:0),0),'#facc15',6)")
s=s.replace(old,new);open(p,'w',encoding='utf-8').write(s);print('ok',p)
