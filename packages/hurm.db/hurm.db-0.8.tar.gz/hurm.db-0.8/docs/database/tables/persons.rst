.. -*- coding: utf-8 -*-
.. :Project:   hurm -- Definition of table persons
.. :Created:   mar 12 gen 2016 12:29:31 CET
.. :Author:    Lele Gaifax <lele@metapensiero.it>
.. :License:   GNU General Public License version 3 or later
.. :Copyright: © 2016 Lele Gaifax
..

.. _persons:

===============
 Persons table
===============

A ``person`` is... well, the obvious thing!

.. patchdb:script:: persons table
   :mimetype: text/x-postgresql
   :depends: domains

   create table persons (
     idperson integer_t not null,
     firstname name_t not null,
     lastname name_t not null,
     role description_t,
     birthdate date_t,
     phone phone_t,
     mobile phone_t,
     email email_t,
     password password_t,
     note text_t,

     constraint pk_persons primary key (idperson),
     constraint uk_persons unique (email)
   )

.. patchdb:script:: grant persons table permissions
   :mimetype: text/x-postgresql
   :depends: persons table

   grant select, insert, delete, update on persons to public

Record initialization
=====================

When a new record is created, if its primary key isn't already set a new value is computed
using a generator.

.. patchdb:script:: idperson generator
   :mimetype: text/x-postgresql

   create sequence gen_idperson

.. patchdb:script:: grant idperson generator permissions
   :mimetype: text/x-postgresql
   :depends: idperson generator

   grant usage on gen_idperson to public

.. patchdb:script:: initialize person record function
   :mimetype: text/x-postgresql
   :depends: persons table, idperson generator

   create or replace function init_person_record()
   returns trigger as $$
   begin
     if new.idperson is null or new.idperson = 0 then
       new.idperson := nextval('gen_idperson');
     end if;
     return new;
   end;
   $$ language plpgsql;

.. patchdb:script:: initialize persons record trigger
   :mimetype: text/x-postgresql
   :depends: persons table, initialize person record function

   create trigger trg_ins_persons
     before insert
     on persons
     for each row execute procedure init_person_record();

Timeline
========

..
   .. patchdb:script:: person timeline type
      :mimetype: text/x-postgresql
      :depends: domains

      create type person_timeline_t as (
        date date_t,
        starttime time_t,
        endtime time_t,
        idtask integer_t
      )

   .. patchdb:script:: person events function
      :mimetype: text/x-postgresql
      :depends: persons table
      :file: person_events.sql

   .. patchdb:script:: task timeline function
      :mimetype: text/x-postgresql
      :depends: person timeline type
      :file: person_timeline.sql
