.. -*- coding: utf-8 -*-
.. :Project:   hurm -- Definition of table availabilities
.. :Created:   mar 12 gen 2016 12:33:32 CET
.. :Author:    Lele Gaifax <lele@metapensiero.it>
.. :License:   GNU General Public License version 3 or later
.. :Copyright: © 2016 Lele Gaifax
..

.. _availabilities:

======================
 Availabilities table
======================

An ``availability`` specifies a *span* of time when a *person* is willing to cooperate, on a
particular date.  The time span can be either *well determined* (from example, “from 14:00 to
18:00”), or *open ended* (e.g. “not before 11:00”, or “not after 22:00”, or even “all the
day”).

.. patchdb:script:: availabilities table
   :mimetype: text/x-postgresql
   :depends: domains

   create table availabilities (
     idavailability integer_t not null,
     idedition integer_t not null,
     idperson integer_t not null,
     date date_t not null,
     starttime time_t,
     endtime time_t,
     note text_t,

     constraint pk_availabilities primary key (idavailability),
     constraint availability_valid_time_range
       check ((starttime is not null and endtime is not null and starttime < endtime)
              or (starttime is null or endtime is null))
   )

.. patchdb:script:: grant availabilities table permissions
   :mimetype: text/x-postgresql
   :depends: availabilities table

   grant select, insert, delete, update on availabilities to public

Record initialization
=====================

When a new record is created, if its primary key isn't already set a new value is computed
using a generator.

.. patchdb:script:: idavailability generator
   :mimetype: text/x-postgresql

   create sequence gen_idavailability

.. patchdb:script:: grant idavailability generator permissions
   :mimetype: text/x-postgresql
   :depends: idavailability generator

   grant usage on gen_idavailability to public

.. patchdb:script:: initialize availability record function
   :mimetype: text/x-postgresql
   :depends: availabilities table, idavailability generator

   create or replace function init_availability_record()
   returns trigger as $$
   begin
     if new.idavailability is null or new.idavailability = 0
     then
       new.idavailability := nextval('gen_idavailability');
     end if;
     return new;
   end;
   $$ language plpgsql;

.. patchdb:script:: initialize availability record trigger
   :mimetype: text/x-postgresql
   :depends: availabilities table, initialize availability record function

   create trigger trg_ins_availabilities
     before insert
     on availabilities
     for each row execute procedure init_availability_record();

Foreign keys
============

A single availability is related to a particular person and to a specific edition.

.. patchdb:script:: fk availabilities->editions
   :mimetype: text/x-postgresql
   :depends: availabilities table, editions table

   alter table availabilities
     add constraint fk_availabilities_idedition
         foreign key (idedition) references editions (idedition)

.. patchdb:script:: fk availabilities->persons
   :mimetype: text/x-postgresql
   :depends: availabilities table, persons table

   alter table availabilities
     add constraint fk_availabilities_idperson
         foreign key (idperson) references persons (idperson)

Validity checks
===============

An availability:

* must fall within the :ref:`edition <editions>`\ 's period
* cannot overlaps other :ref:`availabilities <availabilities>` of the same :ref:`person
  <persons>` on the same date
* cannot be modified or deleted leaving *uncovered* :ref:`duties <duties>`

.. patchdb:script:: check availability validity function
   :mimetype: text/x-postgresql
   :depends: availabilities table, editions table, duties table
   :file: check_availability_validity.sql

.. patchdb:script:: check availability validity trigger
   :mimetype: text/x-postgresql
   :depends: check availability validity function

   create constraint trigger trg_check_availability_validity
     after insert or update or delete
     on availabilities
     for each row execute procedure check_availability_validity();
