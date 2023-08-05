.. -*- coding: utf-8 -*-
.. :Project:   hurm -- Definition of table dutypayloads
.. :Created:   sab 27 feb 2016 16:23:09 CET
.. :Author:    Lele Gaifax <lele@metapensiero.it>
.. :License:   GNU General Public License version 3 or later
.. :Copyright: © 2016 Lele Gaifax
..

.. dutypayloads:

=====================
 Duty payloads table
=====================

This value contains the duty values, one for each :ref:`payload <activitypayloads>` associated
with the related activity.

.. patchdb:script:: dutypayloads table
   :mimetype: text/x-postgresql
   :depends: domains

   create table dutypayloads (
     iddutypayload integer_t not null,
     idduty integer_t not null,
     idactivitypayload integer_t not null,
     value integer_t not null,
     note text_t,

     constraint pk_dutypayloads primary key (iddutypayload),
     constraint uk_dutypayloads unique (idduty, idactivitypayload)
   )

.. patchdb:script:: grant dutypayloads table permissions
   :mimetype: text/x-postgresql
   :depends: dutypayloads table

   grant select, insert, delete, update on dutypayloads to public

Record initialization
=====================

When a new record is created, if its primary key isn't already set a new value is computed
using a generator.

.. patchdb:script:: iddutypayload generator
   :mimetype: text/x-postgresql

   create sequence gen_iddutypayload

.. patchdb:script:: grant iddutypayload generator permissions
   :mimetype: text/x-postgresql
   :depends: iddutypayload generator

   grant usage on gen_iddutypayload to public

.. patchdb:script:: initialize dutypayload record function
   :mimetype: text/x-postgresql
   :depends: dutypayloads table, iddutypayload generator

   create or replace function init_dutypayload_record()
   returns trigger as $$
   begin
     if new.iddutypayload is null or new.iddutypayload = 0 then
       new.iddutypayload := nextval('gen_iddutypayload');
     end if;
     return new;
   end;
   $$ language plpgsql;

.. patchdb:script:: initialize dutypayload record trigger
   :mimetype: text/x-postgresql
   :depends: dutypayloads table, initialize dutypayload record function

   create trigger trg_ins_activities
     before insert
     on dutypayloads
     for each row execute procedure init_dutypayload_record();

Foreign keys
============

A single dutypayload is related to a particular duty and to a given activitypayload. When those
get deleted, the dutypayload will be automatically removed as well.

.. patchdb:script:: fk dutypayloads->duties
   :mimetype: text/x-postgresql
   :depends: dutypayloads table, duties table

   alter table dutypayloads
     add constraint fk_dutypayloads_idduty
         foreign key (idduty) references duties (idduty)
                              on delete cascade

.. patchdb:script:: fk dutypayloads->activitypayloads
   :mimetype: text/x-postgresql
   :depends: dutypayloads table, activitypayloads table

   alter table dutypayloads
     add constraint fk_dutypayloads_idactivitypayload
         foreign key (idactivitypayload) references activitypayloads (idactivitypayload)
                                         on delete cascade
