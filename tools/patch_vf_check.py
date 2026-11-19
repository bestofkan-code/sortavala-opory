# Сверка: вместо кольца — значок-галочка у опоры (зелёный ✓ — сверено, всё верно; оранжевый ! — сверено с расхождением)
import sys
fn=sys.argv[1];s=open(fn,encoding='utf-8').read()
def rep(a,b):
    global s
    assert s.count(a)==1,(s.count(a),a[:80]);s=s.replace(a,b)
rep("""function vfRing(p){if(!p.vf)return '';const k=p.vk&&!p.x;return `<circle r="${k?20.5:17.5}" fill="none" stroke="${vfBad(p)?'#f97316':'#16a34a'}" stroke-width="${k?3.6:3}"/>`}""",
"""function vfRing(p){return ''}
function vfBadge(p){if(!p.vf)return '';const b=vfBad(p),x=(typeof mode!='undefined'&&mode=='sp')?17:12.5,y=(typeof mode!='undefined'&&mode=='sp')?0:-12.5;return `<g transform="translate(${x} ${y})"><circle r="6.6" fill="${b?'#f97316':'#16a34a'}" stroke="#fff" stroke-width="1.5"/>${b?'<path d="M0-3.6V0.9" stroke="#fff" stroke-width="2.1" stroke-linecap="round"/><circle cy="3.4" r="1.15" fill="#fff"/>':'<path d="M-3.2 0.1L-0.9 2.5L3.3-2.4" fill="none" stroke="#fff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>'}</g>`}""")
rep("v+=sqIco(p);return L.divIcon({html:v+'</svg>'","v+=vfBadge(p)+sqIco(p);return L.divIcon({html:v+'</svg>'")
open(fn,'w',encoding='utf-8').write(s);print('ok')
