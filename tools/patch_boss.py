# -*- coding: utf-8 -*-
"""Данные сметы, РД и ППР на картах — только для двух учётных записей (Иль, Женя).

Числа из сметы и РД убраны из кода страниц: страница получает их из таблицы
public.boss_cfg (Supabase), которую по RLS читают только эти две учётные записи.
Остальные видят карту и ход работ без контрактных итогов, сверок со сметой,
«Участков по смете», отчёта для сметы и колонки «По РД».

Применять к каждой странице:  python3 tools/patch_boss.py <file.html> [...]
"""
import re, sys

def rep(s, a, b, cnt, name):
    n = s.count(a)
    cnt[name] = cnt.get(name, 0) + n
    return s.replace(a, b)

HEAD = """<style>/*BOSS*/html:not(.boss) .bossonly,html:not(.boss) #ucb,html:not(.boss) #ucs,html:not(.boss) #ufbtn,html:not(.boss) #uflg,html:not(.boss) #spx,html:not(.boss) #ktd{display:none!important}</style>
<script>var BOSS=false,CFG={KCP:0,LUM:0,SIPM:0,GZ:0,ZS:0,ZA:0};</script>
</head>"""

TAIL = """<script>/*BOSSLOAD*/(function(){
let busy=0;
function apply(v){const was=BOSS;BOSS=!!v;
 if(was&&!BOSS){location.reload();return}
 document.documentElement.classList.toggle('boss',BOSS);if(!BOSS)return;
 try{Object.assign(CFG,v)}catch(e){}
 try{if(typeof KCT!='undefined'&&v.KCT)Object.assign(KCT,v.KCT)}catch(e){}
 try{if(typeof KCP!='undefined'&&v.KCP)KCP=v.KCP}catch(e){}
 try{if(typeof SIPRD!='undefined'&&v.SIPRD)Object.assign(SIPRD,v.SIPRD)}catch(e){}
 try{if(typeof UCOV!='undefined'&&v.UCOV)v.UCOV.forEach(u=>UCOV.add(u))}catch(e){}
 try{if(typeof UC2TP!='undefined'&&v.UC2TP)v.UC2TP.forEach(u=>UC2TP.add(u))}catch(e){}
 try{if(typeof KTC!='undefined'&&v.KTC){KTC.op.forEach((r,i)=>r[4]=v.KTC.op[i]);KTC.zk.forEach((r,i)=>r[3]=v.KTC.zk[i]);KTC.kr.forEach((r,i)=>r[2]=v.KTC.kr[i]);KTC.lum=v.KTC.lum}}catch(e){}
 try{if(typeof KRG!='undefined'){KRG[0][1]=KCT['1'];KRG[1][1]=KCT['90'];KRG[2][1]=KCT['180']}}catch(e){}
 try{if(typeof KLUM!='undefined')KLUM=CFG.LUM}catch(e){}
 try{P.forEach(upd);numLabels()}catch(e){}
 try{if(typeof crewStats=='function')crewStats()}catch(e){}
 try{stats()}catch(e){}
 try{if(typeof sipStats=='function')sipStats()}catch(e){}
 try{if(typeof ufDraw=='function')ufDraw()}catch(e){}
}
async function load(){if(busy)return;busy=1;try{let s=null;try{s=JSON.parse(localStorage.getItem(KEY+'_auth')||'null')}catch(e){}
 if(!s||!s.at||!CF){apply(null);return}
 const r=await fetch(CF.u+'/rest/v1/boss_cfg?select=v&k=eq.cfg',{headers:{apikey:CF.k,Authorization:'Bearer '+s.at}});
 const j=r.ok?await r.json():[];apply(Array.isArray(j)&&j[0]?j[0].v:null)}catch(e){apply(null)}finally{busy=0}}
window.bossLoad=load;
try{if(typeof authUI=='function'){const a=authUI;authUI=function(){const x=a.apply(this,arguments);setTimeout(load,0);return x}}}catch(e){}
setTimeout(load,0);
})();</script>
</body>"""


