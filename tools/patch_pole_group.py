#!/usr/bin/env python3
"""Нажатие на опору подсвечивает опоры, которые к ней относятся:
  • все опоры той же ТП — кольцом в цвет ТП;
  • опоры, которые питаются через эту опору (дальше по линии от ввода ТП), — оранжевым кольцом.
Вверху карты — плашка со счётом (ТП: N опор, установлено M; за этой опорой по линии: K опор).
Подсветка снимается крестиком на плашке или нажатием на пустое место карты.
Применяется к redaktor.html (один раз): python3 tools/patch_pole_group.py redaktor.html
"""
import sys
path = sys.argv[1]
s = open(path, encoding='utf-8').read()
if 'function pgShow(' in s:
    print('already applied'); sys.exit(0)

JS = r"""
<style>#pgb{position:absolute;bottom:22px;left:50%;transform:translateX(-50%);z-index:1000;background:#fff;color:#111;border:2px solid #475569;border-radius:10px;padding:5px 30px 5px 10px;font:13px/1.35 system-ui,sans-serif;box-shadow:0 2px 8px rgba(0,0,0,.25);max-width:min(92vw,560px)}
#pgb b{font-weight:700}#pgb .x{position:absolute;right:6px;top:4px;border:0;background:none;font-size:18px;line-height:1;cursor:pointer;color:#475569}
#pgb .o{color:#c2410c}body.dk #pgb{background:#1f2937;color:#f3f4f6}</style>
<script>
var PGLY=L.layerGroup().addTo(map),PGP=null;
function pgWord(n){return n%10==1&&n%100!=11?'опора':n%10>=2&&n%10<=4&&(n%100<12||n%100>14)?'опоры':'опор'}
function pgDown(p){/* опоры, питающиеся через p: связь по нарисованным линиям, ввод — опора с бронекабелем от ТП */
 const N=NETC||netEdges(),E=N.E||N,adj=new Map(),ok=q=>q&&!q.x&&!q.pp;
 E.forEach(e=>{const a=e[0],b=e[1];if(!ok(a)||!ok(b))return;if(!adj.has(a))adj.set(a,[]);if(!adj.has(b))adj.set(b,[]);adj.get(a).push(b);adj.get(b).push(a)});
 if(!adj.has(p))return null;
 const comp=new Set([p]),st=[p];while(st.length){const x=st.pop();(adj.get(x)||[]).forEach(y=>{if(!comp.has(y)){comp.add(y);st.push(y)}})}
 const roots=[...comp].filter(q=>q.vk&&q!==p);
 if(!roots.length)return p.vk?{all:[...comp].filter(q=>q!==p),root:true}:null;
 const seen=new Set(roots),q2=[...roots];while(q2.length){const x=q2.pop();(adj.get(x)||[]).forEach(y=>{if(y!==p&&!seen.has(y)){seen.add(y);q2.push(y)}})}
 return{all:[...comp].filter(q=>q!==p&&!seen.has(q)),root:!!p.vk}}
function pgClr(){PGLY.clearLayers();PGP=null;const b=document.getElementById('pgb');if(b)b.remove()}
function pgShow(p){PGLY.clearLayers();PGP=p;const t=String(p.tp||''),col=t?tpCol(t):'#475569',
 G=t?P.filter(q=>String(q.tp)==t&&!q.x):[],act=G.filter(q=>!q.pp),gr=G.length-act.length,dn=act.filter(q=>q.done).length,D=pgDown(p);
 act.forEach(q=>L.circleMarker([q.lat,q.lon],{radius:13,color:col,weight:3,opacity:.9,fillColor:col,fillOpacity:.12,interactive:false}).addTo(PGLY));
 if(D)D.all.forEach(q=>L.circleMarker([q.lat,q.lon],{radius:17,color:'#f97316',weight:3,dashArray:'5 4',fill:false,interactive:false}).addTo(PGLY));
 L.circleMarker([p.lat,p.lon],{radius:19,color:'#111',weight:3,fill:false,interactive:false}).addTo(PGLY);
 let b=document.getElementById('pgb');if(!b){b=document.createElement('div');b.id='pgb';map.getContainer().appendChild(b);L.DomEvent.disableClickPropagation(b)}
 b.style.borderColor=col;
 let h='<b>'+esc(p.id)+'</b>';
 if(t)h+=' · <b style="color:'+col+'">'+esc(tpn(t))+'</b>: '+act.length+' '+pgWord(act.length)+' на карте, установлено '+dn+(gr?' (+'+gr+' сер.)':'');
 if(D)h+='<br><span class="o">'+(D.root?'Опора ввода от ТП — через неё питается ':'За этой опорой по линии: ')+'<b>'+D.all.length+'</b> '+pgWord(D.all.length)+(D.all.length?' (оранжевые кольца)':'')+'</span>';
 else if(!p.x&&!p.pp)h+='<br><small>Опора не связана линией с вводом ТП — ветку посчитать нельзя</small>';
 b.innerHTML=h+'<button class="x" title="Убрать подсветку">×</button>';b.querySelector('.x').onclick=pgClr}
{const _pp=popup;popup=function(p){try{pgShow(p)}catch(e){console.warn(e)}return _pp.apply(this,arguments)}}
map.on('click',()=>{if(PGP&&Date.now()-PSEL>900)pgClr()});
</script>
"""
anchor = '</script></body></html>'
i = s.rfind(anchor)
assert i > 0
s = s[:i + len('</script>')] + JS + s[i + len('</script>'):]
open(path, 'w', encoding='utf-8').write(s); print('ok', path)
