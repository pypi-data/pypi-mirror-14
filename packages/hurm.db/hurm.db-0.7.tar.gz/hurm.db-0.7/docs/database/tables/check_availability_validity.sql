-- -*- sql-product: postgres; coding: utf-8 -*-
-- :Project:   hurm -- Function to check an availability record validity
-- :Created:   mar 19 gen 2016 13:15:37 CET
-- :Author:    Lele Gaifax <lele@metapensiero.it>
-- :License:   GNU General Public License version 3 or later
-- :Copyright: © 2016 Lele Gaifax
--

create or replace function check_availability_validity()
returns trigger as $$

declare
  v_startdate date_t;
  v_enddate date_t;

begin
  if tg_op <> 'DELETE'
  then
    select startdate, enddate
    into v_startdate, v_enddate
    from editions e
    where e.idedition = new.idedition;

    if not new.date between v_startdate and v_enddate
    then
      raise exception 'availability date outside allowed period';
    end if;

    if exists (select *
               from availabilities a
               where (new.idavailability is null or a.idavailability <> new.idavailability)
                 and a.date = new.date
                 and a.idperson = new.idperson
                 and (coalesce(new.starttime, '00:00'), coalesce(new.endtime, '24:00'))
                     overlaps
                     (coalesce(a.starttime, '00:00'), coalesce(a.endtime, '24:00')))
    then
      raise exception 'overlapped availability';
    end if;
  else
    if exists (select *
               from duties d join tasks t on t.idtask = d.idtask
                 where t.idedition = old.idedition
                   and t.date = old.date
                   and d.idperson = old.idperson
                   and d.starttime >= coalesce(old.starttime, '00:00')
                   and d.endtime <= coalesce(old.endtime, '24:00'))
    then
      raise exception 'duties outside person availability';
    end if;
  end if;

  if tg_op = 'UPDATE'
     and
     exists (select *
             from duties d join tasks t on t.idtask = d.idtask
             where t.idedition = new.idedition
               and t.date = new.date
               and not exists (select *
                               from availabilities a
                               where a.idedition = t.idedition
                                 and a.idperson = d.idperson
                                 and a.date = t.date
                                 and d.starttime >= coalesce(a.starttime, '00:00')
                                 and d.endtime <= coalesce(a.endtime, '24:00')))
  then
    raise exception 'duties outside person availability';
  end if;

  return null;
end;

$$ language plpgsql;
