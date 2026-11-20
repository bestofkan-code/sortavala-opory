# Кнопка «№» под поиском: показать/скрыть номера опор вида «ТП97-3» на карте (то же, что галочка «подписать номера опор»).
# Подпись теперь с номером ТП; состояние запоминается.
import sys
p=sys.argv[1];s=open(p,encoding='utf-8').read()
def R(a,b,n=1):
    global s
    assert s.count(a)==n,(a[:90],s.count(a));s=s.replace(a,b)
R("if(p.n&&vis(p))L.marker([p.lat,p.lon],{interactive:false,icon:L.divIcon({html:'<span class=\"nlab\">'+p.n+'</span>'",
  "if(p.n&&vis(p))L.marker([p.lat,p.lon],{interactive:false,icon:L.divIcon({html:'<span class=\"nlab\">'+esc(SHD(String(p.id||'').replace(/^КТП\\s+/,'КТП')))+'</span>'")
R("$('pn').onchange=numLabels;",
  "try{if(localStorage.getItem(KEY+'_pn')==='1')$('pn').checked=true}catch(e){}\n$('pn').onchange=()=>{try{localStorage.setItem(KEY+'_pn',$('pn').checked?'1':'0')}catch(e){}numLabels();try{nbtnUI()}catch(e){}};\nfunction nbtnUI(){const a=document.getElementById('nbtn');if(!a)return;const on=$('pn').checked;a.style.background=on?'#4f7cff':'';a.style.color=on?'#fff':'';a.title=on?'Скрыть номера опор':'Показать номера опор (ТП и номер)'}")
R(".nlab{position:absolute;left:9px;top:1px;font:bold 10px sans-serif;",".nlab{position:absolute;left:10px;top:2px;font:bold 11px sans-serif;")
A="o.scrollIntoView({block:'nearest'})}};\n  return d}});new C().addTo(map)}"
R(A,A+"\n{const C=L.Control.extend({options:{position:'topleft'},onAdd(){const d=L.DomUtil.create('div','leaflet-bar');d.innerHTML='<a href=\"#\" id=\"nbtn\" style=\"display:flex;align-items:center;justify-content:center;font:800 15px/30px system-ui,sans-serif\">№</a>';L.DomEvent.disableClickPropagation(d);"
  "d.querySelector('a').onclick=e=>{e.preventDefault();$('pn').checked=!$('pn').checked;$('pn').onchange();toast($('pn').checked?'Номера опор показаны':'Номера опор скрыты')};return d}});new C().addTo(map);setTimeout(()=>{nbtnUI();numLabels()},0)}")
open(p,'w',encoding='utf-8').write(s);print('ok numbtn',p)
