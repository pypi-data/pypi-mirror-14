-- -*- sql-product: postgres; coding: utf-8 -*-
-- :Project:   hurm -- Function to check a duty record validity
-- :Created:   sab 16 gen 2016 20:32:00 CET
-- :Author:    Lele Gaifax <lele@metapensiero.it>
-- :License:   GNU General Public License version 3 or later
-- :Copyright: © 2016 Lele Gaifax
--

create or replace function check_duty_validity()
returns trigger as $$

declare
  v_idedition integer_t;
  v_idactivity integer_t;
  v_date date_t;
  v_starttime time_t;
  v_endtime time_t;
  v_allowoverlappedduties boolean_t;

begin
  select idedition, date, idactivity, coalesce(starttime, '00:00'), coalesce(endtime, '24:00')
  into v_idedition, v_date, v_idactivity, v_starttime, v_endtime
  from tasks t
  where t.idtask = new.idtask;

  if new.starttime < v_starttime or new.starttime >= v_endtime
     or new.endtime < v_starttime or new.endtime > v_endtime
  then
    raise exception 'duty time outside task time';
  end if;

  if not exists (select *
                 from availabilities a
                 where a.idedition = v_idedition
                   and a.idperson = new.idperson
                   and a.date = v_date
                   and new.starttime >= coalesce(a.starttime, '00:00')
                   and new.starttime < coalesce(a.endtime, '24:00')
                   and new.endtime > coalesce(a.starttime, '00:00')
                   and new.endtime <= coalesce(a.endtime, '24:00'))
  then
    raise exception 'duty time outside person availability';
  end if;

  select allowoverlappedduties
  into v_allowoverlappedduties
  from activities a
  where a.idactivity = v_idactivity;

  if not v_allowoverlappedduties
     and exists (select *
                 from duties d join tasks t on d.idtask = t.idtask
                 where (new.idduty is null or d.idduty <> new.idduty)
                   and t.date = v_date
                   and d.idperson = new.idperson
                   and (new.starttime, new.endtime) overlaps (d.starttime, d.endtime))
  then
    raise exception 'overlapped duty';
  end if;

  return null;
end;

$$ language plpgsql;
