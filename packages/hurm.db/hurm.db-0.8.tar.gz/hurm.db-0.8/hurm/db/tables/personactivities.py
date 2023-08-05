# -*- coding: utf-8 -*-
# :Project:   hurm -- SQLAlchemy declaration of table personactivities
# :Created:   gio 18 feb 2016 12:31:09 CET
# :Author:    Lele Gaifax <lele@metapensiero.it>
# :License:   GNU General Public License version 3 or later
# :Copyright: © 2016 Lele Gaifax
#

import sqlalchemy as sa

from .. import metadata, translatable_string as _
from . import domains


personactivities = sa.Table(
    'personactivities', metadata,

    sa.Column(
        'idperson', domains.integer_t, sa.ForeignKey('persons.idperson'),
        nullable=False,
        primary_key=True,
        info={'label': _("Person ID"),
              'hint': _("ID of the related person")}),

    sa.Column(
        'idactivity', domains.integer_t, sa.ForeignKey('activities.idactivity'),
        nullable=False,
        primary_key=True,
        info={'label': _("Activity ID"),
              'hint': _("ID of the related activity")}),
)
