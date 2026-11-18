# ТП: короткое название работы 2 — «Установлен ШУНО» (не обрезается в окне ТП)
import sys
fn=sys.argv[1];s=open(fn,encoding='utf-8').read()
a="var TW=[[1,'Проложен бронекабель'],[2,'Установлен шкаф управления']]"
assert s.count(a)==1;s=s.replace(a,"var TW=[[1,'Проложен бронекабель'],[2,'Установлен ШУНО']]")
open(fn,'w',encoding='utf-8').write(s);print('ok')
