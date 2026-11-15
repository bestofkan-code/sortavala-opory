# Поле «Старая опора»: d — демонтируется, k — остаётся (колонка poles.od)
import sys
fn=sys.argv[1];s=open(fn,encoding='utf-8').read()
def rep(a,b):
    global s
    assert s.count(a)==1,('not unique/absent',a[:80]);s=s.replace(a,b)
rep("js:!!p.js,yd:!!p.yd,ad:p.ad||''};miss.forEach","js:!!p.js,yd:!!p.yd,ad:p.ad||'',od:p.od||null};miss.forEach")
rep("ad:r.ad||'',tp:r.tp,","ad:r.ad||'',od:r.od||'',tp:r.tp,")
rep("miss=['x','w','wc','js','yd','ad','ed','f','kr','sv','h','ka','vk','sx','pp','sp']","miss=['x','w','wc','js','yd','ad','ed','f','kr','sv','h','ka','vk','sx','pp','sp','od']")
rep("var SF=['sp',","var SF=['od','sp',")
a="<label>Светильн.<select data-sv>${[0,1,2].map(v=>`<option ${(+p.sv||0)==v?'selected':''}>${v}</option>`).join('')}</select></label>"
rep(a,a+"<label title=\"Старая опора на месте этой (рядом с ней)\">Старая опора<select data-od class=\"od-${p.od||'n'}\"><option value=\"\" ${p.od?'':'selected'}>—</option><option value=d ${p.od=='d'?'selected':''}>демонтир.</option><option value=k ${p.od=='k'?'selected':''}>остаётся</option></select></label>")
rep("const hs=()=>{d.querySelector('[data-hs]')","{const e=d.querySelector('[data-od]');if(e)e.onchange=()=>{p.od=e.value||'';e.className='od-'+(p.od||'n');upd(p);save();stats();mark(p)}}\nconst hs=()=>{d.querySelector('[data-hs]')")
# просмотр: строка в карточке
rep("function roPopup(p){const d=document.createElement('div');d.className='pp';","function odTxt(p){return p.od=='d'?'<div style=\"font-size:11.5px;color:#b91c1c\">Старая опора: демонтируется</div>':p.od=='k'?'<div style=\"font-size:11.5px;color:#15803d\">Старая опора: остаётся</div>':''}\nfunction roPopup(p){const d=document.createElement('div');d.className='pp';")
rep("${p.ad?'<div><b>Адрес:</b> '+esc(p.ad)+'</div>':''}<button data-h>История опоры</button>`;","${p.ad?'<div><b>Адрес:</b> '+esc(p.ad)+'</div>':''}${odTxt(p)}<button data-h>История опоры</button>`;")
rep('<style>*{box-sizing:border-box}','<style>select.od-d{color:#dc2626;font-weight:600}select.od-k{color:#16a34a;font-weight:600}*{box-sizing:border-box}')
open(fn,'w',encoding='utf-8').write(s);print('ok')
