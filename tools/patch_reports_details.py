import re,sys
FILES=['redaktor.html','prosmotr.html','montazh.html','zamechaniya.html','zamechaniya-prosmotr.html','uchastki.html']
START='<h3>Печать карты в PDF</h3>'
ENDK='<small>Изменения хранятся в этом браузере. Чтобы перенести на другое устройство, сохраните данные в файл и загрузите там.</small></div>'
for f in FILES:
    s=open(f,encoding='utf-8').read()
    if 'id="rpd"' in s: print('skip',f); continue
    a=s.find(START); b=s.find(ENDK)
    if a<0 or b<0 or s.count(START)!=1 or s.count(ENDK)!=1: sys.exit(f+' anchors')
    e=b+len(ENDK); seg=s[a:e]
    if len(re.findall(r'<div\b',seg))!=seg.count('</div>'): sys.exit(f+' unbalanced')
    s=s[:a]+'<details id="rpd" class="rpd"><summary><b>Отчёты</b><small style="opacity:.7;margin-left:6px">печать, PDF, отчёт, база, данные</small></summary>'+seg+'</details>'+s[e:]
    open(f,'w',encoding='utf-8').write(s); print('ok',f)
