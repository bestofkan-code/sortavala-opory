# Основная карта: режим «Задания бригаде» — выделить опоры (нажатием или обводом участка), виды работ, срок → таблица crew_tasks.
import sys,os
p=sys.argv[1];s=open(p,encoding='utf-8').read()
JS=open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'tasks.js'),encoding='utf-8').read()
def R(a,b,n=1):
    global s
    assert s.count(a)==n,(a[:90],s.count(a));s=s.replace(a,b)
R("#sps div{margin:2px 0;font-size:12px}","#sps div{margin:2px 0;font-size:12px}"
  "#tkp{margin-top:6px;border:1px solid #22d3ee;border-radius:8px;padding:6px 8px}#tkp[hidden]{display:none}#tkp input[type=text]{width:100%;box-sizing:border-box;margin:3px 0}"
  "#tkw{flex-wrap:wrap;gap:4px}#tkw label{border:1px solid #4b5468;border-radius:10px;padding:2px 8px;font-size:12px;cursor:pointer}#tkw label:has(input:checked){border-color:#22d3ee;background:rgba(34,211,238,.18)}"
  ".tki2{border:1px solid rgba(127,127,127,.35);border-radius:8px;padding:5px 7px;margin:6px 0;font-size:12.5px}.tki2.dn{opacity:.55}.tki2>small{display:block;opacity:.85;margin-top:2px}"
  ".tkb{height:6px;background:#262c3d;border-radius:3px;overflow:hidden;margin:4px 0}.tkb i{display:block;height:100%;background:#22d3ee}.tki2 .r{margin-top:4px}.tki2 .r button{padding:3px 8px}")
R('<button class="b" data-m="sp" style="border-color:#f59e0b">Совм. подвеска</button>',
  '<button class="b" data-m="sp" style="border-color:#f59e0b">Совм. подвеска</button><button class="b" data-m="task" style="border-color:#22d3ee">Задания бригаде</button>')
R('<small id="sqrs" style="display:block"></small><div id="sps"></div></div>',
  '<small id="sqrs" style="display:block"></small><div id="sps"></div></div>'
  '<div id="tkp" hidden><b>Задания бригаде монтажников</b><small style="display:block;margin:2px 0 4px">Нажимайте на опоры — добавить или убрать из задания, или обведите участок. Сохранённое задание сразу появится на монтажной карте у начальника участка.</small>'
  '<div class="r"><button id="tka">Обвести участок</button><button id="tkok" hidden>Готово</button><button id="tkun" hidden>↶ точка</button><button id="tkc">Очистить</button></div><small id="tki" style="display:block"></small>'
  '<input type="text" id="tkn" placeholder="Название, например: ул. Победы, ТП90">'
  '<div id="tkw" class="r"><label><input type="checkbox" data-k="5"> СИП</label><label><input type="checkbox" data-k="12"> Кронштейн</label><label><input type="checkbox" data-k="6"> Светильник</label><label><input type="checkbox" data-k="14"> Подрезка крон</label><label><input type="checkbox" data-k="100"> Бронекабель</label></div>'
  '<div class="r">Срок: с <input type="date" id="tk1"> по <input type="date" id="tk2"></div><input type="text" id="tkt" placeholder="Примечание для бригады">'
  '<div class="r"><button id="tks">Сохранить задание</button><button id="tkx" hidden>Отменить правку</button></div><div id="tkl"></div></div>')
R("else if(mode=='sp')L.popup(PO()).setLatLng(m.getLatLng()).setContent(sqMenu(p)).openOn(map);",
  "else if(mode=='task'){if(TKA)tkPt(m.getLatLng());else tkTog(p)}else if(mode=='sp')L.popup(PO()).setLatLng(m.getLatLng()).setContent(sqMenu(p)).openOn(map);")
n=s.count("if(dt||SELA||mode=='add')return;");assert n>=2,n
s=s.replace("if(dt||SELA||mode=='add')return;","if(dt||SELA||mode=='add'||mode=='task')return;")
R("$('spp').hidden=mode!='sp';","$('spp').hidden=mode!='sp';$('tkp').hidden=mode!='task';if(mode!='task'&&typeof TKA!='undefined'){TKA=false;TKPTS=[];map.getContainer().style.cursor=''}try{tkDraw();tkList();tkInfo()}catch(e){}")
R("function stats(){try{paInfo()}catch(e){}","function stats(){try{tkDraw();tkList()}catch(e){}try{paInfo()}catch(e){}")
R("const RO=/*RO*/false;","const RO=/*RO*/false;var TKV=false;")
R("$('fjb').onclick=",JS+"\n$('fjb').onclick=")
open(p,'w',encoding='utf-8').write(s);print('ok tasks')
