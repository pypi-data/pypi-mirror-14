.. -*- coding: utf-8 -*-
.. :Project:   hurm -- Definition of table editions
.. :Created:   mar 12 gen 2016 12:31:49 CET
.. :Author:    Lele Gaifax <lele@metapensiero.it>
.. :License:   GNU General Public License version 3 or later
.. :Copyright: © 2016 Lele Gaifax
..

.. _editions:

================
 Editions table
================

An ``edition`` is the *top level* information, carrying a description and the period of
activity of a particular edition of the festival.

.. patchdb:script:: editions table
   :mimetype: text/x-postgresql
   :depends: domains

   create table editions (
     idedition integer_t not null,
     description description_t not null,
     startdate date_t not null,
     enddate date_t not null,
     note text,

     constraint pk_editions primary key (idedition),
     constraint uk_editions unique (description),
     constraint edition_valid_period check (startdate < enddate)
   )

.. patchdb:script:: grant editions table permissions
   :mimetype: text/x-postgresql
   :depends: editions table

   grant select, insert, delete, update on editions to public

Record initialization
=====================

When a new record is created, if its primary key isn't already set a new value is computed
using a generator.

.. patchdb:script:: idedition generator
   :mimetype: text/x-postgresql

   create sequence gen_idedition

.. patchdb:script:: grant idedition generator permissions
   :mimetype: text/x-postgresql
   :depends: idedition generator

   grant usage on gen_idedition to public

.. patchdb:script:: initialize edition record function
   :mimetype: text/x-postgresql
   :depends: editions table, idedition generator

   create or replace function init_edition_record()
   returns trigger as $$
   begin
     if new.idedition is null or new.idedition = 0 then
       new.idedition := nextval('gen_idedition');
     end if;
     return new;
   end;
   $$ language plpgsql;

.. patchdb:script:: initialize edition record trigger
   :mimetype: text/x-postgresql
   :depends: editions table, initialize edition record function

   create trigger trg_ins_editions
     before insert
     on editions
     for each row execute procedure init_edition_record();

Validity checks
===============

When an edition gets modified:

* it's period cannot become narrower than the existing :ref:`availabilities <availabilities>`
  or :ref:`tasks <tasks>`

.. patchdb:script:: check edition validity function
   :mimetype: text/x-postgresql
   :depends: editions table, availabilities table, tasks table
   :file: check_edition_validity.sql

.. patchdb:script:: check edition validity trigger
   :mimetype: text/x-postgresql
   :depends: check edition validity function

   create constraint trigger trg_check_edition_validity
     after update
     on editions
     for each row execute procedure check_edition_validity();
