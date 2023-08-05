# -*- coding: utf-8 -*-
# :Project:   hurm -- SQLAlchemy declaration of table dutypayloads
# :Created:   sab 27 feb 2016 16:46:21 CET
# :Author:    Lele Gaifax <lele@metapensiero.it>
# :License:   GNU General Public License version 3 or later
# :Copyright: © 2016 Lele Gaifax
#

import sqlalchemy as sa

from .. import metadata, translatable_string as _
from . import domains


dutypayloads = sa.Table(
    'dutypayloads', metadata,

    sa.Column(
        'iddutypayload', domains.integer_t, sa.Sequence('gen_iddutypayload', optional=True),
        nullable=False,
        primary_key=True,
        info={'label': _("Duty payload ID"),
              'hint': _("Unique ID of the duty payload")}),

    sa.Column(
        'idduty', domains.integer_t, sa.ForeignKey('duties.idduty'),
        nullable=False,
        info={'label': _("Duty ID"),
              'hint': _("ID of the duty")}),

    sa.Column(
        'idactivitypayload', domains.integer_t,
        sa.ForeignKey('activitypayloads.idactivitypayload'),
        nullable=False,
        info={'label': _("Activity payload ID"),
              'hint': _("ID of the activity payload")}),

    sa.Column(
        'value', domains.integer_t,
        nullable=False,
        info={'label': _("Value"),
              'hint': _("The value of the payload")}),

    sa.Column(
        'note', domains.text_t,
        info={'label': _("Note"),
              'hint': _("Note")}),
)
