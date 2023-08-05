# -*- coding: utf-8 -*-
# :Project:   hurm -- PersonActivity class, mapped to table personactivities
# :Created:   gio 18 feb 2016 12:35:11 CET
# :Author:    Lele Gaifax <lele@metapensiero.it>
# :License:   GNU General Public License version 3 or later
# :Copyright: © 2016 Lele Gaifax
#

from . import AbstractBase


class PersonActivity(AbstractBase):
    def __str__(self):
        return '%s, %s' % (self.person, self.activity)
