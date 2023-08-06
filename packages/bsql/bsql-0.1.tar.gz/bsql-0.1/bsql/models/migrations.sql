-- the migrations table is usually the first migration

begin;
------------------------------------------------------------

create table migrations (
  id          varchar primary key,
  inserted    timestamptz(0) default current_timestamp,
  description text
);

---------------------------------------------------------------------------
commit;

