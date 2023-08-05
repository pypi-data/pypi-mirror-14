# -*- coding: utf-8 -*-
# :Project:   hurm -- SQLAlchemy declaration of table availabilities
# :Created:   mer 23 dic 2015 11:13:05 CET
# :Author:    Lele Gaifax <lele@metapensiero.it>
# :License:   GNU General Public License version 3 or later
# :Copyright: © 2015, 2016 Lele Gaifax
#

import sqlalchemy as sa

from .. import metadata, translatable_string as _
from . import domains


availabilities = sa.Table(
    'availabilities', metadata,

    sa.Column(
        'idavailability', domains.integer_t, sa.Sequence('gen_idavailability', optional=True),
        nullable=False,
        primary_key=True,
        info={'label': _("Availability ID"),
              'hint': _("Unique ID of the availability")}),

    sa.Column(
        'idedition', domains.integer_t, sa.ForeignKey('editions.idedition'),
        nullable=False,
        info={'label': _("Edition ID"),
              'hint': _("ID of the edition")}),

    sa.Column(
        'idperson', domains.integer_t, sa.ForeignKey('persons.idperson'),
        nullable=False,
        info={'label': _("Person ID"),
              'hint': _("ID of the related person")}),

    sa.Column(
        'date', domains.date_t,
        nullable=False,
        info={'label': _("Date"),
              'hint': _("Reference date")}),

    sa.Column(
        'starttime', domains.time_t,
        info={'label': _("Start"),
              'hint': _("Starting time of the availability,"
                        " empty to mean from start of the day")}),

    sa.Column(
        'endtime', domains.time_t,
        info={'label': _("End"),
              'hint': _("Ending time of the availability,"
                        " empty to mean till the end of the day")}),

    sa.Column(
        'note', domains.text_t,
        info={'label': _("Note"),
              'hint': _("Note")}),
)
