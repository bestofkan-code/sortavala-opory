# Собирает montazh.html (карта бригады монтажников) из redaktor.html.
# Бригада видит всю карту, но отмечает только: подрезку крон (9), кронштейн (12), СИП (5), светильник (6),
# длину СИП по пролётам и бронекабель на ТП. Ограничения дублируются на сервере (роль crew в Supabase).
import sys,os
src,dst=sys.argv[1],sys.argv[2];s=open(src,encoding='utf-8').read()
JS=open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'crew.js'),encoding='utf-8').read()
def R(a,b,n=1):
    global s
    assert s.count(a)==n,(a[:90],s.count(a));s=s.replace(a,b)
R("<title>Карта опор — Сортавала</title>","<title>Монтаж — карта бригады, Сортавала</title>")
R("KEY='sortavala_opory_v1'","KEY='sortavala_opory_crew_v1'")
R("<script>document.body.classList.add('dk')</script>","<script>document.body.classList.add('dk','crew')</script>")
R("#skn{display:block;opacity:.75;margin:2px 0 3px;line-height:1.3}</style></head><body>",
  "#skn{display:block;opacity:.75;margin:2px 0 3px;line-height:1.3}"
  ".cri{font-size:12px;margin:3px 0;line-height:1.35}.cri button{padding:1px 6px;margin:0 0 0 4px}"
  "#crw .crr{display:flex;align-items:baseline;gap:6px;font-size:13px;margin-top:7px}#crw .crr span{flex:1}#crw .crr small{color:#4ade80}#crw .crr b{white-space:nowrap}"
  "#crw .crb2{height:7px;background:#262c3d;border-radius:4px;overflow:hidden;margin:3px 0 0}#crw .crb2 i{display:block;height:100%}"
  "#crw .crt{width:100%;border-collapse:collapse;font-size:12px;margin-top:9px}#crw .crt th,#crw .crt td{padding:3px 4px;text-align:right;border-bottom:1px solid rgba(127,127,127,.22)}#crw .crt th:first-child,#crw .crt td:first-child{text-align:left}"
  ".crb{font-size:12px;margin:5px 0;padding:6px 8px;border:1px solid #c026d3;border-radius:8px;background:rgba(192,38,211,.12);line-height:1.35}"
  "body.crew #skd,body.crew #bar,body.crew #st,body.crew .ed:not(.crk),body.crew #lmh,body.crew #spp,body.crew .crh{display:none!important}"
  "body.crew #modes [data-m]:not([data-m=view]):not([data-m=mark]){display:none}"
  "</style></head><body>")
R('<b style="font-size:15px">Опоры освещения, Сортавала</b>',
  '<b style="font-size:15px">Монтаж: СИП, кронштейны, светильники, бронекабель</b><div class="crb">Карта бригады монтажников. Нажмите на опору — отметьте выполненные работы. На линию СИП — впишите длину пролёта. На значок ТП — бронекабель. Все отметки сразу видны на основной карте.</div>')
R('<h3>Ход работ</h3>','<h3>Ход работ бригады</h3><div id="crw"></div>')
R('<div class="ed"><h3>Режим</h3>','<div class="ed crk"><h3>Режим</h3>')
R('data-m="view">Просмотр</button>','data-m="view">Карточки опор</button>')
R('data-m="mark">Отметить установку</button>','data-m="mark">Быстрая отметка</button>')
R('<small>Режим «Добавить»:','<small class="crh">Режим «Добавить»:')
R('<div class="r">Вид работ при отметке:','<small style="display:block">«Быстрая отметка»: выберите вид работ и нажимайте на опоры подряд — отметка ставится и снимается одним нажатием.</small><div class="r">Вид работ при отметке:')
R('<div class="r">Новая опора: <select id="nh">','<div class="r crh">Новая опора: <select id="nh">')
R('<div class="ed"><h3>Отмена действий</h3>','<div class="ed crk"><h3>Отмена действий</h3>')
# вход
R("var USERS=[['Иль','il'],['Никита','nikita'],['Леонид','leonid'],['Женя','zhenya']]","var USERS=[['Начальник участка','montazh']]")
R("<b style=\"font-size:16px\">Вход в редактор карты опор</b>","<b style=\"font-size:16px\">Вход в карту монтажа</b>")
# виды работ
R("$('mw').innerHTML=WK.map(([k,n])=>'<option value=\"'+k+'\"'+(k==4?' selected':'')+'>'+n+'</option>').join('');",
  "var CW=[9,12,5,6];$('mw').innerHTML=WK.filter(([k])=>CW.includes(k)).map(([k,n])=>'<option value=\"'+k+'\"'+(k==5?' selected':'')+'>'+n+'</option>').join('');")
