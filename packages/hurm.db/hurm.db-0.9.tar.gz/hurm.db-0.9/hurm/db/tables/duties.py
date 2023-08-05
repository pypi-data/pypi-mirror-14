# -*- coding: utf-8 -*-
# :Project:   hurm -- SQLAlchemy declaration of table duties
# :Created:   mer 23 dic 2015 11:18:03 CET
# :Author:    Lele Gaifax <lele@metapensiero.it>
# :License:   GNU General Public License version 3 or later
# :Copyright: © 2015, 2016 Lele Gaifax
#

import sqlalchemy as sa

from .. import metadata, translatable_string as _
from . import domains


duties = sa.Table(
    'duties', metadata,

    sa.Column(
        'idduty', domains.integer_t, sa.Sequence('gen_idduty', optional=True),
        nullable=False,
        primary_key=True,
        info={'label': _("Duty ID"),
              'hint': _("Unique ID of the duty")}),

    sa.Column(
        'idperson', domains.integer_t, sa.ForeignKey('persons.idperson'),
        nullable=False,
        info={'label': _("Person ID"),
              'hint': _("ID of the related person")}),

    sa.Column(
        'idtask', domains.integer_t, sa.ForeignKey('tasks.idtask'),
        nullable=False,
        info={'label': _("Task ID"),
              'hint': _("ID of the related task")}),

    sa.Column(
        'starttime', domains.time_t,
        info={'label': _("Start"),
              'hint': _("Starting time of the duty")}),

    sa.Column(
        'endtime', domains.time_t,
        info={'label': _("End"),
              'hint': _("Ending time of the duty")}),

    sa.Column(
        'note', domains.text_t,
        info={'label': _("Note"),
              'hint': _("Note")}),
)
