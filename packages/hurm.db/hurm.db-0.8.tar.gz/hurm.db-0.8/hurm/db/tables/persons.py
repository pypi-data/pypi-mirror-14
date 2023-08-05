# -*- coding: utf-8 -*-
# :Project:   hurm -- SQLAlchemy declaration of table persons
# :Created:   mar 22 dic 2015 18:45:01 CET
# :Author:    Lele Gaifax <lele@metapensiero.it>
# :License:   GNU General Public License version 3 or later
# :Copyright: © 2015, 2016 Lele Gaifax
#

import sqlalchemy as sa

from cryptacular.bcrypt import BCRYPTPasswordManager

from .. import metadata, translatable_string as _
from . import domains


password_manager = BCRYPTPasswordManager()


persons = sa.Table(
    'persons', metadata,

    sa.Column(
        'idperson', domains.integer_t, sa.Sequence('gen_idperson', optional=True),
        nullable=False,
        primary_key=True,
        info={'label': _("Person ID"),
              'hint': _("Unique ID of the person")}),

    sa.Column(
        'firstname', domains.name_t,
        nullable=False,
        info={'label': _("First name"),
              'hint': _("First name of the person")}),

    sa.Column(
        'lastname', domains.name_t,
        nullable=False,
        info={'label': _("Last name"),
              'hint': _("Last name of the person")}),

    sa.Column(
        'role', domains.description_t,
        info={'label': _("Role"),
              'hint': _("Role of the person")}),

    sa.Column(
        'birthdate', domains.date_t,
        info={'label': _("Birthdate"),
              'hint': _("Date of birth")}),

    sa.Column(
        'phone', domains.phone_t,
        info={'label': _("Phone"),
              'hint': _("Phone number of the person")}),

    sa.Column(
        'mobile', domains.phone_t,
        info={'label': _("Mobile"),
              'hint': _("Mobile number of the person")}),

    sa.Column(
        'email', domains.email_t,
        unique=True,
        info={'label': _("Email"),
              'hint': _("Email address of the person")}),

    sa.Column(
        'password', domains.password_t,
        info={'label': _("Password"),
              'hint': _("Hashed password")}),

    sa.Column(
        'note', domains.text_t,
        info={'label': _("Note"),
              'hint': _("Note")}),
)
