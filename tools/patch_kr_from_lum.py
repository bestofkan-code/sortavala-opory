import sys
a="else{p.w=p.w||{};if(on)p.w[k]=d;else delete p.w[k]}}"
b="else{p.w=p.w||{};if(on)p.w[k]=d;else delete p.w[k];if(k==6&&on&&!p.w[12]){p.w[12]=d;if(!(+p.kr))p.kr=1}}}"
for f in ['redaktor.html','montazh.html','prosmotr.html']:
    t=open(f).read()
    i=t.index('function setW(p,k,on,d){');j=t.index('\n',i)
    seg=t[i:j]
    if seg.count(a)!=1:sys.exit(f+' miss')
    t=t[:i]+seg.replace(a,b)+t[j:]
    open(f,'w').write(t);print(f,'ok')
