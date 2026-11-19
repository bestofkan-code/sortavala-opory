# «План в PDF»: подложки «Яндекс карта» и «Яндекс спутник». Плитки Яндекса в EPSG:3395 — пересобираем их на сетку EPSG:3857 (как слой yam/yas на карте), scale=2.
import sys
fn=sys.argv[1];s=open(fn,encoding='utf-8').read()
def rep(a,b):
    global s
    assert s.count(a)==1,(s.count(a),a[:80]);s=s.replace(a,b)
rep('<option value="esri">спутник Esri</option></select>','<option value="esri">спутник Esri</option><option value="ya">подложка Яндекс карта</option><option value="yas">Яндекс спутник</option></select>')
rep("g.save();g.beginPath();g.rect(mx,my,mw,mh);g.clip();g.fillStyle='#e8e8e8';g.fillRect(mx,my,mw,mh);let ok=0,n=0,q=0;",
"""const YAB=o.base=='ya'||o.base=='yas',yU=o.base=='yas'?'https://core-sat.maps.yandex.net/tiles?l=sat&x={x}&y={y}&z={z}&scale=2&lang=ru_RU':'https://core-renderer-tiles.maps.yandex.net/tiles?l=map&x={x}&y={y}&z={z}&scale=2&lang=ru_RU';
const ytile=async(a,b)=>{const N=256*Math.pow(2,z),E=0.0818191908426,f=Math.atan(Math.sinh(Math.PI*(1-2*b*256/N))),sn=Math.sin(f),Yp=(0.5-Math.log(Math.tan(Math.PI/4+f/2)*Math.pow((1-E*sn)/(1+E*sn),E/2))/(2*Math.PI))*N,ty=Math.floor(Yp/256),off=Yp-ty*256;
 const cv=document.createElement('canvas');cv.width=cv.height=512;const c2=cv.getContext('2d');let k2=0;for(const i of [0,1]){const im=await loadTile(yU.replace('{x}',a).replace('{y}',ty+i).replace('{z}',z));if(im){k2++;c2.drawImage(im,0,(i*256-off)*2,512,512)}}return k2?cv:null};
g.save();g.beginPath();g.rect(mx,my,mw,mh);g.clip();g.fillStyle='#e8e8e8';g.fillRect(mx,my,mw,mh);let ok=0,n=0,q=0;""")
rep("im=await loadTile(url(a,b));n++;","im=await (YAB?ytile(a,b):loadTile(url(a,b)));n++;")
rep("const at=o.base=='esri'?'Подложка: Esri World Imagery':","const at=o.base=='esri'?'Подложка: Esri World Imagery':o.base=='ya'||o.base=='yas'?'Подложка: © Яндекс':")
open(fn,'w',encoding='utf-8').write(s);print('ok')
