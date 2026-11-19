# Сверка: у опор, которые можно сверить (есть котлован или закладная), но ещё не сверены — значок-крестик (красный ✕) на том же месте, где галочка.
# Только в редакторе (VF_ON): на просмотре и монтажной карте крестиков нет.
import sys
fn=sys.argv[1];s=open(fn,encoding='utf-8').read()
a="function vfBadge(p){if(!p.vf)return '';const b=vfBad(p),"
assert s.count(a)==1
s=s.replace(a,"function vfOn(){try{return VF_ON}catch(e){return false}}\nfunction vfBadge(p){if(!p.vf){if(!(vfOn()&&vfEl(p)))return '';const x=(typeof mode!='undefined'&&mode=='sp')?17:12.5,y=(typeof mode!='undefined'&&mode=='sp')?0:-12.5;return `<g transform=\"translate(${x} ${y})\"><circle r=\"6.2\" fill=\"#dc2626\" stroke=\"#fff\" stroke-width=\"1.5\"/><path d=\"M-2.5-2.5L2.5 2.5M-2.5 2.5L2.5-2.5\" stroke=\"#fff\" stroke-width=\"1.9\" stroke-linecap=\"round\"/></g>`}const b=vfBad(p),")
open(fn,'w',encoding='utf-8').write(s);print('ok')
