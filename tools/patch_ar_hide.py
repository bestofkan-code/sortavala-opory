# Скрыть блок «Арматура СИП» в окне опоры на основной карте (редактор, просмотр и собранные из них карты); на монтажной карте (montazh) блок остаётся
import sys
fn=sys.argv[1];s=open(fn,encoding='utf-8').read()
def rep(a,b):
    global s
    assert s.count(a)==1,(s.count(a),a[:80]);s=s.replace(a,b)
rep("${odTxt(p)}<div data-arb></div><button data-h>","${odTxt(p)}${AR_SHOW?'<div data-arb></div>':''}<button data-h>")
rep("""<div class="phb" data-phb2 hidden></div><div class="arb" data-arb></div>""","""<div class="phb" data-phb2 hidden></div>${AR_SHOW?'<div class="arb" data-arb></div>':''}""")
rep("function arTxt(p){","const AR_SHOW=/montazh/i.test(location.pathname);\nfunction arTxt(p){")
open(fn,'w',encoding='utf-8').write(s);print('ok')
