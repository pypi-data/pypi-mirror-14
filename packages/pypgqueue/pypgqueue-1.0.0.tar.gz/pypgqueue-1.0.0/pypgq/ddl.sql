create table {SCHEMA_NAME}.jobs (
  id bigserial not null primary key,
  name text not null,
  payload jsonb,
  priority int not null default 0,
  serialization_key_id bigint,
  created_at timestamptz not null default now(),
  started_at timestamptz,
  completed_at timestamptz,
  error_message text
);

create table {SCHEMA_NAME}.serialization_keys (
  id bigserial not null primary key,
  key text not null unique,
  active_job_id bigint references {SCHEMA_NAME}.jobs (id)
);

create index {SCHEMA_NAME}_job_serialization_key_id_idx
on jobs (serialization_key_id);

alter table {SCHEMA_NAME}.jobs
add constraint {SCHEMA_NAME}_jobs_serialization_key_id_fkey
foreign key (serialization_key_id)
references {SCHEMA_NAME}.serialization_keys (id);

create or replace function {SCHEMA_NAME}.tg_notify_job_status()
returns trigger as
$BODY$
begin
  perform pg_notify(
    'pypgq_job_changed',
    json_build_object('database', current_database(),
                      'schema', '{SCHEMA_NAME}',
                      'job_id', NEW.id,
                      'status', TG_ARGV[0])::text);
  return null;
end
$BODY$
language plpgsql;

create trigger {SCHEMA_NAME}_jobs_notify_on_insert_tg
after insert
on {SCHEMA_NAME}.jobs
for each row
execute procedure {SCHEMA_NAME}.tg_notify_job_status('created');

create trigger {SCHEMA_NAME}_jobs_notify_on_started_tg
after update
on {SCHEMA_NAME}.jobs
for each row
when (OLD.started_at is null and NEW.started_at is not null)
execute procedure {SCHEMA_NAME}.tg_notify_job_status('started');

create trigger {SCHEMA_NAME}_jobs_notify_on_completed_tg
after update
on {SCHEMA_NAME}.jobs
for each row
when (OLD.completed_at is null and NEW.completed_at is not null)
execute procedure {SCHEMA_NAME}.tg_notify_job_status('completed');
