# Запрет добавлять и переставлять опоры для отдельных пользователей (сейчас — Леонид).
# Источник правды — сервер: таблица public.user_limits (no_move) и триггер guard_nomove на poles.
# Страница после входа спрашивает rpc is_nomove() и, если запрет есть:
#  - прячет кнопку режима «Добавить» (и выходит из него, если он был включён);
#  - не даёт перетаскивать опоры в режиме «Правка/перенос»;
#  - не даёт переносить опору по GPS в «Сверке на месте».
# Значки ТП, работы, свойства опор и всё остальное — без изменений.
import sys

p = sys.argv[1]
s = open(p, encoding='utf-8').read()
if 'var NOMOVE=' in s:
    print('already', p); sys.exit(0)

def rep(a, b, n=1):
    global s
    c = s.count(a)
    assert c == n, (p, a[:60], c)
    s = s.replace(a, b)

# 1. флаг и проверка на сервере
rep("var USERS=[",
    "var NOMOVE=false;function nmSet(v){NOMOVE=!!v;const b=document.querySelector('#modes [data-m=\"add\"]');if(b)b.style.display=NOMOVE?'none':'';"
    "if(NOMOVE&&typeof mode!='undefined'&&mode=='add'){const v=document.querySelector('#modes [data-m=\"view\"]');if(v)v.click()}}\n"
    "async function nmCheck(){if(RO||!SESS||!CF){nmSet(false);return}try{await authFresh();if(!SESS)return nmSet(false);"
    "const r=await fetch(CF.u+'/rest/v1/rpc/is_nomove',{method:'POST',headers:{apikey:CF.k,Authorization:'Bearer '+SESS.at,'Content-Type':'application/json'},body:'{}'});"
    "if(r.ok)nmSet((await r.json())===true)}catch(e){}}\n"
    "function nmDeny(w){toast('Вам запрещено '+w+' опоры');}\n"
    "var USERS=[")

# 2. после входа / при загрузке с сохранённым входом — проверить; после выхода — снять
rep("if(SESS){if(o)o.style.display='none';WHO=SESS.name||WHO;$('who').value=WHO;return}",
    "if(SESS){if(o)o.style.display='none';WHO=SESS.name||WHO;$('who').value=WHO;nmCheck();return}nmSet(false);")

# 3. добавление опоры нажатием на карту
rep("function addAt(la,lo){", "function addAt(la,lo){if(NOMOVE){nmDeny('добавлять');return}")

# 4. перетаскивание опоры в режиме «Правка/перенос»
rep("if(!hit)return;const[p,m]=hit,o=m.getLatLng(),s=map.mouseEventToLatLng(e)",
    "if(!hit)return;if(NOMOVE){nmDeny('переставлять');return}const[p,m]=hit,o=m.getLatLng(),s=map.mouseEventToLatLng(e)")

# 5. запасной путь: dragend маркера опоры
rep("m.on('dragend',()=>{const c=m.getLatLng(),o=m._o||L.latLng(p.lat,p.lon),d=Math.round(map.distance(o,c));if(d<1||",
    "m.on('dragend',()=>{const c=m.getLatLng(),o=m._o||L.latLng(p.lat,p.lon),d=Math.round(map.distance(o,c));if(NOMOVE){m.setLatLng([p.lat,p.lon]);if(d>=1)nmDeny('переставлять');return}if(d<1||")

# 6. перенос по GPS в «Сверке на месте»
rep("b.querySelector('[data-vg]').onclick=e=>{if(!navigator.geolocation)",
    "b.querySelector('[data-vg]').onclick=e=>{if(NOMOVE)return nmDeny('переставлять');if(!navigator.geolocation)")

open(p, 'w', encoding='utf-8').write(s)
print('ok nomove', p)
