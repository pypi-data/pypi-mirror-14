.. -*- coding: utf-8 -*-
.. :Project:   hurm -- Definition of table activities
.. :Created:   mar 12 gen 2016 12:32:16 CET
.. :Author:    Lele Gaifax <lele@metapensiero.it>
.. :License:   GNU General Public License version 3 or later
.. :Copyright: © 2016 Lele Gaifax
..

.. _activities:

==================
 Activities table
==================

An ``activity`` is simply a label that describes a particular *task*.

.. patchdb:script:: activities table
   :mimetype: text/x-postgresql
   :revision: 3
   :depends: domains@2

   create table activities (
     idactivity integer_t not null,
     description description_t not null,
     allowoverlappedduties boolean_t not null default false,
     allowoverlappedtasks boolean_t not null default false,
     note text_t,

     constraint pk_activities primary key (idactivity),
     constraint uk_activities unique (description)
   )

.. patchdb:script:: add allowoverlappedduties to activities table
   :mimetype: text/x-postgresql
   :depends: activities table@1, domains@2
   :brings: activities table@2

   alter table activities
     add column allowoverlappedduties boolean_t not null default false

.. patchdb:script:: add allowoverlappedtasks to activities table
   :mimetype: text/x-postgresql
   :depends: activities table@2
   :brings: activities table@3

   alter table activities
     add column allowoverlappedtasks boolean_t not null default false

.. patchdb:script:: grant activities table permissions
   :mimetype: text/x-postgresql
   :depends: activities table

   grant select, insert, delete, update on activities to public

Record initialization
=====================

When a new record is created, if its primary key isn't already set a new value is computed
using a generator.

.. patchdb:script:: idactivity generator
   :mimetype: text/x-postgresql

   create sequence gen_idactivity

.. patchdb:script:: grant idactivity generator permissions
   :mimetype: text/x-postgresql
   :depends: idactivity generator

   grant usage on gen_idactivity to public

.. patchdb:script:: initialize activity record function
   :mimetype: text/x-postgresql
   :depends: activities table, idactivity generator

   create or replace function init_activity_record()
   returns trigger as $$
   begin
     if new.idactivity is null or new.idactivity = 0 then
       new.idactivity := nextval('gen_idactivity');
     end if;
     return new;
   end;
   $$ language plpgsql;

.. patchdb:script:: initialize activity record trigger
   :mimetype: text/x-postgresql
   :depends: activities table, initialize activity record function

   create trigger trg_ins_activities
     before insert
     on activities
     for each row execute procedure init_activity_record();
