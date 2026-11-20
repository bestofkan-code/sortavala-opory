# Пометка «нужна вертикальная разметка 2.1.3» (поле poles.rz): галочка в карточке опоры (редактор), значок на опоре
# (квадрат с чёрно-белыми полосами справа внизу), фильтр «Только разметка 2.1.3», строка в окне просмотра, символ и строка легенды в PDF.
import sys
p=sys.argv[1];s=open(p,encoding='utf-8').read()
def R(a,b,n=1):
    global s
    assert s.count(a)==n,(a[:90],s.count(a));s=s.replace(a,b)
# синхронизация
R("vk:!!p.vk,h:+p.h||8,","vk:!!p.vk,rz:!!p.rz,h:+p.h||8,")
R("vk:!!r.vk,h:+r.h||8,","vk:!!r.vk,rz:!!r.rz,h:+r.h||8,")
# карточка редактора
R("<input type=checkbox data-vk ${p.vk?'checked':''}> <b style=\"color:#e879f9\">ввод КЛ</b></label>",
  "<input type=checkbox data-vk ${p.vk?'checked':''}> <b style=\"color:#e879f9\">ввод КЛ</b></label><label title=\"Опора близко к дороге — нанести вертикальную разметку 2.1.3 (ГОСТ Р 52289-2019 п. 6.3.2)\"><input type=checkbox data-rz ${p.rz?'checked':''}> <b style=\"color:#facc15\">разметка 2.1.3</b></label>")
R("d.querySelector('[data-f]').onchange=e=>{",
  "{const e=d.querySelector('[data-rz]');if(e)e.onchange=()=>{PSEL=Date.now();p.rz=e.checked;ch();upd(p);stats();toast(p.id+(p.rz?': нужна разметка 2.1.3':': разметка 2.1.3 не нужна'))}} d.querySelector('[data-f]').onchange=e=>{",1)
# значок на карте
RZ='<g transform="translate(12 12)"><rect x="-5.5" y="-5.5" width="11" height="11" rx="1" fill="#fff" stroke="#111" stroke-width="1.4"/><path d="M-5.5 0.5L0.5-5.5M-5.5 5.5L5.5-5.5M-0.5 5.5L5.5-0.5" stroke="#111" stroke-width="2.1"/></g>'
R("v+=vfBadg","if(p.rz&&!p.x)v+='"+RZ+"';v+=vfBadg")
# PDF (canvas)
R("if(p.vk&&!p.x){g.strokeStyle='#c026d3';g.lineWidth=lw*.9;g.beginPath();g.arc(x,y,r*1.85,0,7);g.stroke();g.fillStyle='#c026d3';g.fillRect(x-r*2.3,y-r*2.3,r*1.1,r*1.1)}}",
  "if(p.vk&&!p.x){g.strokeStyle='#c026d3';g.lineWidth=lw*.9;g.beginPath();g.arc(x,y,r*1.85,0,7);g.stroke();g.fillStyle='#c026d3';g.fillRect(x-r*2.3,y-r*2.3,r*1.1,r*1.1)}"
  "if(p.rz&&!p.x){const a=r*.75,cx=x+r*1.55,cy=y+r*1.55;g.save();g.fillStyle='#fff';g.fillRect(cx-a,cy-a,2*a,2*a);g.beginPath();g.rect(cx-a,cy-a,2*a,2*a);g.clip();g.strokeStyle='#111';g.lineWidth=a*.42;g.beginPath();for(const k of[-1,0,1]){g.moveTo(cx-a+k*a,cy+a+k*a);g.lineTo(cx+a+k*a,cy-a+k*a)}g.stroke();g.restore();g.strokeStyle='#111';g.lineWidth=Math.max(1,a*.22);g.strokeRect(cx-a,cy-a,2*a,2*a)}}")
R("['Опора ввода КЛ (люк)',{t:'S',vk:1}]]","['Опора ввода КЛ (люк)',{t:'S',vk:1}],['Нужна разметка 2.1.3',{t:'S',rz:1}]]",2)
# окно просмотра
R("${p.vk?' · <b style=\"color:#c026d3\">ввод КЛ</b>':","${p.rz&&!p.x?' · <b style=\"color:#a16207\">разметка 2.1.3</b>':''}${p.vk?' · <b style=\"color:#c026d3\">ввод КЛ</b>':")
# фильтр
R('<div class="r"><button class="b" id="vkb" style="border-color:#c026d3">Только ввод КЛ</button><small id="vks"></small></div>',
  '<div class="r"><button class="b" id="vkb" style="border-color:#c026d3">Только ввод КЛ</button><small id="vks"></small></div><div class="r"><button class="b" id="rzb" style="border-color:#facc15">Только разметка 2.1.3</button><small id="rzs"></small></div>')
R("function vis(p){return ftyOk(p)&&visB(p)&&(!VKF||vkOk(p))&&","function vis(p){return ftyOk(p)&&visB(p)&&(!VKF||vkOk(p))&&(!RZF||rzOk(p))&&")
R("var VKF=false;","var RZF=false;try{RZF=localStorage.getItem(KEY+'_rzf')==='1'}catch(e){}\nfunction rzOk(p){return !!p.rz&&!p.x}\nfunction rzUI(){const b=$('rzb');if(!b)return;b.style.background=RZF?'#facc15':'';b.style.color=RZF?'#111':'';b.textContent=RZF?'Показана только разметка 2.1.3 ✕':'Только разметка 2.1.3';const n=P.filter(p=>rzOk(p)&&tpOk(p)).length;$('rzs').innerHTML=n?'отмечено опор: <b>'+n+'</b>':'пока не отмечено'}\n"
  "setTimeout(()=>{const b=$('rzb');if(!b)return;b.onclick=()=>{RZF=!RZF;try{localStorage.setItem(KEY+'_rzf',RZF?'1':'0')}catch(e){}rzUI();P.forEach(upd);numLabels();if(RZF){const L2=P.filter(p=>rzOk(p)&&tpOk(p));if(L2.length)map.fitBounds(L.latLngBounds(L2.map(p=>[p.lat,p.lon])).pad(.15),{maxZoom:17});else toast('Опор с пометкой «разметка 2.1.3» нет')}};rzUI()},0);\n"
  "var VKF=false;")
R("{const _st2=stats;stats=function(){const r=_st2.apply(this,arguments);try{vkUI()}cat","{const _st2=stats;stats=function(){const r=_st2.apply(this,arguments);try{rzUI()}catch(e){}try{vkUI()}cat")
R("if(v('VKF'))a.push('ввод КЛ');","if(v('VKF'))a.push('ввод КЛ');if(v('RZF'))a.push('разметка 2.1.3');")
open(p,'w',encoding='utf-8').write(s);print('ok rz',p)
