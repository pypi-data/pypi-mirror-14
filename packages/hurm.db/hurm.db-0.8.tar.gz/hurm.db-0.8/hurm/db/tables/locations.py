# -*- coding: utf-8 -*-
# :Project:   hurm -- SQLAlchemy declaration of table locations
# :Created:   mar 22 dic 2015 18:17:59 CET
# :Author:    Lele Gaifax <lele@metapensiero.it>
# :License:   GNU General Public License version 3 or later
# :Copyright: © 2015, 2016 Lele Gaifax
#

import sqlalchemy as sa

from .. import metadata, translatable_string as _
from . import domains


locations = sa.Table(
    'locations', metadata,

    sa.Column(
        'idlocation', domains.integer_t, sa.Sequence('gen_idlocation', optional=True),
        nullable=False,
        primary_key=True,
        info={'label': _("Location ID"),
              'hint': _("Unique ID of the location")}),

    sa.Column(
        'description', domains.description_t,
        nullable=False,
        unique=True,
        info={'label': _("Location"),
              'hint': _("Description of the location")}),

    sa.Column(
        'address', domains.description_t,
        info=dict(
            label=_("Address"),
            hint=_("Street address"))),

    sa.Column(
        'city', domains.description_t,
        info=dict(
            label=_("City"),
            hint=_("City name"))),

    sa.Column(
        'province', domains.province_t,
        info=dict(
            label=_("Province code"),
            hint=_("Code of the province"))),

    sa.Column(
        'zip', domains.shortcode_t,
        info=dict(
            label=_("Zip code"),
            hint=_("Zip code of the city"))),

    sa.Column(
        'country', domains.country_t,
        info=dict(
            label=_("Country code"),
            hint=_("Code of the country"))),

    sa.Column(
        'latitude', domains.latlng_t,
        info={'label': _("Latitude"),
              'hint': _("Latitude of the location")}),

    sa.Column(
        'longitude', domains.latlng_t,
        info={'label': _("Longitude"),
              'hint': _("Longitude of the location")}),

    sa.Column(
        'phone', domains.phone_t,
        info={'label': _("Phone"),
              'hint': _("Phone number of the location")}),

    sa.Column(
        'mobile', domains.phone_t,
        info={'label': _("Mobile"),
              'hint': _("Mobile number of the location")}),

    sa.Column(
        'email', domains.email_t,
        info={'label': _("Email"),
              'hint': _("Email address of the location")}),

    sa.Column(
        'note', domains.text_t,
        info={'label': _("Note"),
              'hint': _("Note")}),
)
