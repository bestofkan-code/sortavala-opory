# Фото HEIC/HEIF (iPhone): перед сжатием переводим в JPEG через heic2any (грузится с CDN только когда нужен);
# в полях выбора фото разрешены .heic/.heif
import sys
fn=sys.argv[1];s=open(fn,encoding='utf-8').read()
def rep(a,b,n=1):
    global s
    assert s.count(a)==n,(s.count(a),a[:80]);s=s.replace(a,b)
FN=r"""function isHeic(f){return f&&(/^image\/hei[cf]/i.test(f.type||'')||/\.hei[cf]$/i.test(f.name||''))}
var HEIC2ANY=null;function heicLib(){return HEIC2ANY||(HEIC2ANY=new Promise((ok,no)=>{if(window.heic2any)return ok(window.heic2any);const sc=document.createElement('script');sc.src='https://cdn.jsdelivr.net/npm/heic2any@0.0.4/dist/heic2any.min.js';sc.onload=()=>window.heic2any?ok(window.heic2any):no(new Error('heic2any не загрузился'));sc.onerror=()=>{HEIC2ANY=null;no(new Error('нет связи: не удалось загрузить конвертер HEIC'))};document.head.appendChild(sc)}))}
async function heicFix(f){if(!isHeic(f))return f;try{if(window.createImageBitmap){const bm=await createImageBitmap(f);bm.close&&bm.close();return f}}catch(e){}
 try{toast('Перевожу HEIC в JPEG…')}catch(e){}const h=await heicLib();let r=await h({blob:f,toType:'image/jpeg',quality:.9});if(Array.isArray(r))r=r[0];return r}
"""
rep("function ppShrink(f){return new Promise((ok,no)=>{",FN+"function ppShrink(f0){return heicFix(f0).then(f=>new Promise((ok,no)=>{")
# закрыть .then(...)
i=s.find("function ppShrink(f0)");j=s.find("im.src=u})}",i);assert j>0
s=s[:j]+"im.src=u}))}"+s[j+len("im.src=u})}"):]
rep('accept="image/*"','accept="image/*,.heic,.heif"',s.count('accept="image/*"'))
open(fn,'w',encoding='utf-8').write(s);print('ok')
