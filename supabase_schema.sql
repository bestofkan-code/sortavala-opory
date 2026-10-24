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
