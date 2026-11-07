# Основная карта: бронекабель — сплошная линия, когда на ТП отмечено «Проложен бронекабель»; статус в окне кабеля; исправлен лист «Работы по дням».
import sys
p=sys.argv[1];s=open(p,encoding='utf-8').read()
def R(a,b,n=1):
    global s
    assert s.count(a)==n,(a[:90],s.count(a));s=s.replace(a,b)
R("function cabLen(t){","function cabDone(t){try{return !!(((TPD.get(String(t))||{}).w||{})[1])}catch(e){return false}}\nfunction cabLen(t){")
R("CABS.forEach(z=>{L.polyline(z.path,{color:'#c026d3',weight:4,opacity:.95,dashArray:'12 6',interactive:false}).addTo(ll);",
  "CABS.forEach(z=>{const cd=cabDone(z.tp);L.polyline(z.path,cd?{color:'#c026d3',weight:5,opacity:1,interactive:false}:{color:'#c026d3',weight:4,opacity:.95,dashArray:'12 6',interactive:false}).addTo(ll);")
R("html:'<div class=\"spl\" style=\"background:#c026d3;color:#fff\">'+Math.round(z.d)+' м</div>'","html:'<div class=\"spl\" style=\"background:#c026d3;color:#fff\">'+(cd?'✓ ':'')+Math.round(z.d)+' м</div>'")
R("<small>подземная КЛ от ТП до опоры ввода с инспекционным люком</small><div class=\"r\"><button data-cp>Опора '+esc(z.p.id)+'</button>'",
  "<small>подземная КЛ от ТП до опоры ввода с инспекционным люком</small><div>'+(cabDone(z.tp)?'✅ проложен'+(((TPD.get(z.tp)||{}).w||{})[1]?' '+String(TPD.get(z.tp).w[1]).split('-').reverse().join('.'):'')+((TPD.get(z.tp)||{}).cab!=null?' · факт '+(+TPD.get(z.tp).cab).toLocaleString('ru-RU')+' м':''):'⬜ ещё не проложен')+'</div><div class=\"r\"><button data-cp>Опора '+esc(z.p.id)+'</button><button data-ct>'+esc(tpn(z.tp))+' ›</button>'")
R("d.querySelector('[data-cp]').onclick=()=>{map.closePopup();L.popup(PO()).setLatLng([z.p.lat,z.p.lon]).setContent(popup(z.p)).openOn(map)};",
  "d.querySelector('[data-cp]').onclick=()=>{map.closePopup();L.popup(PO()).setLatLng([z.p.lat,z.p.lon]).setContent(popup(z.p)).openOn(map)};d.querySelector('[data-ct]').onclick=()=>{map.closePopup();tpPopup(z.tp,L.latLng(z.a))};")
R("TPD.set(t,r);TQ[t]=r;tpSave();if(ch.lat!=null)lines();else tpDraw();","TPD.set(t,r);TQ[t]=r;tpSave();if(ch.lat!=null||ch.w)lines();else tpDraw();")
R("r[k-1]++}}));","r[WK.findIndex(w=>w[0]==k)]++}}));")
R("vertical-align:middle;margin-right:6px\"></i>бронекабель от ТП &nbsp;","vertical-align:middle;margin-right:6px\"></i>бронекабель от ТП (пунктир — не проложен, сплошной — проложен) &nbsp;")
open(p,'w',encoding='utf-8').write(s);print('ok main-cab')
