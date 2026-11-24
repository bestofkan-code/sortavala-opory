#!/usr/bin/env python3
"""Светильники считаются по кронштейну: на опоре с отметкой «Установлен светильник»
2-рожковый кронштейн = 2 светильника, 1-рожковый = 1 (без кронштейна — по полю «Светильн.», минимум 1).
Функция lumI(p) — везде, где считались установленные светильники. При отметке светильника и при смене
кронштейна поле sv выставляется по кронштейну.
Применение: python3 tools/patch_lumcount.py <file.html>
"""
import sys
path=sys.argv[1];s=open(path,encoding='utf-8').read()
if 'function lumI(' in s: print('already',path);sys.exit(0)
def R(old,new,need=1):
    global s
    n=s.count(old);assert n>=need,(path,old[:60],n);s=s.replace(old,new);return n
R("function ready(p){const n=Math.max(1,+p.kr||0);return !!p.done&&!p.x&&(+p.sv||0)>=n&&(+p.sv||0)>0}",
  "function lumI(p){return wdone(p,6)?(+p.kr==2?2:+p.kr==1?1:Math.max(1,+p.sv||1)):0}\nfunction ready(p){const n=Math.max(1,+p.kr||0);return !!p.done&&!p.x&&lumI(p)>=n}")
R("(wdone(p,6)?(+p.sv||Math.max(1,+p.kr||1)):0)","lumI(p)",0)
R("wdone(p,6)?(+p.sv||Math.max(1,+p.kr||1)):''","(lumI(p)||'')",0)
R("wdone(p,6)?(+p.sv||Math.max(1,+p.kr||1)):0","lumI(p)",0)
R("sv=A.reduce((a,p)=>a+(+p.sv||0),0)","sv=A.reduce((a,p)=>a+lumI(p),0)")
R("o.zoi+=3*(+p.sv||Math.max(1,+p.kr||1))","o.zoi+=3*(+p.kr==2?2:+p.kr==1?1:Math.max(1,+p.sv||1))",0)
R("sv=Math.min(2,+p.sv||0)","sv=Math.min(2,lumI(p)||+p.sv||0)",0)
R("if(k==6){if(on&&!(+p.sv))p.sv=Math.max(1,+p.kr||1);if(!on)p.sv=0}","if(k==6){if(on)p.sv=Math.max(1,+p.kr||1);if(!on)p.sv=0}")
R("p.kr=+a;p.ka=b?+b:null;krSel();","p.kr=+a;p.ka=b?+b:null;if(wdone(p,6))p.sv=Math.max(1,p.kr||1);krSel();")
open(path,'w',encoding='utf-8').write(s);print('ok',path)
