# -*- coding: utf-8 -*-
# :Project:   hurm -- SQLAlchemy declaration of table tasks
# :Created:   mer 23 dic 2015 10:55:49 CET
# :Author:    Lele Gaifax <lele@metapensiero.it>
# :License:   GNU General Public License version 3 or later
# :Copyright: © 2015, 2016 Lele Gaifax
#

import sqlalchemy as sa

from .. import metadata, translatable_string as _
from . import domains


tasks = sa.Table(
    'tasks', metadata,

    sa.Column(
        'idtask', domains.integer_t, sa.Sequence('gen_idtask', optional=True),
        nullable=False,
        primary_key=True,
        info={'label': _("Task ID"),
              'hint': _("Unique ID of the task")}),

    sa.Column(
        'idedition', domains.integer_t, sa.ForeignKey('editions.idedition'),
        nullable=False,
        info={'label': _("Edition ID"),
              'hint': _("ID of the edition")}),

    sa.Column(
        'idlocation', domains.integer_t, sa.ForeignKey('locations.idlocation'),
        nullable=False,
        info={'label': _("Location ID"),
              'hint': _("ID of the involved location")}),

    sa.Column(
        'date', domains.date_t,
        nullable=False,
        info={'label': _("Date"),
              'hint': _("Reference date")}),

    sa.Column(
        'starttime', domains.time_t,
        nullable=False,
        info={'label': _("Start"),
              'hint': _("Starting time of the task")}),

    sa.Column(
        'endtime', domains.time_t,
        info={'label': _("End"),
              'hint': _("Ending time of the task, empty means till the end of the day")}),

    sa.Column(
        'idactivity', domains.integer_t, sa.ForeignKey('activities.idactivity'),
        nullable=False,
        info={'label': _("Activity ID"),
              'hint': _("ID of the related activity")}),

    sa.Column(
        'npersons', domains.integer_t,
        nullable=False,
        info={'label': _("Persons"),
              'hint': _("Number of required persons")}),

    sa.Column(
        'note', domains.text_t,
        info={'label': _("Note"),
              'hint': _("Note")}),
)