def patch(s):
    c = {}
    if '/*BOSS*/' in s:
        return s, {'уже применён': 1}
    s = s.replace('</head>', HEAD, 1)
    i = s.rfind('</body>')
    s = s[:i] + TAIL + s[i + len('</body>'):]

    # --- константы сметы и РД ---
    s = rep(s, "var KCT={'1':0,'90':0,'180':0},KCP=0", "var KCT={'1':0,'90':0,'180':0},KCP=0", c, 'KCT')
    s = rep(s, "var SIPRD={};", "var SIPRD={};", c, 'SIPRD')
    s = rep(s, "var UCOV=new Set();", "var UCOV=new Set();", c, 'UCOV')
    s = rep(s, "var UC2TP=new Set();", "var UC2TP=new Set();", c, 'UC2TP')
    m = re.search(r"var KTC=\{op:\[.*?lum:0\}", s, re.S)
    if m:
        k = m.group(0)
        k2 = re.sub(r"(\['[^']+','ОГС [^']+','[SA]',[89],)\d+\]", r"\g<1>0]", k)
        k2 = re.sub(r"(\['[^']+','ФМ-[^']+','[SA]',)\d+\]", r"\g<1>0]", k2)
        k2 = re.sub(r",(353|50|189)\]", ",0]", k2)
        k2 = k2.replace('lum:0}', 'lum:0}')
        s = s.replace(k, k2); c['KTC'] = 1

    # --- «Контракт и выполнение» ---
    s = rep(s, "function ktUI(){const t=$('ktt');if(!t)return;", "function ktUI(){const t=$('ktt');if(!t)return;if(!BOSS)return;", c, 'ktUI')

    # --- «Ход работ» в шапке ---
    s = rep(s, "$('st').innerHTML=(()=>{const K=0,", "$('st').innerHTML=(()=>{const K=CFG.KCP,", c, 'st K')
    s = rep(s, "${v} из ${K} <small style=\"color:#555;font-weight:400\">(${Math.round(v/K*1000)/10}%) · осталось ${Math.max(0,K-v)}</small></b></div>`+bar(v,c);",
            "${v}${K?` из ${K} <small style=\"color:#555;font-weight:400\">(${Math.round(v/K*1000)/10}%) · осталось ${Math.max(0,K-v)}</small>`:''}</b></div>`+(K?bar(v,c):'');", c, 'st ln')
    s = rep(s, "<b>По контракту в этом этапе: ${K} опор</b> <small style=\"color:#555\">весь объект, без учёта фильтров</small>",
            "<b>${K?'По контракту в этом этапе: '+K+' опор':'Ход работ'}</b> <small style=\"color:#555\">весь объект, без учёта фильтров</small>", c, 'st head')
    s = rep(s, "MS=WF?Math.max(0,0-", "MS=WF&&BOSS?Math.max(0,CFG.KCP-", c, 'MS')
    s = rep(s, "${WF?'':'<small>Таблица по выбранным фильтрам; контракт 0 считается без фильтров.</small>'}",
            "${WF?'':'<small>Таблица по выбранным фильтрам'+(BOSS?'; контракт '+CFG.KCP+' считается без фильтров':'')+'.</small>'}", c, 'st note')

    s = rep(s, "ln=(nm,v,T,c,u)=>`<div", "ln=(nm,v,T,c,u)=>!T?`<div style=\"display:flex;justify-content:space-between;gap:6px\"><span>${nm}</span><b style=\"color:${c}\">${u?'≈ ':''}${v.toLocaleString('ru-RU')}${u||''}</b></div>`:`<div", c, 'hw ln')
    s = rep(s, "ln('СИП протянут',L,0,", "ln('СИП протянут',L,CFG.SIPM,", c, 'hw sip')
    s = rep(s, "ln('Светильников установлено',sv,0,", "ln('Светильников установлено',sv,CFG.LUM,", c, 'hw lum')
    s = rep(s, "ln('1-рожковые',kc('1'),KCT['1'],'#0f172a')+ln('2-рожковые 90°',kc('90'),KCT['90'],'#ea580c')+ln('2-рожковые 180°',kc('180'),KCT['180'],'#7c3aed')",
            "ln('1-рожковые',kc('1'),KCT['1'],'#0f172a')+ln('2-рожковые 90°',kc('90'),KCT['90'],'#ea580c')+ln('2-рожковые 180°',kc('180'),KCT['180'],'#7c3aed')", c, 'hw kr')
    s = rep(s, "B.filter(p=>wdone(p,11)).length,92,'#a16207')", "B.filter(p=>wdone(p,11)).length,CFG.GZ,'#a16207')", c, 'hw gz')
    s = rep(s, "+'<small style=\"color:#555;display:block;margin:-2px 0 4px\">Светильники, кронштейны и СИП — из сметы (0 шт., N/N/N шт., N м), котлованы под заземление — по числу комплектов повторного заземления (92). СИП — приблизительно, по длинам пролётов на карте, где на обеих опорах отмечен СИП.</small>'}",
            "+(BOSS?'<small style=\"color:#555;display:block;margin:-2px 0 4px\">Светильники, кронштейны и СИП — из сметы ('+CFG.LUM+' шт., '+KCT['1']+'/'+KCT['90']+'/'+KCT['180']+' шт., '+CFG.SIPM.toLocaleString('ru-RU')+' м), котлованы под заземление — по числу комплектов повторного заземления ('+CFG.GZ+'). СИП — приблизительно, по длинам пролётов на карте, где на обеих опорах отмечен СИП.</small>':'<small style=\"color:#555;display:block;margin:-2px 0 4px\">СИП — приблизительно, по длинам пролётов на карте, где на обеих опорах отмечен СИП.</small>')}", c, 'hw note')
    s = rep(s, "function hwAllH(A){const K=0,", "function hwAllH(A){if(!BOSS)return '';const K=CFG.KCP,", c, 'hwAll')
    s = rep(s, "['свет.',pc(sv,0)],['СИП',pc(L,0)]]", "['свет.',pc(sv,CFG.LUM)],['СИП',pc(L,CFG.SIPM)]]", c, 'hwAll lum')
    s = rep(s, "кронштейны (из 0), светильники (из 0), СИП (из N м).",
            "кронштейны (из ${CFG.KCP}), светильники (из ${CFG.LUM}), СИП (из ${CFG.SIPM.toLocaleString('ru-RU')} м).", c, 'hwAll note')

    # --- выгрузки «Проверка котлованов» и «Проверка кронштейнов»: строки «По контракту» ---
    s = rep(s, "K=0,KS=402,KA=190;", "K=CFG.KCP,KS=CFG.ZS,KA=CFG.ZA;", c, 'fd K')
    s = rep(s, "K={'1':0,'90':0,'180':0};", "K=KCT;", c, 'kc K')
    for start in ("['По контракту',K,'',K-S.k,", "['По контракту',K['1'],"):
        while True:
            a = s.find(start)
            if a < 0 or s[a - 10:a].endswith('(BOSS?['):
                break
            b = s.find("['Разница карта − контракт',", a)
            e = s.find("],[],", b)
            if b < 0 or e < 0 or b - a > 400 or e - b > 400:
                break
            s = s[:a] + '...(BOSS?[' + s[a:e + 1] + ']:[]),[],' + s[e + len('],[],'):]
            c['contract rows'] = c.get('contract rows', 0) + 1

    # --- кронштейны: сверка со сметой, подсказки, новая опора ---
    s = rep(s, "function kcSm(){const e=$('kcm');if(!e)return;", "function kcSm(){const e=$('kcm');if(!e)return;if(!BOSS){e.innerHTML='';return}", c, 'kcSm')
    s = rep(s, "опор больше контракта (0)", "опор больше контракта (${KCP})", c, 'kc592a')
    s = rep(s, "меньше контракта (0)", "меньше контракта (${KCP})", c, 'kc592b')
    s = rep(s, "не хватает до 0, нужно дать", "не хватает до ${KCP}, нужно дать", c, 'kc592c')
    s = rep(s, "«Котлованов осталось» в строке «По контракту» — до 0.", "«Котлованов осталось» в строке «По контракту» — до числа опор по контракту.", c, 'fd note')
    s = rep(s, "function kcOver(p){", "function kcOver(p){if(!BOSS)return;", c, 'kcOver')
    s = rep(s, "if(c0.n>=KCP)toast(", "if(BOSS&&c0.n>=KCP)toast(", c, 'addAt')
    s = rep(s, "'не задан — по смете типов не осталось')+' · '+kcLeftTxt())}", "(BOSS?'не задан — по смете типов не осталось':'не задан'))+(BOSS?' · '+kcLeftTxt():''))}", c, 'addAt2')
    s = rep(s, "не предлагать в подсказках до сметы", "не предлагать в подсказках", c, 'kok')

    # --- СИП-карта: колонка «По РД» ---
    s = rep(s, "miss=ALL?Math.max(0,0-", "miss=ALL&&BOSS?Math.max(0,CFG.KCP-", c, 'sip miss')
    s = rep(s, "(ALL?'По РД':'')", "(ALL&&BOSS?'По РД':'')", c, 'sip col')
    s = rep(s, "rd=!ALL?'':", "rd=!(ALL&&BOSS)?'':", c, 'sip rd')
    s = rep(s, "'По РД (0 опоры)'", "(BOSS?'По РД ('+CFG.KCP+' опор)':'')", c, 'sip xl h')
    s = rep(s, "ALL?(r[6]?SIPRD[r[6]]:'нет в РД'):''", "ALL&&BOSS?(r[6]?SIPRD[r[6]]:'нет в РД'):''", c, 'sip xl')
    s = rep(s, " (в РД — SO250.01)", "", c, 'so250')
    s = rep(s, " (в РД — SO260)", "", c, 'so260')
    s = rep(s, "По РД — спецификации участков 1 и 2 на 0 опоры; «—» — в РД нет. Анкерные SO250.01 и подвески SO260 в РД рассчитаны на несущую нулевую жилу, а у СИП-4 4×25 её нет: зажимы нужны на 4-жильный жгут — уточнить у проектировщика или поставщика.",
            "${BOSS?'По РД — спецификации участков 1 и 2 на '+CFG.KCP+' опор; «—» — в РД нет. Анкерные и поддерживающие зажимы по РД рассчитаны на несущую нулевую жилу, а у СИП-4 4×25 её нет: зажимы нужны на 4-жильный жгут.':''}", c, 'sip note')
    s = rep(s, ",['В РД SO250.01 и SO260 — арматура под несущую нулевую жилу; у СИП-4 4×25 её нет, нужны зажимы на 4-жильный жгут — уточнить у проектировщика или поставщика.']]",
            "].concat(BOSS?[['Зажимы по РД рассчитаны на несущую нулевую жилу; у СИП-4 4×25 её нет, нужны зажимы на 4-жильный жгут.']]:[])", c, 'sip xl note')

    # --- монтажная карта (бригада): итоги без контрактных чисел ---
    s = rep(s, "var KRG=[['1-рожковые',null,p=>(+p.kr||0)==1],['2-рожк. 90°',null,p=>(+p.kr||0)==2&&+p.ka==90],['2-рожк. 180°',null,p=>",
            "var KRG=[['1-рожковые',null,p=>(+p.kr||0)==1],['2-рожк. 90°',null,p=>(+p.kr||0)==2&&+p.ka==90],['2-рожк. 180°',null,p=>", c, 'crew KRG')
    s = rep(s, "]],KLUM=0;", "]],KLUM=null;", c, 'crew KLUM')
    s = rep(s, "${ALL?'<td>'+KLUM+'</td>':''}", "${ALL?'<td>'+(KLUM??'—')+'</td>':''}", c, 'crew KLUM td')
    s = rep(s, "const ALL=!FTS.size&&!(typeof TKONLY!='undefined'&&TKONLY),K=0,", "const ALL=!FTS.size&&!(typeof TKONLY!='undefined'&&TKONLY),K=BOSS?CFG.KCP:Q.length,", c, 'crew K')
    s = rep(s, "`<small style=\"display:block;opacity:.8;margin-bottom:2px\">Итог по контракту: <b>${K} опор</b>", "`<small style=\"display:block;opacity:.8;margin-bottom:2px\">${BOSS?'Итог по контракту':'Итог по карте'}: <b>${K} опор</b>", c, 'crew head')

    # --- совместная подвеска: оценка для сметы ---
    s = rep(s, "function sqEst(){let c;", "function sqEst(){if(!BOSS)return '';let c;", c, 'sqEst')

    # --- участки по смете: заливка ---
    s = rep(s, "if(!UFON){cv.style.display='none';return}", "if(!UFON||!BOSS){cv.style.display='none';return}", c, 'ufArea')

    # --- слова «проект» в отметках ---
    for a, b in [("исключена из проекта", "исключена"), ("Исключена из проекта", "Исключена"),
                 ("исключено из проекта", "исключено"), ("Исключено из проекта", "Исключено"),
                 ("гравит. фундамент по проекту", "гравит. фундамент"), ("гравит. (проект)", "гравит."),
                 ("Гравит. фундамент (проект)", "Гравит. фундамент"), ("пунктир — проект", "пунктир — не установлен"),
                 ("Кронштейн 1-рожк. (проект)", "Кронштейн 1-рожк. (план)"), ("Новая (не в проекте)", "Новая"),
                 ("Добавлена (не в проекте)", "Добавлена (новая)"), ("Добавлено новых (сверх проекта)", "Добавлено новых"),
                 ("по проекту отмечено", "запланировано")]:
        s = rep(s, a, b, c, 'слово: ' + a)
    return s, c


if __name__ == '__main__':
    for f in sys.argv[1:]:
        s = open(f, encoding='utf-8').read()
        s2, c = patch(s)
        open(f, 'w', encoding='utf-8').write(s2)
        miss = [k for k, v in c.items() if not v]
        print(f, '— заменено:', sum(1 for v in c.values() if v), 'не найдено:', ', '.join(miss) if miss else '—')
