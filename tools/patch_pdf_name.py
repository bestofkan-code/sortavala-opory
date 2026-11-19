# Имя PDF-отчёта (и подпись в заголовке листа) по применённым фильтрам:
# вид плана · спецфильтр · виды работ · опоры (тип/высота) · ТП · даты
import sys
fn=sys.argv[1];s=open(fn,encoding='utf-8').read()
def rep(a,b):
    global s
    assert s.count(a)==1,(s.count(a),a[:80]);s=s.replace(a,b)
i=s.find("function pdfName(L2){");j=s.find("\n",i);assert i>0
NEW=r"""function pdfFlt(){const a=[],v=(n)=>{try{return eval(n)}catch(e){return false}};
 if(v('VKF'))a.push('ввод КЛ');if(v('FJ'))a.push('совместная подвеска');if(v('NB'))a.push('не забетонированные');if(v('GY'))a.push('серые (предполагаемые)');if(v('NK'))a.push('не забурены котлованы');if(v('VS'))a.push('не сверены котлованы');
 try{const t=ftyTxt();if(t)a.push(t)}catch(e){}
 const ks=wsel();if(ks.length){const nm=k=>{const w=WK.find(x=>x[0]==k);return w?w[1].toLowerCase():String(k)},neg=$('wm').value!='1';a.push((neg?'не выполнено: ':'')+ks.map(nm).join(ks.length>1&&$('wl').value=='all'?' + ':', '))}
 else if($('wm').value!='1'&&($('wdf').value||$('wdt').value))a.push('работы не выполнены');
 return a}
function pdfName(L2){const r=wDates(L2),t=r?(r[0]==r[1]?rd(r[0]):rd(r[0])+'–'+rd(r[1])):rd(LD()),m=$('parea').value,base=m=='all'?'Общий план':m=='view'?'План участка':'Опоры в работе',F=pdfFlt(),tp=tpLbl();
 const parts=[base].concat(F).concat(tp?[tp]:[]).concat([t]);let f=parts.join(' — ').replace(/[\\/:*?"<>|]+/g,' ').replace(/\s+/g,' ').trim();if(f.length>150)f=f.slice(0,147).trim()+'…';
 return{dl:(r?'работы '+(r[0]==r[1]?rd(r[0]):'с '+rd(r[0])+' по '+rd(r[1])):''),flt:F.join(', '),file:f+'.pdf'}}"""
s=s[:i]+NEW+s[j:]
rep("a.file=n.file;if(n.dl)a.title+=' · '+n.dl;return a}","a.file=n.file;if(n.flt)a.title+=' · '+n.flt;if(n.dl)a.title+=' · '+n.dl;return a}")
rep("if(m=='all'){const L2=P.filter(tpOk);if(!L2.length)return null;return{only:f?L2:null,","if(m=='all'){const sp=pdfFlt().length,L2=P.filter(p=>tpOk(p)&&(!sp||vis(p)));if(!L2.length)return null;return{only:(f||sp)?L2:null,")
open(fn,'w',encoding='utf-8').write(s);print('ok')
