-- Supabase Adapter α0.1
-- Experimental schema for preserving Landscape, Evidence, Context and Relations.
-- Apply this schema to a dedicated Supabase project for experiments.

create table if not exists landscapes (
    id uuid primary key default gen_random_uuid(),
    landscape_type text not null,
    title text,
    locale text not null default 'ja-JP',
    metadata jsonb not null default '{}'::jsonb,
    created_at timestamptz not null default now()
);

create table if not exists contexts (
    id uuid primary key default gen_random_uuid(),
    landscape_id uuid not null references landscapes(id) on delete cascade,
    context_type text not null,
    original_text text not null,
    locale text not null default 'ja-JP',
    source_ref text,
    metadata jsonb not null default '{}'::jsonb,
    created_at timestamptz not null default now()
);

create table if not exists evidences (
    id uuid primary key default gen_random_uuid(),
    landscape_id uuid not null references landscapes(id) on delete cascade,
    evidence_type text not null,
    operation_ref text,
    protocol_ref text,
    backend_ref text,
    payload jsonb not null default '{}'::jsonb,
    observed_at timestamptz not null default now(),
    immutable boolean not null default true
);

create table if not exists relations (
    id uuid primary key default gen_random_uuid(),
    landscape_id uuid not null references landscapes(id) on delete cascade,
    source_context_id uuid references contexts(id) on delete set null,
    target_context_id uuid references contexts(id) on delete set null,
    relation_type text not null,
    status text not null default 'candidate',
    basis text,
    evidence_id uuid references evidences(id) on delete set null,
    metadata jsonb not null default '{}'::jsonb,
    created_at timestamptz not null default now()
);

create index if not exists contexts_landscape_id_idx on contexts(landscape_id);
create index if not exists evidences_landscape_id_idx on evidences(landscape_id);
create index if not exists relations_landscape_id_idx on relations(landscape_id);
create index if not exists relations_source_context_id_idx on relations(source_context_id);
create index if not exists relations_target_context_id_idx on relations(target_context_id);

comment on table landscapes is 'Observable Landscape container; not an AI persona or model state.';
comment on table contexts is 'Original human/context material. Preserve source text.';
comment on table evidences is 'Backend/runtime observations. Treat as append-oriented evidence.';
comment on table relations is 'Observed or candidate connections; not conclusions about human intent.';
