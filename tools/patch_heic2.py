# HEIC: конвертер heic-to 1.6.7 (libheif 1.23) вместо старого heic2any 0.0.4 — тот не читает HEIC новых iPhone
# («ERR_LIBHEIF format not supported»); heic2any оставлен запасным
import sys
fn=sys.argv[1];s=open(fn,encoding='utf-8').read()
i=s.find("var HEIC2ANY=null;");j=s.find("function ppShrink(f0)",i);assert i>0 and j>i
NEW=r"""var HEICLIB={};function heicLoad(name,url,glob){return HEICLIB[name]||(HEICLIB[name]=new Promise((ok,no)=>{if(window[glob])return ok(window[glob]);const sc=document.createElement('script');sc.src=url;sc.onload=()=>window[glob]?ok(window[glob]):no(new Error(name+' не загрузился'));sc.onerror=()=>{delete HEICLIB[name];no(new Error('нет связи: не удалось загрузить конвертер HEIC'))};document.head.appendChild(sc)}))}
async function heicFix(f){if(!isHeic(f))return f;try{if(window.createImageBitmap){const bm=await createImageBitmap(f);bm.close&&bm.close();return f}}catch(e){}
 try{toast('Перевожу HEIC в JPEG…')}catch(e){}let er;
 try{const H=await heicLoad('heic-to','https://cdn.jsdelivr.net/npm/heic-to@1.6.7/dist/iife/heic-to.js','HeicTo');return await H({blob:f,type:'image/jpeg',quality:.9})}catch(e){er=e}
 try{const h=await heicLoad('heic2any','https://cdn.jsdelivr.net/npm/heic2any@0.0.4/dist/heic2any.min.js','heic2any');let r=await h({blob:f,toType:'image/jpeg',quality:.9});return Array.isArray(r)?r[0]:r}catch(e){}
 throw new Error('не удалось перевести HEIC в JPEG ('+(er&&er.message||er)+'). Пришлите фото в JPEG: на iPhone «Настройки → Камера → Форматы → Наиболее совместимый»')}
"""
s=s[:i]+NEW+s[j:]
open(fn,'w',encoding='utf-8').write(s);print('ok')
