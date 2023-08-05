-- -*- sql-product: postgres; coding: utf-8 -*-
-- :Project:   hurm -- Function to check an edition record validity
-- :Created:   sab 23 gen 2016 19:22:30 CET
-- :Author:    Lele Gaifax <lele@metapensiero.it>
-- :License:   GNU General Public License version 3 or later
-- :Copyright: © 2016 Lele Gaifax
--

create or replace function check_edition_validity()
returns trigger as $$

begin
  if exists (select *
             from availabilities a
             where a.idedition = new.idedition
               and a.date not between new.startdate and new.enddate)
  then
    raise exception 'availabilities outside edition period';
  end if;

  if exists (select *
             from tasks t
             where t.idedition = new.idedition
               and t.date not between new.startdate and new.enddate)
  then
    raise exception 'tasks outside edition period';
  end if;

  return null;
end;

$$ language plpgsql;
