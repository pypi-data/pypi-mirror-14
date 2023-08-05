.. -*- coding: utf-8 -*-
.. :Project:   hurm -- Definition of table activitypayloads
.. :Created:   sab 27 feb 2016 15:48:37 CET
.. :Author:    Lele Gaifax <lele@metapensiero.it>
.. :License:   GNU General Public License version 3 or later
.. :Copyright: © 2016 Lele Gaifax
..

.. _activitypayloads:

=========================
 Activity payloads table
=========================

This table contains the description of the values, associated to a particular activity, that
must be collected on each duty related to that particular activity.

.. patchdb:script:: activitypayloads table
   :mimetype: text/x-postgresql
   :depends: domains@2

   create table activitypayloads (
     idactivitypayload integer_t not null,
     idactivity integer_t not null,
     description description_t not null,
     note text_t,
     unitcost money_t,

     constraint pk_activitypayloads primary key (idactivitypayload),
     constraint uk_activitypayloads unique (description, idactivitypayload)
   )

.. patchdb:script:: grant activitypayloads table permissions
   :mimetype: text/x-postgresql
   :depends: activitypayloads table

   grant select, insert, delete, update on activitypayloads to public

Record initialization
=====================

When a new record is created, if its primary key isn't already set a new value is computed
using a generator.

.. patchdb:script:: idactivitypayload generator
   :mimetype: text/x-postgresql

   create sequence gen_idactivitypayload

.. patchdb:script:: grant idactivitypayload generator permissions
   :mimetype: text/x-postgresql
   :depends: idactivitypayload generator

   grant usage on gen_idactivitypayload to public

.. patchdb:script:: initialize activitypayload record function
   :mimetype: text/x-postgresql
   :depends: activitypayloads table, idactivitypayload generator

   create or replace function init_activitypayload_record()
   returns trigger as $$
   begin
     if new.idactivitypayload is null or new.idactivitypayload = 0 then
       new.idactivitypayload := nextval('gen_idactivitypayload');
     end if;
     return new;
   end;
   $$ language plpgsql;

.. patchdb:script:: initialize activitypayload record trigger
   :mimetype: text/x-postgresql
   :depends: activitypayloads table, initialize activitypayload record function

   create trigger trg_ins_activities
     before insert
     on activitypayloads
     for each row execute procedure init_activitypayload_record();

Foreign keys
============

A single activitypayload is related to a particular activity.

.. patchdb:script:: fk activitypayloads->activities
   :mimetype: text/x-postgresql
   :depends: personactivities table, activities table

   alter table activitypayloads
     add constraint fk_activitypayloads_idactivity
         foreign key (idactivity) references activities (idactivity)
                                  on delete cascade
