# Фотоотчёт по ШУНО в окне ТП (основная и монтажная карты): фото хранятся в pole_photos с uid «tp:<ТП>», k=2, kind='after'
import sys
fn=sys.argv[1];s=open(fn,encoding='utf-8').read()
def rep(a,b):
    global s
    assert s.count(a)==1,(s.count(a),a[:80]);s=s.replace(a,b)
rep("function pname(u){const p=P.find(o=>o.uid==u);return p?p.id:u}","function pname(u){if(/^tp:/.test(u))return tpn(u.slice(3));const p=P.find(o=>o.uid==u);return p?p.id:u}")
rep("o.innerHTML='<img src=\"'+ppU(y)+'\" alt=\"\"><div>'+esc(pname(y.uid))+' · подрезка крон · '+(y.kind=='before'?'до':'после')+' · '",
    "const tpq=/^tp:/.test(y.uid);o.innerHTML='<img src=\"'+ppU(y)+'\" alt=\"\"><div>'+esc(pname(y.uid))+(tpq?' · ШУНО':' · подрезка крон · '+(y.kind=='before'?'до':'после'))+' · '")
FN=r"""function tpPh(box,t){const u='tp:'+t,K=2;box._r=()=>{const L2=ppL(u,K),w=((TPD.get(t)||{}).w||{});if(RO&&!L2.length){box.hidden=true;box.innerHTML='';return}box.hidden=false;
 box.innerHTML='<div class="phh">ШУНО — фотоотчёт'+(!RO&&w[K]&&!L2.length?' <span style="color:#fbbf24">· нужно фото</span>':'')+'</div><div class="phr">'+L2.map(x=>'<span class="tnpt"><img src="'+ppU(x)+'" loading="lazy" data-ppv="'+x.id+'" alt="">'+(RO?'':'<b data-ppd="'+x.id+'" title="Удалить">×</b>')+'</span>').join('')+(RO?'':'<label class="tnpa" title="Добавить фото">＋<input type="file" accept="image/*" capture="environment" multiple data-ppk hidden></label>')+(L2.length||RO?'':'<small style="color:#6b7280">фото шкафа: общий вид, ввод кабеля, подключение</small>')+'</div>';setTimeout(ppPan,0);
 box.querySelectorAll('[data-ppv]').forEach(im=>im.onclick=()=>ppView(L2,L2.findIndex(x=>x.id==im.dataset.ppv)));
 box.querySelectorAll('[data-ppd]').forEach(b=>b.onclick=async()=>{PSEL=Date.now();if(!AUTH())return alert('Войдите, чтобы удалять фото.');if(!confirm('Удалить фото?'))return;const x=PPH.find(o=>o.id==b.dataset.ppd);if(!x)return;try{await authFresh()}catch(e){}
  try{const r=await fetch(CF.u+'/rest/v1/pole_photos?id=eq.'+x.id,{method:'DELETE',headers:H()});if(!r.ok)throw new Error(await r.text());await fetch(CF.u+'/storage/v1/object/pole-photos/'+x.path.split('/').map(encodeURIComponent).join('/'),{method:'DELETE',headers:H()});PPH=PPH.filter(o=>o.id!=x.id);ppSave();setTimeout(ppRefresh,0)}catch(e){alert('Не удалось удалить: '+(e.message||e))}});
 box.querySelectorAll('[data-ppk]').forEach(inp=>{inp.onclick=()=>{PSEL=Date.now()};inp.onchange=async()=>{PSEL=Date.now();if(!AUTH()){inp.value='';return alert('Войдите, чтобы добавлять фото.')}const fs=[...inp.files];inp.value='';if(!fs.length)return;inp.parentNode.firstChild.textContent='…';let ok=0;
  for(const f of fs){try{await ppUp(u,K,'after',f);ok++}catch(e){alert('Фото не загружено: '+(e.message||e))}}if(ok)toast('Фото ШУНО загружено: '+ok);box._r()}})};box._r()}
"""
rep("function tpPopup(t,at){",FN+"function tpPopup(t,at){")
rep("addAdr(d,at.lat,at.lng,'');fixCard(d);L.popup(PO()).setLatLng(at).setContent(d).openOn(map)}",
    "{const pb=document.createElement('div');pb.className='phb';pb.setAttribute('data-phb','');const rr=d.querySelector('[data-tz]');rr.parentNode.parentNode.insertBefore(pb,rr.parentNode);tpPh(pb,t)}addAdr(d,at.lat,at.lng,'');fixCard(d);L.popup(PO()).setLatLng(at).setContent(d).openOn(map)}")
open(fn,'w',encoding='utf-8').write(s);print('ok')
