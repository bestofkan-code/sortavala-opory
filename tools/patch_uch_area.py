#!/usr/bin/env python3
"""Кнопка «1|2»: заливка ОБЛАСТЕЙ участков 1 и 2 (после patch_uch_fill.py).
Каждая точка карты в пределах ~60 м от опор красится цветом участка ближайшей опоры
(синий — участок 1, оранжевый — участок 2), по линии раздела областей рисуется граница.
Рисуется на холсте под значками опор, перерисовывается после сдвига и масштабирования.
Применение:
  for f in redaktor.html prosmotr.html zamechaniya.html zamechaniya-prosmotr.html montazh.html uchastki.html; do python3 tools/patch_uch_area.py $f; done
"""
import sys, re
path = sys.argv[1]
s = open(path, encoding='utf-8').read()
if 'function ufArea(' in s:
    print('already applied', path); sys.exit(0)
a = s.index('function ufDraw(){try{')
b = s.index('function ufToggle(){')
NEW = r"""function ufDraw(){ufUI();ufArea()}
var UFCV=null,UFRM=60;
function ufArea(){try{
 if(!map.getPane('ucp')){const p=map.createPane('ucp');p.style.zIndex=450;p.style.pointerEvents='none'}
 const pane=map.getPane('ucp');pane.style.opacity=1;
 if(!UFCV){UFCV=document.createElement('canvas');UFCV.style.position='absolute';UFCV.style.pointerEvents='none';pane.appendChild(UFCV)}
 const cv=UFCV,sz=map.getSize();if(!UFON){cv.style.display='none';return}cv.style.display='';
 const dpr=1,W=sz.x,H=sz.y;cv.width=W;cv.height=H;cv.style.width=W+'px';cv.style.height=H+'px';
 L.DomUtil.setPosition(cv,map.containerPointToLayerPoint([0,0]));
 const ctx=cv.getContext('2d');ctx.clearRect(0,0,W,H);
 const z=map.getZoom(),mpp=40075016.686*Math.cos(61.71*Math.PI/180)/Math.pow(2,z+8),R=Math.max(12,UFRM/mpp),R2=R*R;
 const pts=[];P.forEach(p=>{if(!p||!p.tp||(p.x&&!p.sx))return;const c=map.latLngToContainerPoint([p.lat,p.lon]);if(c.x<-R||c.y<-R||c.x>W+R||c.y>H+R)return;pts.push([c.x,c.y,ucOf(p)])});
 const G=new Map(),key=(i,j)=>i+','+j;pts.forEach(q=>{const k=key(Math.floor(q[0]/R),Math.floor(q[1]/R));if(!G.has(k))G.set(k,[]);G.get(k).push(q)});
 const st=Math.max(3,Math.round(Math.min(W,H)/260)),nx=Math.ceil(W/st),ny=Math.ceil(H/st),A=new Uint8Array(nx*ny);
 for(let j=0;j<ny;j++){const y=j*st+st/2,gj=Math.floor(y/R);for(let i=0;i<nx;i++){const x=i*st+st/2,gi=Math.floor(x/R);let bd=R2,bu=0;
  for(let a=-1;a<=1;a++)for(let b=-1;b<=1;b++){const L2=G.get(key(gi+a,gj+b));if(!L2)continue;for(const q of L2){const dx=q[0]-x,dy=q[1]-y,d=dx*dx+dy*dy;if(d<bd){bd=d;bu=q[2]}}}
  A[j*nx+i]=bu}}
 const C={1:'rgba(37,99,235,.33)',2:'rgba(249,115,22,.38)'},E={1:'rgba(29,78,216,.9)',2:'rgba(194,65,12,.9)'};
 for(let j=0;j<ny;j++)for(let i=0;i<nx;i++){const u=A[j*nx+i];if(!u)continue;ctx.fillStyle=C[u];ctx.fillRect(i*st,j*st,st,st)}
 ctx.fillStyle='rgba(124,58,237,.95)';
 for(let j=0;j<ny;j++)for(let i=0;i<nx;i++){const u=A[j*nx+i];if(!u)continue;const r=i+1<nx?A[j*nx+i+1]:0,d=j+1<ny?A[(j+1)*nx+i]:0;
  if(r&&r!==u)ctx.fillRect(i*st+st-1.5,j*st-1,3,st+2);if(d&&d!==u)ctx.fillRect(i*st-1,j*st+st-1.5,st+2,3)}
 for(let j=0;j<ny;j++)for(let i=0;i<nx;i++){const u=A[j*nx+i];if(!u)continue;const r=i+1<nx?A[j*nx+i+1]:0,l=i>0?A[j*nx+i-1]:0,d=j+1<ny?A[(j+1)*nx+i]:0,t=j>0?A[(j-1)*nx+i]:0;
  if(!r||!l||!d||!t){ctx.fillStyle=E[u];ctx.fillRect(i*st,j*st,st,st)}}
}catch(e){console.log('ufArea',e)}}
"""
s = s[:a] + NEW + s[b:]
# перерисовка после сдвига/масштаба вместо подстройки толщины линий
old = "map.on('zoomend',()=>{if(UFON){const w=ufW();UFL.forEach(l=>l.setStyle({weight:w}))}});"
assert s.count(old) == 1, (path, 'zoomend hook')
s = s.replace(old, "map.on('moveend zoomend resize',()=>{if(UFON)ufArea()});map.on('zoomstart',()=>{if(UFCV)UFCV.style.display='none'});")
open(path, 'w', encoding='utf-8').write(s); print('ok', path)
