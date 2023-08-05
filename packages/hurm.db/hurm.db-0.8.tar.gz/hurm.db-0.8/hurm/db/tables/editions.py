# -*- coding: utf-8 -*-
# :Project:   hurm -- SQLAlchemy declaration of table editions
# :Created:   mar 22 dic 2015 16:05:12 CET
# :Author:    Lele Gaifax <lele@metapensiero.it>
# :License:   GNU General Public License version 3 or later
# :Copyright: © 2015, 2016 Lele Gaifax
#

import sqlalchemy as sa

from .. import metadata, translatable_string as _
from . import domains


editions = sa.Table(
    'editions', metadata,

    sa.Column(
        'idedition', domains.integer_t, sa.Sequence('gen_idedition', optional=True),
        nullable=False,
        primary_key=True,
        info={'label': _("Edition ID"),
              'hint': _("Unique ID of the edition")}),

    sa.Column(
        'description', domains.description_t,
        nullable=False,
        unique=True,
        info={'label': _("Edition"),
              'hint': _("Description of the edition")}),

    sa.Column(
        'startdate', domains.date_t,
        nullable=False,
        info={'label': _("Start"),
              'hint': _("Starting date")}),

    sa.Column(
        'enddate', domains.date_t,
        nullable=False,
        info={'label': _("End"),
              'hint': _("Ending date")}),

    sa.Column(
        'note', domains.text_t,
        info={'label': _("Note"),
              'hint': _("Note")}),
)
