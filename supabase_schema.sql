create table if not exists poles (
  uid text primary key,
  id text, lat double precision, lon double precision,
  t text, g boolean, line text, done boolean, date date, note text,
  tp text, n int, x boolean default false, w jsonb default '{}'::jsonb, wc text, f text, js boolean default false
);
alter table poles add column if not exists tp text;
alter table poles add column if not exists n int;
alter table poles add column if not exists x boolean default false;
alter table poles add column if not exists w jsonb default '{}'::jsonb;
alter table poles add column if not exists wc text;
alter table poles add column if not exists f text;
alter table poles add column if not exists js boolean default false;
alter table poles enable row level security;
drop policy if exists "open" on poles;
create policy "open" on poles for all to anon using (true) with check (true);

create table if not exists draws (
  id text primary key,
  d jsonb
);
alter table draws enable row level security;
drop policy if exists "open" on draws;
create policy "open" on draws for all to anon using (true) with check (true);

-- Двор, адрес и автор изменения
alter table poles add column if not exists yd boolean default false;
alter table poles add column if not exists ad text;
alter table poles add column if not exists ed text;

-- История изменений: каждая правка опоры записывается автоматически
create table if not exists history (
  id bigserial primary key,
  ts timestamptz not null default now(),
  uid text not null,
  op text not null,          -- I добавлена, U изменена, D удалена
  old jsonb,
  new jsonb,
  ed text                    -- кто внёс изменение
);
create index if not exists history_ts_idx on history (ts desc);
create index if not exists history_uid_idx on history (uid, ts desc);
alter table history enable row level security;
drop policy if exists "read" on history;
create policy "read" on history for select to anon using (true);

create or replace function log_pole_change() returns trigger
language plpgsql security definer set search_path = public as $$
declare o jsonb; n jsonb;
begin
  if tg_op = 'DELETE' then
    insert into history(uid, op, old, new, ed) values (old.uid, 'D', to_jsonb(old), null, old.ed);
    return old;
  end if;
  n := to_jsonb(new) - 'ed';
  if tg_op = 'UPDATE' then
    o := to_jsonb(old) - 'ed';
    if o = n then return new; end if;
    insert into history(uid, op, old, new, ed) values (new.uid, 'U', to_jsonb(old), to_jsonb(new), new.ed);
  else
    insert into history(uid, op, old, new, ed) values (new.uid, 'I', null, to_jsonb(new), new.ed);
  end if;
  return new;
end $$;

drop trigger if exists poles_history on poles;
create trigger poles_history after insert or update or delete on poles
for each row execute function log_pole_change();

-- Кронштейн (0 нет, 1 однорожковый, 2 двухрожковый) и число установленных светильников
alter table poles add column if not exists kr int default 0;
alter table poles add column if not exists sv int default 0;

-- Частичное обновление опор: меняются только переданные поля, отметки работ объединяются
-- (полный текст функции pole_patch см. в миграции pole_patch_partial_updates)

-- Доступ: читать могут все (просмотр), менять — только вошедшие в редактор
drop policy if exists "open" on poles;
create policy "read" on poles for select to anon, authenticated using (true);
create policy "write" on poles for all to authenticated using (true) with check (true);
drop policy if exists "open" on draws;
create policy "read" on draws for select to anon, authenticated using (true);
create policy "write" on draws for all to authenticated using (true) with check (true);
revoke execute on function public.log_pole_change() from anon, authenticated, public;

-- Длина СИП по пролётам между опорами
create table if not exists spans (
  uid text primary key,   -- пара опор uidA|uidB
  id text,                -- подпись пролёта
  len numeric,            -- длина СИП, м
  sd date,                -- дата протяжки
  note text,
  ed text
);
alter table spans enable row level security;
create policy "read" on spans for select to anon, authenticated using (true);
create policy "write" on spans for all to authenticated using (true) with check (true);
create trigger spans_history after insert or update or delete on spans
for each row execute function log_pole_change();

-- Трансформаторные подстанции: положение значка и работы (бронекабель, шкаф управления)
create table if not exists tps (
  uid text primary key, id text, lat double precision, lon double precision,
  w jsonb default '{}'::jsonb, cab numeric, note text, ed text
);
alter table tps enable row level security;
create policy "read" on tps for select to anon, authenticated using (true);
create policy "write" on tps for all to authenticated using (true) with check (true);
create trigger tps_history after insert or update or delete on tps
for each row execute function log_pole_change();

-- Высота опоры, м (8 или 9)
alter table poles add column if not exists h int default 8;

-- Замечания технадзора (zamechaniya.html): статус устранения по номеру замечания
create table if not exists public.tn_remarks(
 n int primary key,
 st text not null default 'open' check (st in ('open','work','done')),
 note text, dt date, ed text,
 updated_at timestamptz not null default now());
alter table public.tn_remarks enable row level security;
create policy tn_read on public.tn_remarks for select to anon, authenticated using (true);
create policy tn_ins on public.tn_remarks for insert to authenticated with check (true);
create policy tn_upd on public.tn_remarks for update to authenticated using (true) with check (true);

-- Фото до/после по замечаниям технадзора: bucket tn-photos (public read) + таблица tn_photos
-- insert into storage.buckets(id,name,public,file_size_limit,allowed_mime_types) values('tn-photos','tn-photos',true,8388608,array['image/jpeg','image/png','image/webp']);
-- policies on storage.objects for authenticated: insert/select/delete where bucket_id='tn-photos'
create table if not exists public.tn_photos(id uuid primary key default gen_random_uuid(), n int not null,
 kind text not null check (kind in ('before','after')), path text not null, ed text, created_at timestamptz not null default now());

-- Фото до/после по работам опоры (сейчас: подрезка крон, k=9): bucket pole-photos (public read) + таблица pole_photos
create table if not exists public.pole_photos(id uuid primary key default gen_random_uuid(), uid text not null, k int not null,
 kind text not null check (kind in ('before','after')), path text not null, ed text, created_at timestamptz not null default now());

-- Угол двухрожкового кронштейна: 90 или 180 градусов (null — не указан); pole_patch дополнен полем ka
alter table public.poles add column if not exists ka int check (ka in (90,180));

-- Ручная правка линий (пролётов) между опорами: uid = 'uidA|uidB' (по алфавиту)
-- op: del — линия удалена, add — добавлена вручную, path — изменён путь (pts: [[lat,lon],...] точки изгиба)
create table if not exists public.line_edits(uid text primary key, op text not null check (op in ('del','add','path')), pts jsonb, ed text, updated_at timestamptz not null default now());

-- Опора ввода КЛ от ТП (анкерная с инспекционным люком под бронекабель).
-- Линия бронекабеля рисуется от значка ТП к такой опоре; изгибы пути хранятся в line_edits с uid 'p…|tp:<ТП>'.
alter table public.poles add column if not exists vk boolean not null default false;
-- pole_patch: добавлена строка  vk = case when s ? 'vk' then coalesce((s->>'vk')::boolean,false) else vk end

-- Исключённая из контракта опора, по которой всё равно тянем СИП (опора существует).
alter table public.poles add column if not exists sx boolean not null default false;
-- pole_patch: добавлена строка  sx = case when s ? 'sx' then coalesce((s->>'sx')::boolean,false) else sx end
