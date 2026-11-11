# Сборка страниц из redaktor.html

Основной файл — `redaktor.html`. Остальные страницы собираются из него:

```
sed 's#const RO=/\*RO\*/false;#const RO=true;#' redaktor.html > prosmotr.html
python3 tools/patch_tn.py redaktor.html tools/tn_remarks.json zamechaniya.html
python3 tools/patch_tn.py prosmotr.html tools/tn_remarks.json zamechaniya-prosmotr.html
python3 tools/patch_crew.py redaktor.html montazh.html     # «монтажная карта» для бригады монтажников (использует tools/crew.js)
python3 tools/patch_zones.py redaktor.html uchastki.html   # «Участки работ»: письма и схемы по участкам (использует tools/zones.js)
```

`montazh.html` («монтажная карта») — вход только для учётной записи бригады (`montazh@…`, роль `crew` в Supabase). Кронштейны на значке опоры там рисуются крупнее, с белой обводкой и цветом по типу (1-рожк. — тёмный, 2-рожк. 90° — оранжевый, 180° — фиолетовый; пунктир — не установлен), легенда — в панели.
Сервер разрешает этой роли менять только работы 5 (СИП), 6 (светильник), 12 (кронштейн), 14 (подрезка крон бригадой — отдельно от нашей 9),
комментарий по работам, длины СИП по пролётам (таблица spans) и на ТП — «Проложен бронекабель» и длину кабеля.

Таблица «Контракт и выполнение» в шапке: `python3 tools/patch_main_contract.py redaktor.html` (уже применено) — опоры по типам (397/183/5/7), закладные (402/190), кронштейны (353/50/189), светильники (831): контракт / на карте / сделано / осталось. На монтажной карте скрыта.

СИП-карта (кнопка под таблицей «Контракт и выполнение»): `python3 tools/patch_main_sip.py redaktor.html` (уже применено; код в `tools/sip.js`) — магистраль и ответвления, длины пролётов, роль опоры на линии, расчёт арматуры и Excel.

Фильтр «Опоры» (стандартные/анкерные, 8/9 м): `python3 tools/patch_main_ptype.py redaktor.html` (уже применено).

Задания бригаде: `python3 tools/patch_main_tasks.py redaktor.html` (уже применено; код в `tools/tasks.js`).
В основной карте режим «Задания бригаде» — выделить опоры, виды работ, срок → таблица `crew_tasks`;
на монтажной карте задания показаны в панели «Задания» и кольцами вокруг опор.

Участки работ (`uchastki.html`, код в `tools/zones.js`): выделить опоры участка (нажатием или обводом), даты и время, виды работ и что нужно —
освободить места у опор (письмо в пресс-службу + объявление для жителей), отключение ВЛ 0,4 кВ (письмо в Россети), автовышка на проезжей части (письмо в ГИБДД).
Кнопка «Документы» собирает архив в папке «Участок <название> <даты>»: схема участка (PDF, A4) и письма (DOCX). Реквизиты писем — кнопка «Реквизиты писем» (хранятся в браузере).
Участки хранятся в таблице `work_zones` (если её нет — только в браузере):
```sql
create table if not exists public.work_zones(id text primary key, name text not null, uids text[] not null default '{}', works int[] not null default '{}',
 d1 date, d2 date, t1 text, t2 text, lift boolean not null default false, road boolean not null default false, outage boolean not null default false,
 park boolean not null default true, note text, sent jsonb not null default '{}'::jsonb, done boolean not null default false, ed text, updated_at timestamptz not null default now());
alter table public.work_zones enable row level security;
create policy wz_read on public.work_zones for select to anon, authenticated using (true);
create policy wz_write on public.work_zones for all to authenticated using (not public.is_crew()) with check (not public.is_crew());
```

- `patch_main_brackets.py` — блок «Проверка кронштейнов» под «Контракт и выполнение»: по ТП 1-рожк./90°/180° (установлено из всего), тип не указан, «можно ставить», замечания по опорам (нажать — карта покажет опору), выгрузка «Таблица проверки (Excel)».
