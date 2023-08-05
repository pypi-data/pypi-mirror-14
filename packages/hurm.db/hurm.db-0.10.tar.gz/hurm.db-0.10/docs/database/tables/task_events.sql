-- -*- sql-product: postgres; coding: utf-8 -*-
-- :Project:   hurm -- Helper function to generate task's timeline
-- :Created:   sab 16 gen 2016 20:01:21 CET
-- :Author:    Lele Gaifax <lele@metapensiero.it>
-- :License:   GNU General Public License version 3 or later
-- :Copyright: © 2016 Lele Gaifax
--

create or replace function task_events(p_idtask integer_t)
returns setof time_t as $$

declare
  v_date date_t;
  v_starttime time_t;
  v_endtime time_t;

begin
  select starttime, coalesce(endtime, '24:00')
  into v_starttime, v_endtime
  from tasks
  where idtask = p_idtask;

  return next v_starttime;
  return next v_endtime;

  for v_starttime, v_endtime in select starttime, endtime
                                from duties
                                where idtask = p_idtask
  loop
    return next v_starttime;
    return next v_endtime;
  end loop;
end;

$$ language plpgsql stable
