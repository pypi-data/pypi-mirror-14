-- -*- sql-product: postgres; coding: utf-8 -*-
-- :Project:   hurm -- Function to check a task record validity
-- :Created:   mar 19 gen 2016 13:20:28 CET
-- :Author:    Lele Gaifax <lele@metapensiero.it>
-- :License:   GNU General Public License version 3 or later
-- :Copyright: © 2016 Lele Gaifax
--

create or replace function check_task_validity()
returns trigger as $$

declare
  v_startdate date_t;
  v_enddate date_t;
  v_allowoverlappedtasks boolean_t;

begin
  select startdate, enddate
  into v_startdate, v_enddate
  from editions e
  where e.idedition = new.idedition;

  if (not new.date between v_startdate and v_enddate) then
    raise exception 'task date outside allowed period';
  end if;

  select allowoverlappedtasks
  into v_allowoverlappedtasks
  from activities a
  where a.idactivity = new.idactivity;

  if not v_allowoverlappedtasks
     and exists (select *
                 from tasks t
                 where (new.idtask is null or t.idtask <> new.idtask)
                   and t.date = new.date
                   and t.idactivity = new.idactivity
                   and t.idlocation = new.idlocation
                   and (new.starttime, coalesce(new.endtime, '24:00'))
                       overlaps
                       (t.starttime, coalesce(t.endtime, '24:00')))
  then
    raise exception 'overlapped task';
  end if;

  if tg_op <> 'INSERT'
     and
     exists (select *
             from duties d
             where d.idtask = old.idtask
               and (d.starttime < coalesce(new.starttime, '00:00')
                    or
                    d.endtime > coalesce(new.endtime, '24:00')))
  then
    raise exception 'duties outside task time range';
  end if;

  return null;
end;
$$ language plpgsql;
