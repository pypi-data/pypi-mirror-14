.. -*- coding: utf-8 -*-
.. :Project:   hurm -- Definition of table personactivities
.. :Created:   gio 18 feb 2016 12:17:48 CET
.. :Author:    Lele Gaifax <lele@metapensiero.it>
.. :License:   GNU General Public License version 3 or later
.. :Copyright: © 2016 Lele Gaifax
..

.. personactivities:

===================
 Person activities
===================

Any :ref:`person <persons>` may choose a set of preferred :ref:`activities <activities>`.

.. patchdb:script:: personactivities table
   :mimetype: text/x-postgresql
   :depends: domains

   create table personactivities (
     idperson integer_t not null,
     idactivity integer_t not null,

     constraint pk_personactivities primary key (idperson, idactivity)
   )

.. patchdb:script:: grant personactivities table permissions
   :mimetype: text/x-postgresql
   :depends: tasks table

   grant select, insert, delete, update on tasks to public

Foreign keys
============

A single personactivity is related to a particular person and to a specific activity.

.. patchdb:script:: fk personactivities->persons
   :mimetype: text/x-postgresql
   :depends: personactivities table, persons table
   :revision: 2

   alter table personactivities
     drop constraint if exists fk_personactivities_idperson
   ;;
   alter table personactivities
     add constraint fk_personactivities_idperson
         foreign key (idperson) references persons (idperson)

.. patchdb:script:: fk personactivities->activities
   :mimetype: text/x-postgresql
   :depends: personactivities table, activities table
   :revision: 2

   alter table personactivities
     drop constraint if exists fk_personactivities_idactivity
   ;;
   alter table personactivities
     add constraint fk_personactivities_idactivity
         foreign key (idactivity) references activities (idactivity)
