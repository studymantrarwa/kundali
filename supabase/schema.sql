create extension if not exists pgcrypto;

create type public.user_role as enum ('user','astrologer','admin');
create type public.astrologer_status as enum ('pending','approved','rejected','suspended');

create table if not exists public.profiles (
 id uuid primary key references auth.users(id) on delete cascade,
 email text unique not null,
 full_name text default '',
 role public.user_role not null default 'user',
 language text not null default 'en',
 created_at timestamptz default now()
);

create table if not exists public.astrologers (
 id uuid primary key references public.profiles(id) on delete cascade,
 bio text default '',
 languages text[] default '{}',
 price numeric(10,2) not null default 0 check(price>=0),
 discount_percent numeric(5,2) not null default 0 check(discount_percent between 0 and 100),
 is_online boolean not null default false,
 status public.astrologer_status not null default 'pending',
 created_at timestamptz default now(),
 updated_at timestamptz default now()
);

create table if not exists public.kundlis (
 id uuid primary key default gen_random_uuid(),
 user_id uuid not null references public.profiles(id) on delete cascade,
 title text default 'My Kundli',
 birth_date date not null,
 birth_time time not null,
 birth_place text not null,
 latitude double precision,
 longitude double precision,
 timezone text,
 calculation jsonb not null,
 created_at timestamptz default now()
);

create table if not exists public.chat_rooms (
 id uuid primary key default gen_random_uuid(),
 user_id uuid not null references public.profiles(id) on delete cascade,
 astrologer_id uuid not null references public.astrologers(id) on delete cascade,
 status text not null default 'active' check(status in ('active','closed')),
 created_at timestamptz default now(),
 closed_at timestamptz
);

create unique index if not exists one_active_chat on public.chat_rooms(user_id, astrologer_id) where status='active';

create table if not exists public.chat_messages (
 id uuid primary key default gen_random_uuid(),
 room_id uuid not null references public.chat_rooms(id) on delete cascade,
 sender_id uuid not null references public.profiles(id) on delete cascade,
 message text not null check(length(trim(message))>0),
 created_at timestamptz default now()
);

create table if not exists public.reviews (
 id uuid primary key default gen_random_uuid(),
 room_id uuid not null references public.chat_rooms(id) on delete cascade,
 user_id uuid not null references public.profiles(id) on delete cascade,
 astrologer_id uuid not null references public.astrologers(id) on delete cascade,
 rating integer not null check(rating between 1 and 5),
 review text default '',
 created_at timestamptz default now(),
 unique(room_id,user_id)
);

create or replace function public.handle_new_user()
returns trigger language plpgsql security definer set search_path=public as $$
begin
 insert into public.profiles(id,email,full_name) values(new.id,coalesce(new.email,''),coalesce(new.raw_user_meta_data->>'full_name',''));
 return new;
end; $$;

drop trigger if exists on_auth_user_created on auth.users;
create trigger on_auth_user_created after insert on auth.users
for each row execute procedure public.handle_new_user();

alter table public.profiles enable row level security;
alter table public.astrologers enable row level security;
alter table public.kundlis enable row level security;
alter table public.chat_rooms enable row level security;
alter table public.chat_messages enable row level security;
alter table public.reviews enable row level security;

create or replace function public.is_admin() returns boolean
language sql stable security definer set search_path=public
as $$ select exists(select 1 from public.profiles where id=auth.uid() and role='admin') $$;

create policy profiles_self on public.profiles for select using(id=auth.uid() or public.is_admin());
create policy profiles_update_self on public.profiles for update using(id=auth.uid() or public.is_admin());

create policy astrologer_public_approved on public.astrologers for select using(status='approved' or id=auth.uid() or public.is_admin());
create policy astrologer_self_update on public.astrologers for update using(id=auth.uid() or public.is_admin());
create policy astrologer_self_insert on public.astrologers for insert with check(id=auth.uid());
create policy astrologer_admin_all on public.astrologers for all using(public.is_admin()) with check(public.is_admin());

create policy kundli_owner on public.kundlis for select using(user_id=auth.uid() or public.is_admin() or exists(
 select 1 from public.chat_rooms r where r.user_id=kundlis.user_id and r.astrologer_id=auth.uid() and r.status='active'
));
create policy kundli_insert_owner on public.kundlis for insert with check(user_id=auth.uid());
create policy kundli_update_owner on public.kundlis for update using(user_id=auth.uid() or public.is_admin());
create policy kundli_delete_owner on public.kundlis for delete using(user_id=auth.uid() or public.is_admin());

create policy rooms_participants on public.chat_rooms for select using(user_id=auth.uid() or astrologer_id=auth.uid() or public.is_admin());
create policy rooms_user_insert on public.chat_rooms for insert with check(user_id=auth.uid());
create policy rooms_participant_update on public.chat_rooms for update using(user_id=auth.uid() or astrologer_id=auth.uid() or public.is_admin());

create policy messages_participants on public.chat_messages for select using(exists(
 select 1 from public.chat_rooms r where r.id=room_id and (r.user_id=auth.uid() or r.astrologer_id=auth.uid() or public.is_admin())
));
create policy messages_send on public.chat_messages for insert with check(sender_id=auth.uid() and exists(
 select 1 from public.chat_rooms r where r.id=room_id and r.status='active' and (r.user_id=auth.uid() or r.astrologer_id=auth.uid())
));

create policy reviews_owner on public.reviews for select using(user_id=auth.uid() or astrologer_id=auth.uid() or public.is_admin());
create policy reviews_insert on public.reviews for insert with check(user_id=auth.uid() and exists(
 select 1 from public.chat_rooms r where r.id=room_id and r.user_id=auth.uid() and r.astrologer_id=reviews.astrologer_id and r.status='closed'
));
create policy reviews_admin on public.reviews for all using(public.is_admin()) with check(public.is_admin());

-- Realtime publication. If Supabase reports these tables are already members, ignore that notice.
alter publication supabase_realtime add table public.chat_messages;
alter publication supabase_realtime add table public.chat_rooms;
