# Окно опоры компактнее: меньше высота плиток работ и полей, галочки в одну строку,
# на широком экране (от 700 px) окно шире (420 px) и работы в 3 колонки
import sys
fn=sys.argv[1];s=open(fn,encoding='utf-8').read()
def rep(a,b):
    global s
    assert s.count(a)==1,(s.count(a),a[:80]);s=s.replace(a,b)
rep("const PO=()=>({closeOnClick:false,minWidth:250,maxWidth:300,","const PO=()=>({closeOnClick:false,minWidth:250,maxWidth:innerWidth>=700?440:300,")
rep("function popup0(p){if(RO)return roPopup(p);const d=document.createElement('div');d.className='pp';","function popup0(p){if(RO)return roPopup(p);const d=document.createElement('div');d.className='pp'+(innerWidth>=700?' cw':'');")
CSS=(".pp .yco{font-size:11px;margin:1px 0 3px;gap:5px}.pp .yco button{font-size:10.5px;padding:1px 6px}.pp .yco a{font-size:10.5px}"
".pp .g3p{gap:2px 4px;margin:3px 0}.pp .g3p label{font-size:10px;line-height:1.15}.pp .g3p select{height:24px;padding:1px 4px}"
".pp .g3p .ck2{grid-column:1/-1;flex-direction:row;flex-wrap:wrap;gap:2px 14px;justify-content:flex-start;margin-top:1px}"
".pp .wh{margin:4px 0 2px}.pp .wg{gap:3px}.pp .wt,.pp .wt button{height:26px}.pp .wt button{font-size:11.5px}.pp .wt .wn i{width:14px;height:14px}"
".pp.cw{width:420px}.pp.cw .wg{grid-template-columns:repeat(3,minmax(0,1fr))}.pp.cw .wt .wdt{font-size:9.5px;padding:0 4px 0 1px}.pp.cw .wt .wn{padding:0 2px 0 5px;gap:4px}"
".pp .g2i{margin-top:4px}.pp .g2i input{height:24px}.pp .brow{margin-top:4px}.pp .brow button{height:26px}")
rep("function popup0(p){","document.head.insertAdjacentHTML('beforeend','<style>"+CSS+"</style>');\nfunction popup0(p){")
open(fn,'w',encoding='utf-8').write(s);print('ok')
