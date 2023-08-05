.. -*- coding: utf-8 -*-
.. :project:   hurm -- Definition of table duties
.. :created:   mar 12 gen 2016 12:34:14 cet
.. :author:    lele gaifax <lele@metapensiero.it>
.. :license:   gnu general public license version 3 or later
.. :copyright: copyright (c) 2016 lele gaifax
..

.. _duties:

==============
 Duties table
==============

A ``duty`` records the assignment of a particular *person* to a given *task*.

.. patchdb:script:: duties table
   :mimetype: text/x-postgresql
   :depends: domains

   create table duties (
     idduty integer_t not null,
     idperson integer_t not null,
     idtask integer_t not null,
     starttime time_t not null,
     endtime time_t not null,
     note text_t,

     constraint pk_duties primary key (idduty),
     constraint duty_valid_time_range check (starttime < endtime)
   )

.. patchdb:script:: grant duties table permissions
   :mimetype: text/x-postgresql
   :depends: duties table

   grant select, insert, delete, update on duties to public

Record initialization
=====================

When a new record is created, if its primary key isn't already set a new value is computed
using a generator.

.. patchdb:script:: idduty generator
   :mimetype: text/x-postgresql

   create sequence gen_idduty

.. patchdb:script:: grant idduty generator permissions
   :mimetype: text/x-postgresql
   :depends: idduty generator

   grant usage on gen_idduty to public

.. patchdb:script:: initialize duty record function
   :mimetype: text/x-postgresql
   :depends: duties table, idduty generator

   create or replace function init_duty_record()
   returns trigger as $$
   begin
     if new.idduty is null or new.idduty = 0
     then
       new.idduty := nextval('gen_idduty');
     end if;
     return new;
   end;
   $$ language plpgsql;

.. patchdb:script:: initialize duty record trigger
   :mimetype: text/x-postgresql
   :depends: duties table, initialize duty record function

   create trigger trg_ins_duties
     before insert
     on duties
     for each row execute procedure init_duty_record();

Foreign keys
============

A single duty is related to a particular person and to a specific task.

.. patchdb:script:: fk duties->persons
   :mimetype: text/x-postgresql
   :depends: duties table, persons table

   alter table duties
     add constraint fk_duties_idperson
         foreign key (idperson) references persons (idperson)

.. patchdb:script:: fk duties->tasks
   :mimetype: text/x-postgresql
   :depends: duties table, tasks table

   alter table duties
     add constraint fk_duties_idtask
         foreign key (idtask) references tasks (idtask)

Validity checks
===============

A duty:

* must fall within its :ref:`task <tasks>` time span
* must fall within related person's :ref:`availability <availabilities>`
* cannot overlaps other :ref:`duties` of the same person on the same date
  (except when the activity associated with the related task allows that)

.. patchdb:script:: check duty validity function
   :mimetype: text/x-postgresql
   :revision: 2
   :depends: domains@2, availabilities table, duties table, tasks table
   :file: check_duty_validity.sql

.. patchdb:script:: check duty validity trigger
   :mimetype: text/x-postgresql
   :depends: check duty validity function

   create constraint trigger trg_check_duty_validity
     after insert or update
     on duties
     for each row execute procedure check_duty_validity();
