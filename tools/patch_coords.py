# Координаты опоры в карточке (редактор и просмотр): «61.712345, 30.691234» — формат Яндекс Карт, кнопка «Копировать» и ссылка «Яндекс»
import sys
fn=sys.argv[1];s=open(fn,encoding='utf-8').read()
def rep(a,b):
    global s
    assert s.count(a)==1,('not unique/absent',a[:80]);s=s.replace(a,b)
FN=r"""function ycoS(p){return (+p.lat).toFixed(6)+', '+(+p.lon).toFixed(6)}
function ycoH(p,dark){if(p.lat==null||p.lon==null)return '';const c=ycoS(p),u='https://yandex.ru/maps/?pt='+(+p.lon).toFixed(6)+','+(+p.lat).toFixed(6)+'&z=18&l=map';return `<div class="yco${dark?' dk':''}"><span title="Координаты для Яндекс Карт (широта, долгота)">${c}</span><button type="button" data-yco="${c}" title="Скопировать координаты в формате Яндекс Карт">Копировать</button><a href="${u}" target="_blank" rel="noopener">Яндекс</a></div>`}
function ycoCopy(t,b){const ok=()=>{const o=b.textContent;b.textContent='Скопировано';b.classList.add('ok');setTimeout(()=>{b.textContent=o;b.classList.remove('ok')},1500)},fb=()=>{const ta=document.createElement('textarea');ta.value=t;ta.style.cssText='position:fixed;left:-9999px;top:0';document.body.appendChild(ta);ta.select();try{document.execCommand('copy');ok()}catch(e){prompt('Координаты:',t)}ta.remove()};if(navigator.clipboard&&window.isSecureContext)navigator.clipboard.writeText(t).then(ok,fb);else fb()}
document.head.insertAdjacentHTML('beforeend','<style>.yco{display:flex;align-items:center;gap:6px;margin:3px 0 4px;font-size:12px;flex-wrap:wrap}.yco span{font-family:ui-monospace,Menlo,Consolas,monospace;user-select:all}.yco button{font:600 11.5px system-ui,sans-serif;padding:2px 8px;border-radius:6px;border:1px solid #94a3b8;background:#f1f5f9;color:#0f172a;cursor:pointer}.yco button.ok{background:#16a34a;border-color:#16a34a;color:#fff}.yco a{font-size:11.5px;color:#2563eb}.yco.dk span{color:#e2e8f0}.yco.dk button{background:#334155;color:#f8fafc;border-color:#64748b}.yco.dk a{color:#93c5fd}</style>');
document.addEventListener('click',e=>{const b=e.target.closest&&e.target.closest('[data-yco]');if(!b)return;e.preventDefault();e.stopPropagation();ycoCopy(b.getAttribute('data-yco'),b)},true);
"""
rep("function roPopup(p){const d=document.createElement('div');d.className='pp';",FN+"function roPopup(p){const d=document.createElement('div');d.className='pp';")
rep("""${/^p\\d+$/.test(p.uid)?'':' <small style="color:#15803d">новая</small>'}</div><div>${tpn(p.tp||'-')}""","""${/^p\\d+$/.test(p.uid)?'':' <small style="color:#15803d">новая</small>'}</div>${ycoH(p)}<div>${tpn(p.tp||'-')}""")
rep("""${/^p\\d+$/.test(p.uid)?'':' <small style="color:#4ade80">новая</small>'}</div>
${sqHas(p)?""","""${/^p\\d+$/.test(p.uid)?'':' <small style="color:#4ade80">новая</small>'}</div>${ycoH(p,1)}
${sqHas(p)?""")
open(fn,'w',encoding='utf-8').write(s);print('ok')
