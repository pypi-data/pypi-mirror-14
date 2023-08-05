# -*- coding: utf-8 -*-
# :Project:   hurm -- Data domains
# :Created:   lun 14 dic 2015 16:00:45 CET
# :Author:    Lele Gaifax <lele@metapensiero.it>
# :License:   GNU General Public License version 3 or later
# :Copyright: © 2015, 2016 Lele Gaifax
#

from sqlalchemy import (
    Boolean,
    CHAR,
    Date,
    Integer,
    Numeric,
    Time,
    Unicode,
    UnicodeText,
    VARCHAR,
    )
from sqlalchemy.types import TypeDecorator

from ..utils import normalize


class Description(TypeDecorator):
    impl = Unicode

    def process_bind_param(self, value, dialect):
        return normalize(value)


class Name(TypeDecorator):
    impl = Unicode

    def process_bind_param(self, value, dialect):
        return normalize(value, True)


boolean_t = Boolean()
"A boolean flag"

country_t = CHAR(2)
"A country ISO 3166 alpha2 code"

date_t = Date()
"A date"

description_t = Description(100)
"A long description"

email_t = VARCHAR(50)
"An email address"

integer_t = Integer()
"An integer value"

latlng_t = Numeric(10,6)
"A latitude or a longitude"

money_t = Numeric(10,4)
"A money value in some currency"

name_t = Name(50)
"A fifty characters long name"

password_t = VARCHAR(60)
"A password hash"

phone_t = VARCHAR(20)
"A phone number"

province_t = VARCHAR(6)
"A province ISO 3166-2 code"

shortcode_t = VARCHAR(10)
"A short code"

text_t = UnicodeText()
"An arbitrarily long description."

time_t = Time()
"A time of the day"
