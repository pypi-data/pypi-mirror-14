-- -*- sql-product: postgres; coding: utf-8 -*-
-- :Project:   hurm -- Task's timeline generator
-- :Created:   sab 16 gen 2016 20:21:03 CET
-- :Author:    Lele Gaifax <lele@metapensiero.it>
-- :License:   GNU General Public License version 3 or later
-- :Copyright: © 2016 Lele Gaifax
--

create or replace function task_timeline(p_idtask integer_t)
returns setof task_timeline_t as $$

declare
  v_date date_t;
  v_event time_t;
  v_time time_t;
  v_result task_timeline_t;

begin
  select date
  into v_date
  from tasks
  where idtask = p_idtask;

  v_time := null;
  for v_event in select distinct e.t
                 from task_events(p_idtask) as e(t)
                 order by t
  loop
    if v_time is not null
    then
      v_result.starttime := v_time;
      v_result.endtime := v_event;
      select count(d.idperson)
      into v_result.npersons
      from duties d
      where d.idtask = p_idtask
        and d.starttime <= v_time
        and d.endtime > v_time;
      return next v_result;
    end if;
    v_time := v_event;
  end loop;
end;

$$ language plpgsql stable
