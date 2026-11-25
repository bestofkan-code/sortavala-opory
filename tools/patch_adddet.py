import re,sys
FILES=['redaktor.html','prosmotr.html','montazh.html','zamechaniya.html','zamechaniya-prosmotr.html','uchastki.html']
END='<option value="A">анкерная</option></select></div>'
for f in FILES:
    s=open(f,encoding='utf-8').read()
    if 'id="addd"' in s: print('skip',f); continue
    i=s.find('Режим «Добавить»'); a=s.rfind('<small',0,i); b=s.find(END,a)
    if i<0 or b<0 or s.count('Режим «Добавить»')!=1: sys.exit(f+' anchors')
    e=b+len(END); seg=s[a:e]
    if len(re.findall(r'<div\b',seg))!=seg.count('</div>'): sys.exit(f+' unbalanced')
    s=s[:a]+'<details id="addd"><summary style="font-size:12px;color:#9aa3b5;cursor:pointer;margin:4px 0">Добавление опор и быстрая отметка работ</summary>'+seg+'</details>'+s[e:]
    open(f,'w',encoding='utf-8').write(s); print('ok',f)
