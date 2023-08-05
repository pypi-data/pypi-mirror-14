.. -*- coding: utf-8 -*-
.. :Project:   hurm -- Definition of table tasks
.. :Created:   mar 12 gen 2016 12:33:00 CET
.. :Author:    Lele Gaifax <lele@metapensiero.it>
.. :License:   GNU General Public License version 3 or later
.. :Copyright: © 2016 Lele Gaifax
..

.. _tasks:

=============
 Tasks table
=============

A ``task`` is a particular *activity* that must be performed at a specific *location* on a
given date: it involves a certain number of *persons* for some time.

.. patchdb:script:: tasks table
   :mimetype: text/x-postgresql
   :depends: domains

   create table tasks (
     idtask integer_t not null,
     idedition integer_t not null,
     idlocation integer_t not null,
     date date_t not null,
     starttime time_t not null,
     endtime time_t,
     idactivity integer_t not null,
     npersons integer_t not null,
     note text_t,

     constraint pk_tasks primary key (idtask),
     constraint task_valid_time_range
       check (endtime is null
              or endtime is not null and starttime < endtime)
   )

.. patchdb:script:: grant tasks table permissions
   :mimetype: text/x-postgresql
   :depends: tasks table

   grant select, insert, delete, update on tasks to public

Record initialization
=====================

When a new record is created, if its primary key isn't already set a new value is computed
using a generator.

.. patchdb:script:: idtask generator
   :mimetype: text/x-postgresql

   create sequence gen_idtask

.. patchdb:script:: grant idtask generator permissions
   :mimetype: text/x-postgresql
   :depends: idtask generator

   grant usage on gen_idtask to public

.. patchdb:script:: initialize task record function
   :mimetype: text/x-postgresql
   :depends: tasks table, idtask generator

   create or replace function init_task_record()
   returns trigger as $$
   begin
     if new.idtask is null or new.idtask = 0 then
       new.idtask := nextval('gen_idtask');
     end if;
     return new;
   end;
   $$ language plpgsql;

.. patchdb:script:: initialize task record trigger
   :mimetype: text/x-postgresql
   :depends: tasks table, initialize task record function

   create trigger trg_ins_tasks
     before insert
     on tasks
     for each row execute procedure init_task_record();

Foreign keys
============

A single task is related to a particular edition for a specific activity at a given location.

.. patchdb:script:: fk tasks->editions
   :mimetype: text/x-postgresql
   :depends: tasks table, editions table

   alter table tasks
     add constraint fk_tasks_idedition
         foreign key (idedition) references editions (idedition)

.. patchdb:script:: fk tasks->activities
   :mimetype: text/x-postgresql
   :depends: tasks table, activities table

   alter table tasks
     add constraint fk_tasks_idactivity
         foreign key (idactivity) references activities (idactivity)

.. patchdb:script:: fk tasks->locations
   :mimetype: text/x-postgresql
   :depends: tasks table, locations table

   alter table tasks
     add constraint fk_tasks_idlocation
         foreign key (idlocation) references locations (idlocation)

Validity checks
===============

A task:

* must fall within the :ref:`edition <editions>`\ 's period
* cannot overlaps other tasks with the same :ref:`activity <activities>` at the same
  :ref:`location <locations>`
* cannot be modified leaving *uncovered* duties


.. patchdb:script:: check task validity function
   :mimetype: text/x-postgresql
   :depends: tasks table, editions table, duties table
   :file: check_task_validity.sql

.. patchdb:script:: check task date trigger
   :mimetype: text/x-postgresql
   :depends: check task validity function

   create constraint trigger trg_check_task_validity
     after insert or update
     on tasks
     for each row execute procedure check_task_validity();

Timeline
========


.. patchdb:script:: task timeline type
   :mimetype: text/x-postgresql
   :depends: domains

   create type task_timeline_t as (
     starttime time_t,
     endtime time_t,
     npersons integer_t
   )

.. patchdb:script:: task events function
   :mimetype: text/x-postgresql
   :depends: tasks table
   :file: task_events.sql

.. patchdb:script:: task timeline function
   :mimetype: text/x-postgresql
   :depends: task timeline type
   :file: task_timeline.sql
