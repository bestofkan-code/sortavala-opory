import sys
FILES=['redaktor.html','prosmotr.html','montazh.html','zamechaniya.html','zamechaniya-prosmotr.html','uchastki.html']
S2X="const S2X=[];try{(typeof S2!='undefined'?S2:[]).forEach(z=>{const gg=s2Geo(z),ps=(z.path||[]).filter(q=>q.p).map(q=>U.get(q.p)).filter(Boolean);if(ps.length<2)return;let sag=0;gg.seg.forEach(x=>{sag+=sipSag(x[2]).d});const pc={nodes:ps.map(p=>p.uid),len:gg.len,sag,loops:0,inl:0,a:ps[0],b:ps[ps.length-1],spans:gg.seg.length,nofeed:false,s2:true};PCS.push(pc);S2X.push({len:gg.len,done:ps.every(p=>wdone(p,5)),pc})})}catch(e){}\n "
R=[("\n return{ED,ND,PCS,U}}","\n "+S2X+"return{ED,ND,PCS,U,S2X}}"),
   ("C.ED.forEach(x=>{if(ok(x.a)&&ok(x.b)){L+=x.len;n++}});","C.ED.forEach(x=>{if(ok(x.a)&&ok(x.b)){L+=x.len;n++}});(C.S2X||[]).forEach(z=>{if(z.done){L+=z.len;n+=z.pc.spans}});"),
   ("C.ED.forEach(x=>{if(ok(x.a)&&ok(x.b))L+=x.len})}catch(e){}","C.ED.forEach(x=>{if(ok(x.a)&&ok(x.b))L+=x.len});(C.S2X||[]).forEach(z=>{if(z.done)L+=z.len})}catch(e){}"),
   ("(all||wdone(p,15))).length;o.gz=gn;","(all||wdone(p,11))).length;o.gz=gn;")]
for f in FILES:
    s=open(f,encoding='utf-8').read()
    for a,b in R:
        c=s.count(a)
        if c!=1: sys.exit(f'{f}: {a[:50]!r} count {c}')
        s=s.replace(a,b)
    open(f,'w',encoding='utf-8').write(s); print('ok',f)
