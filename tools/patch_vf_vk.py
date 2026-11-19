# Сверка на опоре с вводом КЛ: зелёное (оранжевое) кольцо сверки сливалось с сиреневым кольцом «ввод КЛ» — выносим его наружу (r 20, толще)
import sys
fn=sys.argv[1];s=open(fn,encoding='utf-8').read()
a="""function vfRing(p){if(!p.vf)return '';return `<circle r="17.5" fill="none" stroke="${vfBad(p)?'#f97316':'#16a34a'}" stroke-width="3"/>`}"""
assert s.count(a)==1
s=s.replace(a,"""function vfRing(p){if(!p.vf)return '';const k=p.vk&&!p.x;return `<circle r="${k?20.5:17.5}" fill="none" stroke="${vfBad(p)?'#f97316':'#16a34a'}" stroke-width="${k?3.6:3}"/>`}""")
open(fn,'w',encoding='utf-8').write(s);print('ok')
