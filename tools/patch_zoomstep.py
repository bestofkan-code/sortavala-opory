# Шаг масштаба карты меньше: кнопки +/− по 0,5 уровня, колесо мыши медленнее, щипок — с шагом 0,25.
import sys
p=sys.argv[1];s=open(p,encoding='utf-8').read()
a="map=L.map('m',{maxZoom:20,rotate:true,"
assert s.count(a)==1;s=s.replace(a,"map=L.map('m',{maxZoom:20,zoomSnap:.25,zoomDelta:.5,wheelPxPerZoomLevel:120,rotate:true,")
open(p,'w',encoding='utf-8').write(s);print('ok zoomstep',p)
