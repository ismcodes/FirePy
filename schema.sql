drop table if exists emergencies;
create table emergencies (
  id integer primary key autoincrement,
  sequence text not null,
  begin date not null,
  end date
);