# -*- coding: utf-8 -*-
# :Project:   hurm -- SQLAlchemy declaration of table activitypayloads
# :Created:   sab 27 feb 2016 16:40:06 CET
# :Author:    Lele Gaifax <lele@metapensiero.it>
# :License:   GNU General Public License version 3 or later
# :Copyright: © 2016 Lele Gaifax
#

import sqlalchemy as sa

from .. import metadata, translatable_string as _
from . import domains


activitypayloads = sa.Table(
    'activitypayloads', metadata,

    sa.Column(
        'idactivitypayload', domains.integer_t, sa.Sequence('gen_idactivitypayload',
                                                            optional=True),
        nullable=False,
        primary_key=True,
        info={'label': _("Activity payload ID"),
              'hint': _("Unique ID of the activity payload")}
    ),

    sa.Column(
        'idactivity', domains.integer_t, sa.ForeignKey('activities.idactivity'),
        nullable=False,
        info={'label': _("Activity ID"),
              'hint': _("ID of the related activity")}),

    sa.Column(
        'description', domains.description_t,
        nullable=False,
        info={'label': _("Value name"),
              'hint': _("The name of the particular payload value")},
    ),

    sa.Column(
        'note', domains.text_t,
        info={'label': _("Note"),
              'hint': _("The long description of the payload value")}),

    sa.Column(
        'unitcost', domains.money_t,
        info={'label': _("Unit cost"),
              'hint': _("Coefficient to transform the value in money")}),
)
