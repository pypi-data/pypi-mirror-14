# -*- coding: utf-8 -*-
# :Project:   hurm -- SQLAlchemy declaration of table activities
# :Created:   mer 23 dic 2015 10:44:39 CET
# :Author:    Lele Gaifax <lele@metapensiero.it>
# :License:   GNU General Public License version 3 or later
# :Copyright: © 2015, 2016 Lele Gaifax
#

import sqlalchemy as sa

from .. import metadata, translatable_string as _
from . import domains


activities = sa.Table(
    'activities', metadata,

    sa.Column(
        'idactivity', domains.integer_t, sa.Sequence('gen_idactivity', optional=True),
        nullable=False,
        primary_key=True,
        info={'label': _("Activity ID"),
              'hint': _("Unique ID of the activity")}),

    sa.Column(
        'description', domains.description_t,
        nullable=False,
        unique=True,
        info={'label': _("Activity"),
              'hint': _("Description of the activity")}),

    sa.Column(
        'allowoverlappedduties', domains.boolean_t,
        nullable=False,
        default=False,
        info={'label': _('Duties overlap'),
              'hint': _('Whether overlapped duties related to the activity are allowed')}
    ),
    sa.Column(
        'note', domains.text_t,
        info={'label': _("Note"),
              'hint': _("Note")}),
)
