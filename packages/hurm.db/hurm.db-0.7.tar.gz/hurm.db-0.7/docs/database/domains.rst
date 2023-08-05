.. -*- coding: utf-8 -*-
.. :Project:   hurm
.. :Created:   mar 12 gen 2016 11:33:51 CET
.. :Author:    Lele Gaifax <lele@metapensiero.it>
.. :License:   GNU General Public License version 3 or later
.. :Copyright: © 2016 Lele Gaifax
..

==================
 Database domains
==================

.. patchdb:script:: domains
   :language: sql
   :mimetype: text/x-postgresql
   :revision: 2

   create domain boolean_t boolean
   ;;
   create domain country_t char(2)
   ;;
   create domain date_t date
   ;;
   create domain description_t varchar(100)
   ;;
   create domain email_t varchar(50)
   ;;
   create domain integer_t integer
   ;;
   create domain latlng_t numeric(10,6)
   ;;
   create domain money_t numeric(10,4)
   ;;
   create domain name_t varchar(50)
   ;;
   create domain password_t varchar(60)
   ;;
   create domain phone_t varchar(20)
   ;;
   create domain province_t varchar(6)
   ;;
   create domain shortcode_t varchar(10)
   ;;
   create domain text_t text
   ;;
   create domain time_t time
   ;;
   create domain timestamp_t timestamp

.. patchdb:script:: create boolean domain
   :language: sql
   :mimetype: text/x-postgresql
   :depends: domains@1
   :brings: domains@2

   create domain boolean_t boolean
   ;;
   create domain money_t numeric(10,4)
