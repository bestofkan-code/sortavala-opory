# Все линии СИП сплошные: без пунктира «предположительная связь» и пунктира к серым опорам — на карте и в PDF.
# (Пунктир остаётся только у бронекабеля, это не СИП.)
import sys
p=sys.argv[1];s=open(p,encoding='utf-8').read()
def R(a,b,n=1):
    global s
    assert s.count(a)==n,(a[:90],s.count(a));s=s.replace(a,b)
R("color:'#6b7280',weight:2.5,opacity:.85,dashArray:'6 5',interactive:false","color:'#6b7280',weight:3,opacity:.9,interactive:false")
R("{color:tc,weight:4,opacity:1,dashArray:dash,interactive:false}","{color:tc,weight:4,opacity:1,interactive:false}")
R("g.setLineDash(sg[2]?[lw*4,lw*3]:[]);","g.setLineDash([]);")
R("g.setLineDash(c=='n'||c=='r'?[lw*4,lw*3]:[]);","g.setLineDash([]);")
R("['l','Связь предположительная','#1d4ed8',[1.2*u,.9*u]],","")
R("['#1d4ed8','Связь предположительная',[1.2*u,.9*u]],","")
R("dashArray:k=='n'?'6 6':k=='x'||k=='c'?'9 6':null,","dashArray:null,")
open(p,'w',encoding='utf-8').write(s);print('ok solid',p)
