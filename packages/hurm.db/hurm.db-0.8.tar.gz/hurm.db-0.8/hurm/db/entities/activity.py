# -*- coding: utf-8 -*-
# :Project:   hurm -- Activity class, mapped to table activities
# :Created:   sab 02 gen 2016 15:32:31 CET
# :Author:    Lele Gaifax <lele@metapensiero.it>
# :License:   GNU General Public License version 3 or later
# :Copyright: © 2016 Lele Gaifax
#

from . import AbstractBase


class Activity(AbstractBase):
    def __str__(self):
        return self.description
