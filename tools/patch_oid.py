# Перенумерация опор 22.11.2026: в карточке опоры рядом с номером — прежний номер (колонка poles.oid), «был ТП57-30».
# Откат нумерации на сервере: select public.renum_rollback();  (копия — таблица poles_renum_backup, соответствие — poles_renum_map)
import sys
p=sys.argv[1];s=open(p,encoding='utf-8').read()
OLD="${p.oid&&p.oid!==p.id?' <small style=\"color:#64748b\" title=\"Номер до перенумерации 22.11.2026\">был '+esc(p.oid)+'</small>':''}"
n=0
if 'p.oid&&p.oid!==p.id' not in s:
  for a in ["<div><b>${esc(p.id)}</b> <small>лин.","<b data-pid>${esc(p.id)}</b>"]:
    c=s.count(a); n+=c
    s=s.replace(a, a.replace("</b>","</b>"+OLD,1))
# fromRow: прежний номер из базы (только чтение, rowOf его не отправляет)
fr="date:r.date||'',note:r.note||''});"
if "oid:r.oid" not in s:
  assert s.count(fr)==1,(p,s.count(fr)); s=s.replace(fr,"date:r.date||'',note:r.note||'',oid:r.oid||''});"); n+=1
open(p,'w',encoding='utf-8').write(s);print('ok oid',p,n)
