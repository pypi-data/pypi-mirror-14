.. -*- coding: utf-8 -*-
.. :Project:   hurm -- Definition of table locations
.. :Created:   mar 12 gen 2016 12:31:01 CET
.. :Author:    Lele Gaifax <lele@metapensiero.it>
.. :License:   GNU General Public License version 3 or later
.. :Copyright: © 2016 Lele Gaifax
..

.. _locations:

=================
 Locations table
=================

.. patchdb:script:: locations table
   :mimetype: text/x-postgresql
   :depends: domains

   create table locations (
     idlocation integer_t not null,
     description description_t not null,
     address description_t,
     city description_t,
     province province_t,
     zip shortcode_t,
     country country_t,
     latitude latlng_t,
     longitude latlng_t,
     phone phone_t,
     mobile phone_t,
     email email_t,
     note text_t,

     constraint pk_locations primary key (idlocation),
     constraint uk_locations unique (description)
   )

.. patchdb:script:: grant locations table permissions
   :mimetype: text/x-postgresql
   :depends: locations table

   grant select, insert, delete, update on locations to public

Record initialization
=====================

When a new record is created, if its primary key isn't already set a new value is computed
using a generator.

.. patchdb:script:: idlocation generator
   :mimetype: text/x-postgresql

   create sequence gen_idlocation

.. patchdb:script:: grant idlocation generator permissions
   :mimetype: text/x-postgresql
   :depends: idlocation generator

   grant usage on gen_idlocation to public

.. patchdb:script:: initialize location record function
   :mimetype: text/x-postgresql
   :depends: locations table, idlocation generator

   create or replace function init_location_record()
   returns trigger as $$
   begin
     if new.idlocation is null or new.idlocation = 0 then
       new.idlocation := nextval('gen_idlocation');
     end if;
     return new;
   end;
   $$ language plpgsql;

.. patchdb:script:: initialize location record trigger
   :mimetype: text/x-postgresql
   :depends: locations table, initialize location record function

   create trigger trg_ins_locations
     before insert
     on locations
     for each row execute procedure init_location_record();
