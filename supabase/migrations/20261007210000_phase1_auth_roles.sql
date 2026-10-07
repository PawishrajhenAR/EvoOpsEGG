-- Phase 1: profiles, roles, user_roles, RLS, signup trigger
-- Single-org EvoOps identity foundation

create extension if not exists "pgcrypto";

-- ---------------------------------------------------------------------------
-- Tables
-- ---------------------------------------------------------------------------

create table if not exists public.roles (
  id uuid primary key default gen_random_uuid(),
  key text not null unique,
  name text not null,
  description text not null default '',
  created_at timestamptz not null default now()
);

create table if not exists public.profiles (
  id uuid primary key references auth.users (id) on delete cascade,
  email text not null,
  display_name text not null default '',
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create table if not exists public.user_roles (
  user_id uuid not null references public.profiles (id) on delete cascade,
  role_id uuid not null references public.roles (id) on delete cascade,
  granted_at timestamptz not null default now(),
  granted_by uuid references public.profiles (id) on delete set null,
  primary key (user_id, role_id)
);

create index if not exists user_roles_role_id_idx on public.user_roles (role_id);
create index if not exists profiles_email_idx on public.profiles (email);

-- ---------------------------------------------------------------------------
-- Seed roles
-- ---------------------------------------------------------------------------

insert into public.roles (key, name, description)
values
  ('operator', 'Operator', 'Runs tasks, submits feedback'),
  ('approver', 'Approver', 'Approves agent version promotions'),
  ('admin', 'Admin', 'Manages users, roles, and system settings')
on conflict (key) do nothing;

-- ---------------------------------------------------------------------------
-- Helpers (security definer)
-- ---------------------------------------------------------------------------

create or replace function public.current_user_id()
returns uuid
language sql
stable
as $$
  select auth.uid();
$$;

create or replace function public.has_role(role_key text)
returns boolean
language sql
stable
security definer
set search_path = public
as $$
  select exists (
    select 1
    from public.user_roles ur
    join public.roles r on r.id = ur.role_id
    where ur.user_id = auth.uid()
      and r.key = role_key
  );
$$;

create or replace function public.is_admin()
returns boolean
language sql
stable
security definer
set search_path = public
as $$
  select public.has_role('admin');
$$;

create or replace function public.set_updated_at()
returns trigger
language plpgsql
as $$
begin
  new.updated_at = now();
  return new;
end;
$$;

drop trigger if exists profiles_set_updated_at on public.profiles;
create trigger profiles_set_updated_at
before update on public.profiles
for each row execute function public.set_updated_at();

-- Auto-create profile on signup
create or replace function public.handle_new_user()
returns trigger
language plpgsql
security definer
set search_path = public
as $$
begin
  insert into public.profiles (id, email, display_name)
  values (
    new.id,
    coalesce(new.email, ''),
    coalesce(new.raw_user_meta_data->>'display_name', split_part(coalesce(new.email, 'user'), '@', 1))
  )
  on conflict (id) do update
    set email = excluded.email,
        updated_at = now();
  return new;
end;
$$;

drop trigger if exists on_auth_user_created on auth.users;
create trigger on_auth_user_created
after insert on auth.users
for each row execute function public.handle_new_user();

-- Bootstrap: if no admin exists, first profile can claim admin once (via RPC)
create or replace function public.claim_bootstrap_admin()
returns boolean
language plpgsql
security definer
set search_path = public
as $$
declare
  admin_role_id uuid;
  admin_count int;
begin
  if auth.uid() is null then
    raise exception 'not authenticated';
  end if;

  select count(*) into admin_count
  from public.user_roles ur
  join public.roles r on r.id = ur.role_id
  where r.key = 'admin';

  if admin_count > 0 then
    return false;
  end if;

  select id into admin_role_id from public.roles where key = 'admin';

  insert into public.user_roles (user_id, role_id, granted_by)
  values (auth.uid(), admin_role_id, auth.uid())
  on conflict do nothing;

  return true;
end;
$$;

create or replace function public.grant_role(target_user_id uuid, role_key text)
returns void
language plpgsql
security definer
set search_path = public
as $$
declare
  rid uuid;
begin
  if not public.is_admin() then
    raise exception 'admin role required';
  end if;

  select id into rid from public.roles where key = role_key;
  if rid is null then
    raise exception 'unknown role: %', role_key;
  end if;

  insert into public.user_roles (user_id, role_id, granted_by)
  values (target_user_id, rid, auth.uid())
  on conflict do nothing;
end;
$$;

create or replace function public.revoke_role(target_user_id uuid, role_key text)
returns void
language plpgsql
security definer
set search_path = public
as $$
begin
  if not public.is_admin() then
    raise exception 'admin role required';
  end if;

  delete from public.user_roles ur
  using public.roles r
  where ur.role_id = r.id
    and ur.user_id = target_user_id
    and r.key = role_key;
end;
$$;

-- ---------------------------------------------------------------------------
-- RLS
-- ---------------------------------------------------------------------------

alter table public.profiles enable row level security;
alter table public.roles enable row level security;
alter table public.user_roles enable row level security;

-- profiles
drop policy if exists profiles_select_self_or_admin on public.profiles;
create policy profiles_select_self_or_admin
  on public.profiles for select
  to authenticated
  using (id = auth.uid() or public.is_admin());

drop policy if exists profiles_update_self on public.profiles;
create policy profiles_update_self
  on public.profiles for update
  to authenticated
  using (id = auth.uid() or public.is_admin())
  with check (id = auth.uid() or public.is_admin());

-- roles: readable by authenticated; no direct writes (seed + service role)
drop policy if exists roles_select_authenticated on public.roles;
create policy roles_select_authenticated
  on public.roles for select
  to authenticated
  using (true);

-- user_roles
drop policy if exists user_roles_select_self_or_admin on public.user_roles;
create policy user_roles_select_self_or_admin
  on public.user_roles for select
  to authenticated
  using (user_id = auth.uid() or public.is_admin());

-- Mutations go through grant_role / revoke_role RPCs (security definer)
revoke all on function public.grant_role(uuid, text) from public;
revoke all on function public.revoke_role(uuid, text) from public;
revoke all on function public.claim_bootstrap_admin() from public;
grant execute on function public.grant_role(uuid, text) to authenticated;
grant execute on function public.revoke_role(uuid, text) to authenticated;
grant execute on function public.claim_bootstrap_admin() to authenticated;
grant execute on function public.has_role(text) to authenticated;
grant execute on function public.is_admin() to authenticated;

grant select on public.roles to authenticated;
grant select, update on public.profiles to authenticated;
grant select on public.user_roles to authenticated;
