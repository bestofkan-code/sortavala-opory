# «План в PDF»: без количеств — убраны блок «Опоры на плане / Всего по объекту», таблица «По подстанциям»
# и «(N шт.)» в заголовке; на листе остаются карта и условные обозначения
import sys
fn=sys.argv[1];s=open(fn,encoding='utf-8').read()
def rep(a,b):
    global s
    assert s.count(a)==1,(s.count(a),a[:80]);s=s.replace(a,b)
i=s.find("y+=2*u;g.textBaseline='alphabetic';g.font=`bold ${3.8*u}px ${F}`;g.fillText(SHT.length<P.length?'Опоры на плане':'Всего по объекту',px,y)")
j=s.find("g.font=`${2.3*u}px ${F}`;g.fillStyle='#555';g.fillText('Положение опор приблизительное.'",i)
assert i>0 and j>i and j-i<6000,(i,j)
s=s[:i]+"g.textBaseline='alphabetic';"+s[j:]
rep("(o.title||`Общий план, все опоры (${P.length} шт.)`)","(o.title||'Общий план, все опоры')")
rep("title:(f?'План: '+f:'Общий план')+`, все опоры (${L2.length} шт.)`","title:(f?'План: '+f:'Общий план')+', все опоры'")
rep("title:'Опоры в работе'+(f?', '+f:'')+` (${L2.length} шт.)`","title:'Опоры в работе'+(f?', '+f:'')")
open(fn,'w',encoding='utf-8').write(s);print('ok')
