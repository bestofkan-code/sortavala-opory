# Собирает uchastki.html — «Участки работ» — из redaktor.html (код в tools/zones.js).
# Выделяем опоры участка, даты и время работ → архив: схема участка (PDF) и письма в пресс-службу
# (с объявлением для жителей), в Россети (отключение ВЛ 0,4 кВ), в ГИБДД (автовышка на проезжей части).
# На странице только режим «Участки»: отметки работ и правка опор здесь недоступны.
#   python3 tools/patch_zones.py redaktor.html uchastki.html
import sys, os
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
JS = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'zones.js'), encoding='utf-8').read()


def R(a, b, n=1):
    global s
    assert s.count(a) == n, (a[:90], s.count(a))
    s = s.replace(a, b)


R("<title>Карта опор — Сортавала</title>", "<title>Участки работ — Сортавала</title>")
R("#sps div{margin:2px 0;font-size:12px}", "#sps div{margin:2px 0;font-size:12px}"
  "#modes button:not([data-m=zone]){display:none!important}"
  "#znp{margin-top:6px;border:1px solid #f59e0b;border-radius:8px;padding:6px 8px}#znp[hidden]{display:none}"
  "#znp input[type=text],#znp textarea{width:100%;box-sizing:border-box;margin:3px 0}"
  "#znw,#znf{flex-wrap:wrap;gap:4px}#znw label,#znf label{border:1px solid #4b5468;border-radius:10px;padding:2px 8px;font-size:12px;cursor:pointer}"
  "#znw label:has(input:checked),#znf label:has(input:checked){border-color:#f59e0b;background:rgba(245,158,11,.18)}"
  ".zni{border:1px solid rgba(127,127,127,.35);border-radius:8px;padding:5px 7px;margin:6px 0;font-size:12.5px}.zni.dn{opacity:.55}.zni>small{display:block;opacity:.85;margin-top:2px}"
  ".zni .r{margin-top:4px}.zni .r button{padding:3px 8px}.zni .zdoc{border-color:#f59e0b}"
  ".zsr{gap:4px;flex-wrap:wrap}.zns{font-size:11.5px;border:1px solid #4b5468;border-radius:10px;padding:1px 7px}.zns.ok{border-color:#22c55e;background:rgba(34,197,94,.15)}.zns:has(input:disabled){opacity:.45}"
  ".zdb{margin-top:5px;border-top:1px dashed rgba(127,127,127,.4);padding-top:5px}.zdb label{display:block;font-size:12px;margin:2px 0}"
  "#zncf label{display:block;font-size:12px;margin-top:4px}#zncf{margin-top:4px}"
  ".znlb{transform:translate(-50%,-50%);background:rgba(168,85,247,.92);color:#fff;font:600 12px system-ui;padding:2px 7px;border-radius:9px;white-space:nowrap;pointer-events:none}")
R('<button class="b" data-m="task" style="border-color:#22d3ee">Задания бригаде</button>',
  '<button class="b" data-m="task" style="border-color:#22d3ee">Задания бригаде</button><button class="b" data-m="zone" style="border-color:#f59e0b">Участки работ</button>')
R('<div id="tkl"></div></div>',
  '<div id="tkl"></div></div>'
  '<div id="znp" hidden><b>Участки работ — письма и схемы</b><small style="display:block;margin:2px 0 4px">Нажимайте на опоры — добавить или убрать из участка, или обведите участок на карте. '
  'Для сохранённого участка кнопка «Документы» соберёт архив: схему участка (PDF) и письма в пресс-службу (с объявлением для жителей), в Россети и в ГИБДД (Word).</small>'
  '<div class="r"><button id="zna">Обвести участок</button><button id="znok" hidden>Готово</button><button id="znun" hidden>↶ точка</button><button id="znc">Очистить</button></div><small id="zni" style="display:block"></small>'
  '<input type="text" id="znn" placeholder="Название участка, например: ул. Победы, ТП90">'
  '<div class="r">Даты: с <input type="date" id="zn1"> по <input type="date" id="zn2"></div>'
  '<div class="r">Время: с <input type="time" id="znt1" value="08:00"> до <input type="time" id="znt2" value="18:00"></div>'
  '<small style="display:block;margin-top:4px">Какие работы</small><div id="znw" class="r">'
  '<label><input type="checkbox" data-k="1"> Котлованы и фундаменты</label><label><input type="checkbox" data-k="4"> Установка опор</label>'
  '<label><input type="checkbox" data-k="12"> Кронштейны и светильники</label><label><input type="checkbox" data-k="5"> СИП</label>'
  '<label><input type="checkbox" data-k="20"> Перенос совм. подвески</label><label><input type="checkbox" data-k="21"> Демонтаж старых опор</label><label><input type="checkbox" data-k="11"> Заземление</label></div>'
  '<small style="display:block;margin-top:4px">Что нужно</small><div id="znf" class="r">'
  '<label title="Письмо в пресс-службу и объявление для жителей"><input type="checkbox" id="znpk" checked> Освободить места у опор (пресс-служба)</label>'
  '<label title="Письмо в Россети"><input type="checkbox" id="znof"> Отключение ВЛ 0,4 кВ (Россети)</label>'
  '<label><input type="checkbox" id="znlf"> Автовышка / кран</label>'
  '<label title="Вместе с «Автовышка» — письмо в ГИБДД"><input type="checkbox" id="znrd"> На проезжей части (ГИБДД)</label></div>'
  '<input type="text" id="znt" placeholder="Примечание (для себя)">'
  '<div class="r"><button id="zns">Сохранить участок</button><button id="znx" hidden>Отменить правку</button><button id="zncb">Реквизиты писем</button></div>'
  '<div id="zncf" hidden></div><div id="znl"></div></div>')
R("else if(mode=='task'){if(TKA)tkPt(m.getLatLng());else tkTog(p)}",
  "else if(mode=='zone'){if(ZNA)znPt(m.getLatLng());else znTog(p)}else if(mode=='task'){if(TKA)tkPt(m.getLatLng());else tkTog(p)}")
n = s.count("if(dt||SELA||mode=='add'||mode=='task')return;")
assert n >= 2, n
s = s.replace("if(dt||SELA||mode=='add'||mode=='task')return;", "if(dt||SELA||mode=='add'||mode=='task'||mode=='zone')return;")
R("$('tkp').hidden=mode!='task';",
  "$('tkp').hidden=mode!='task';$('znp').hidden=mode!='zone';if(mode!='zone'&&typeof ZNA!='undefined'){ZNA=false;ZNPTS=[]}try{znDraw();znList();znInfo()}catch(e){}")
R("function stats(){try{tkDraw();tkList()}catch(e){}", "function stats(){try{tkDraw();tkList()}catch(e){}try{znDraw()}catch(e){}")
R("$('fjb').onclick=", JS + "\n$('fjb').onclick=")
R('<div id="s"><b style="font-size:15px">Опоры освещения, Сортавала</b>',
  '<div id="s"><b style="font-size:15px">Участки работ — Сортавала</b><small style="display:block;opacity:.8;margin:2px 0 4px">Письма и схемы по участкам: пресс-служба, Россети, ГИБДД · <a href="redaktor.html" style="color:inherit">основная карта</a></small>')
open(dst, 'w', encoding='utf-8').write(s)
print('ok', dst)
