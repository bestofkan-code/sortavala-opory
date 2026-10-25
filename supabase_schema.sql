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
