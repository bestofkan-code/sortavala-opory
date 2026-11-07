# Отдельная работа 14 «Подрезка крон (бригада)»: своя отметка, свои фото (k=14), свой фотоотчёт в карте бригады.
import sys
p=sys.argv[1];s=open(p,encoding='utf-8').read()
def R(a,b,n=1):
    global s
    assert s.count(a)==n,(a[:90],s.count(a));s=s.replace(a,b)
R('[9, "Подрезка крон деревьев"], [13, "Вывоз отходов"]];','[9, "Подрезка крон деревьев"], [14, "Подрезка крон (бригада)"], [13, "Вывоз отходов"]];')
R("9:'Подрезка крон',13:'Вывоз отходов'};","9:'Подрезка крон',14:'Подрезка (бриг.)',13:'Вывоз отходов'};")
# карточка редактора: кнопка фото и блок фото для 14
R("${k==9?`<button class=\"wph\" data-wph title=\"Фото до и после\">${ppIco}${ppN(p.uid,9)||''}</button>`:''}",
  "${k==9||k==14?`<button class=\"wph\" data-wph=${k} title=\"Фото до и после\">${ppIco}${ppN(p.uid,k)||''}</button>`:''}")
R("if(k==9)setTimeout(()=>phb._r(),0);sync2();","if(k==9)setTimeout(()=>phb._r(),0);if(k==14)setTimeout(()=>phb2._r(),0);sync2();")
R("const wp=g.querySelector('[data-wph]');if(wp)wp.onclick=()=>{PHO=!PHO;phb._r()}};let PHO=false;const phb=d.querySelector('[data-phb]');ppBlock(phb,p,9,()=>PHO);",
  "g.querySelectorAll('[data-wph]').forEach(wp=>wp.onclick=()=>{if(wp.dataset.wph=='14'){PHO2=!PHO2;phb2._r()}else{PHO=!PHO;phb._r()}})};let PHO=false,PHO2=false;const phb=d.querySelector('[data-phb]'),phb2=d.querySelector('[data-phb2]');ppBlock(phb,p,9,()=>PHO);ppBlock(phb2,p,14,()=>PHO2);")
R("<div class=\"phb\" data-phb hidden></div>\n<div class=\"g2i\">","<div class=\"phb\" data-phb hidden></div><div class=\"phb\" data-phb2 hidden></div>\n<div class=\"g2i\">")
R("box.innerHTML='<div class=\"phh\">Подрезка крон — фото'","box.innerHTML='<div class=\"phh\">'+(k==14?'Подрезка крон (бригада) — фото':'Подрезка крон — фото')")
# просмотр: фото бригады тоже
R("if(RO&&ppL(p.uid,9).length){const b=document.createElement('div');b.className='phb';d.appendChild(b);ppBlock(b,p,9,()=>true)}",
  "if(RO)[9,14].forEach(k=>{if(ppL(p.uid,k).length){const b=document.createElement('div');b.className='phb';d.appendChild(b);ppBlock(b,p,k,()=>true)}});")
# фотоотчёт: ключ работы в переменной PRK (в карте бригады — 14)
a=s.index('async function ppReport(');b=s.index("$('ppr').onclick",a);t=s[a:b]
n0=t.count('(p,9)')+t.count('(p.uid,9')
t=t.replace('wdone(p,9)','wdone(p,PRK)').replace('wd(p,9)','wd(p,PRK)').replace('ppN(p.uid,9)','ppN(p.uid,PRK)').replace('ppL(p.uid,9,kind)','ppL(p.uid,PRK,kind)')
assert '(p,9)' not in t and '(p.uid,9' not in t,t
s=s[:a]+'var PRK=9,PRT=\'Фотоотчёт: подрезка крон деревьев\';\n'+t.replace("g.fillText('Фотоотчёт: подрезка крон деревьев',50,62)","g.fillText(PRT,50,62)").replace("doc.save('Фотоотчёт подрезка крон '+per+'.pdf')","doc.save(PRT.replace(':','')+' '+per+'.pdf')")+s[b:]
open(p,'w',encoding='utf-8').write(s);print('ok tree14, replaced',n0)
