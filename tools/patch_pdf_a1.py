import sys
FILES=['redaktor.html','prosmotr.html','montazh.html','zamechaniya.html','zamechaniya-prosmotr.html','uchastki.html']
R=[("const A3=o.paper=='A3',u=250/25.4,CW=Math.round((A3?420:297)*u),CH=Math.round((A3?297:210)*u)",
    "const A1=o.paper=='A1',A3=o.paper=='A3'||A1,u=(A1?200:250)/25.4,CW=Math.round((A1?841:A3?420:297)*u),CH=Math.round((A1?594:A3?297:210)*u)"),
   ("let L2=wrap('План-схема участка работ: опоры, кронштейны, СИП-4 4×25',66*u)","let L2=wrap(o.kro?'План-схема: опоры и кронштейны по типам':'План-схема участка работ: опоры, кронштейны, СИП-4 4×25',66*u)"),
   ("SH.forEach(p=>dpole(g,...C(p.lat,p.lon),o.kro?{uid:'p0',t:p.t,kr:p.kr,ka:p.ka,w:{12:'x'}}:p,r));","SH.forEach(p=>dpole(g,...C(p.lat,p.lon),o.kro?{uid:'p0',t:'S',kr:p.kr,ka:p.ka,w:{12:'x'}}:p,r));"),
   ("async function pdfPlan(){const st=$('pst'),A3=$('pq').value=='A3';","async function pdfPlan(){const st=$('pst'),A1=$('pq').value=='A1',A3=$('pq').value=='A3';"),
   ("paper:$('pq').value,base:$('pbm').value,max:170,","paper:$('pq').value,base:$('pbm').value,max:A1?700:170,"),
   ('<select id="pq"><option value="A3">A3 (250 dpi)</option>','<select id="pq"><option value="A3">A3 (250 dpi)</option><option value="A1">A1 (200 dpi)</option>'),
]
for f in FILES:
    s=open(f,encoding='utf-8').read()
    for a,b in R:
        if s.count(a)!=1: sys.exit(f'{f}: {a[:50]} count {s.count(a)}')
        s=s.replace(a,b)
    # pdfPlan's jsPDF format/size (first occurrence after pdfPlan start)
    i=s.find('async function pdfPlan(){'); j=s.find("format:A3?'a3':'a4',compress:true});doc.addImage(cv.toDataURL('image/jpeg',.92),'JPEG',0,0,A3?420:297,A3?297:210);",i)
    k=s.find('$(\'pdfb\').onclick=pdfPlan',i)
    if j<0 or j>k: sys.exit(f+' pdfPlan format')
    old="format:A3?'a3':'a4',compress:true});doc.addImage(cv.toDataURL('image/jpeg',.92),'JPEG',0,0,A3?420:297,A3?297:210);"
    new="format:A1?'a1':A3?'a3':'a4',compress:true});doc.addImage(cv.toDataURL('image/jpeg',.9),'JPEG',0,0,A1?841:A3?420:297,A1?594:A3?297:210);"
    s=s[:j]+new+s[j+len(old):]
    open(f,'w',encoding='utf-8').write(s); print('ok',f)