R("$('wf').innerHTML=WK.map(([k,n])=>","$('wf').innerHTML=WK.filter(([k])=>CWF.includes(k)).map(([k,n])=>")
R("if(mode=='mark'){const k=+$('mw').value;setW(p,k,!wdone(p,k),$('md').value);upd(p);save();stats();mark(p)}",
  "if(mode=='mark'){const k=+$('mw').value;if(!CW.includes(k))return;crewW(p,k,!wdone(p,k),$('md').value||LD());upd(p);save();stats();mark(p);toast(p.id+': '+(WSN[k]||'')+(wdone(p,k)?' ✓':' — отметка снята'))}")
R("function popup0(p){if(RO)return roPopup(p);","function popup0(p){if(RO)return roPopup(p);return crewCard(p);")
R("function stats(){try{paInfo()}catch(e){}","function stats(){try{crewStats()}catch(e){}try{paInfo()}catch(e){}")
# пролёт СИП: без правки линий, с отметкой «СИП» на обеих опорах
R("+'<div class=\"r\" style=\"margin-top:6px;border-top:1px solid #2c3346;padding-top:6px\"><button data-lp>Изменить путь</button><button data-ld style=\"color:#f87171\">Удалить линию</button>'+(LE.has(k)?'<button data-lr>Как было</button>':'')+'</div>');",
  "+'<label style=\"display:block;margin-top:6px;font-size:12px\"><input type=checkbox data-s5 checked> отметить «СИП» на обеих опорах пролёта</label>');")
R("if(!RO){d.querySelector('[data-lp]').onclick=()=>{map.closePopup();leEdit(k)};d.querySelector('[data-ld]').onclick=()=>{if(!confirm('Удалить линию '+z.name+' с карты?'))return;map.closePopup();leDel(k)};const lr=d.querySelector('[data-lr]');if(lr)lr.onclick=()=>{map.closePopup();leSet(k,null);toast('Линия '+z.name+' возвращена как было')};",
  "if(!RO){")
R("SP.set(k,row);SPQ[k]=row;spSave();lines();stats();map.closePopup();spSend();",
  "SP.set(k,row);SPQ[k]=row;spSave();{const s5=d.querySelector('[data-s5]');if(s5&&s5.checked)[z.ua,z.ub].forEach(u=>{const q=P.find(o=>o.uid==u);if(q&&!wdone(q,5)){crewW(q,5,true,row.sd||LD());upd(q);save();mark(q)}})}lines();stats();map.closePopup();spSend();")
# бронекабель: путь не правим
R("+(RO?'':'<button data-ce>Изменить путь</button>')+","+")
R("if(!RO)d.querySelector('[data-ce]').onclick=()=>{map.closePopup();leEdit(k)};","")
# ТП: только «Проложен бронекабель» и длина
R("'<div class=\"wl\">'+TW.map(([k,n])=>'<label><input type=checkbox data-tw='","'<div class=\"wl\">'+TW.filter(([k])=>k==1).map(([k,n])=>'<label><input type=checkbox data-tw='")
R("+'<input type=\"text\" data-tn placeholder=\"Примечание по ТП\" value=\"'+esc(r.note||'')+'\">'","+(r.note?'<div class=\"cri\">Примечание: '+esc(r.note)+'</div>':'')")
R("+'<small>Переместить значок ТП: режим «Правка/перенос», затем перетащите.</small>')","+'<small>Отметьте, когда бронекабель от ТП до опоры ввода проложен, и впишите фактическую длину.</small>')")
R("d.querySelector('[data-tn]').onchange=e=>tpPut(t,{note:e.target.value.trim()})}","}")
# логика бригады
R("$('fjb').onclick=",JS+"\n$('fjb').onclick=")
open(dst,'w',encoding='utf-8').write(s);print('ok crew ->',dst)
