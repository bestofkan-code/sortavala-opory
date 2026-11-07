# Сборка страниц из redaktor.html

Основной файл — `redaktor.html`. Остальные страницы собираются из него:

```
sed 's#const RO=/\*RO\*/false;#const RO=true;#' redaktor.html > prosmotr.html
python3 tools/patch_tn.py redaktor.html tools/tn_remarks.json zamechaniya.html
python3 tools/patch_tn.py prosmotr.html tools/tn_remarks.json zamechaniya-prosmotr.html
python3 tools/patch_crew.py redaktor.html montazh.html     # карта бригады монтажников (использует tools/crew.js)
```

`montazh.html` — вход только для учётной записи бригады (`montazh@…`, роль `crew` в Supabase).
Сервер разрешает этой роли менять только работы 5 (СИП), 6 (светильник), 9 (подрезка крон), 12 (кронштейн),
комментарий по работам, длины СИП по пролётам (таблица spans) и на ТП — «Проложен бронекабель» и длину кабеля.
