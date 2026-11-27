/* Резервная копия данных для страниц «только смотреть».
   Каждые ~5 минут GitHub сам выгружает таблицы из Supabase в data/mirror/ (см. .github/workflows/mirror.yml).
   Если Supabase не ответил за 6 секунд (в России без VPN он за Cloudflare и режется), страница берёт данные из копии.
   Запись (отметки, фото) по-прежнему идёт только в Supabase. */
(function(){
  var SB='https://rznsydqapcffgnvynfdg.supabase.co',ST=SB+'/storage/v1/object/public/';
  var BASE=(document.currentScript&&document.currentScript.src||location.href).replace(/lib\/mirror\.js.*$/,'')+'data/mirror/';
  var TB={poles:1,sip2:1,hooks:1,tps:1,spans:1,line_edits:1,draws:1,pole_photos:1,tn_photos:1,tn_remarks:1,work_zones:1,crew_tasks:1};
  var TO=6000,RETRY=5*60*1000,dead=0,META=null,metaAt=0,CACHE={},of=window.fetch.bind(window);
  function isDead(){return Date.now()<dead}
  if(/[?&]mirror=1/.test(location.search))dead=1e15;   /* проверка: открыть страницу с ?mirror=1 */
  async function meta(){if(META&&Date.now()-metaAt<60000)return META;var r=await of(BASE+'meta.json?t='+Date.now(),{cache:'no-store'});META=await r.json();metaAt=Date.now();return META}
  async function table(t){var m=await meta(),v=m.ts||'';if(CACHE[t]&&CACHE[t].v===v)return CACHE[t].rows;var r=await of(BASE+t+'.json?v='+encodeURIComponent(v));if(!r.ok)throw new Error('нет копии '+t);var rows=await r.json();CACHE[t]={v:v,rows:rows};return rows}
  function val(x,c){var p=c.split('->>');if(p.length==2){var o=x[p[0]];return o&&o[p[1].replace(/'/g,'')]}return x[c]}
  function flt(rows,u){var lim=null,off=0,ord=null,ok=true;
    u.searchParams.forEach(function(v,k){
      if(k=='select')return;if(k=='limit'){lim=+v;return}if(k=='offset'){off=+v;return}if(k=='order'){ord=v.split(',')[0].split('.');return}
      var m;
      if((m=/^eq\.(.*)$/.exec(v))){rows=rows.filter(function(x){return String(val(x,k))===m[1]})}
      else if((m=/^in\.\((.*)\)$/.exec(v))){var s=m[1].split(',').map(function(q){return q.replace(/^"|"$/g,'')});rows=rows.filter(function(x){return s.indexOf(String(val(x,k)))>=0})}
      else if(v=='is.null'){rows=rows.filter(function(x){return val(x,k)==null})}
      else if(v=='not.is.null'){rows=rows.filter(function(x){return val(x,k)!=null})}
      else ok=false});
    if(!ok)return null;
    if(ord){var c=ord[0],d=ord[1]=='desc'?-1:1;rows=rows.slice().sort(function(a,b){var p=a[c],q=b[c];return (p==q?0:(p==null?1:q==null?-1:(p>q?1:-1)))*d})}
    rows=rows.slice(off,lim==null?undefined:off+lim);return rows}
  async function fromMirror(u){var rows=flt(await table(u.pathname.split('/').pop()),u);if(rows==null)throw new TypeError('нет связи с базой');badge();
    return new Response(JSON.stringify(rows),{status:200,headers:{'Content-Type':'application/json','X-Mirror':'1'}})}
  window.fetch=async function(input,init){
    var url=typeof input=='string'?input:(input&&input.url)||String(input),me=((init&&init.method)||(input&&input.method)||'GET').toUpperCase();
    if(me!='GET'||url.indexOf(SB+'/rest/v1/')!==0)return of(input,init);
    var u=new URL(url),t=u.pathname.split('/').pop();
    if(!TB[t])return of(input,init);
    if(isDead()){try{return await fromMirror(u)}catch(e){}}
    var ctl=new AbortController(),tm=setTimeout(function(){ctl.abort()},TO);
    try{var r=await of(input,Object.assign({},init||{},{signal:ctl.signal})),tx=await r.text();clearTimeout(tm);
      if(!r.ok&&r.status>=500)throw new Error(r.status);
      if(dead){dead=0;badge()}
      return new Response(tx,{status:r.status,statusText:r.statusText,headers:r.headers})}
    catch(e){clearTimeout(tm);dead=Date.now()+RETRY;try{return await fromMirror(u)}catch(e2){throw e}}};
  /* фото: при работе с копии подменяем ссылки Supabase Storage на копии на сайте */
  function fix(el){['src','href'].forEach(function(a){var v=el.getAttribute&&el.getAttribute(a);if(v&&v.indexOf(ST)===0&&isDead()){el.setAttribute(a,BASE+'photos/'+v.slice(ST.length).split('?')[0])}})}
  document.addEventListener('error',function(e){var t=e.target;if(t&&t.tagName=='IMG'&&t.src.indexOf(ST)===0&&!t.dataset.mir){t.dataset.mir=1;t.src=BASE+'photos/'+t.src.slice(ST.length).split('?')[0]}},true);
  new MutationObserver(function(ms){if(!isDead())return;ms.forEach(function(m){if(m.type=='attributes')fix(m.target);else m.addedNodes.forEach(function(n){if(n.nodeType!=1)return;fix(n);n.querySelectorAll&&n.querySelectorAll('img[src^="'+ST+'"],a[href^="'+ST+'"]').forEach(fix)})})}).observe(document.documentElement,{subtree:true,childList:true,attributes:true,attributeFilter:['src','href']});
  window.MIRROR={dead:isDead,photo:function(b,p){return isDead()?BASE+'photos/'+b+'/'+p:ST+b+'/'+p}};
  /* плашка «показана копия» */
  var bd=null;
  async function badge(){try{if(!document.body){setTimeout(badge,500);return}
    if(!bd){bd=document.createElement('div');bd.style.cssText='position:fixed;left:8px;bottom:8px;z-index:100000;background:#7c2d12;color:#fff;font:12px/1.35 system-ui,sans-serif;padding:5px 9px;border-radius:8px;box-shadow:0 1px 6px rgba(0,0,0,.4);max-width:80vw;pointer-events:none';document.body.appendChild(bd)}
    if(!isDead()){bd.style.display='none';return}
    var m=await meta(),d=m.ts?new Date(m.ts):null;
    bd.textContent='Нет связи с базой — показана копия'+(d?' на '+d.toLocaleString('ru-RU',{day:'2-digit',month:'2-digit',hour:'2-digit',minute:'2-digit'}):'')+'. Обновится сама.';bd.style.display='block'}catch(e){}}
})();
