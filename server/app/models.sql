create table demo_table (
  id serial primary key,
  username varchar(40) not null,
  message text,
  timestamp timestamptz not null default current_timestamp
);


