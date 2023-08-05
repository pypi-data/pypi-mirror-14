# -*- coding: utf-8 -*-
# :Project:   hurm -- Person class, mapped to table persons
# :Created:   sab 02 gen 2016 15:34:36 CET
# :Author:    Lele Gaifax <lele@metapensiero.it>
# :License:   GNU General Public License version 3 or later
# :Copyright: © 2016 Lele Gaifax
#

from sqlalchemy.orm import object_session

from .. import translatable_string as N_
from . import AbstractBase, DBSession

from ..tables import password_manager


class Person(AbstractBase):
    def __init__(self, **kwargs):
        if 'password' in kwargs and kwargs['password']:
            kwargs['password'] = password_manager.encode(kwargs['password'])

        if 'idactivities' in kwargs:
            self._update_idactivities(kwargs.pop('idactivities'))

        super().__init__(**kwargs)

    def update(self, data, **kwargs):
        if 'password' in data and data['password']:
            data['password'] = password_manager.encode(data['password'])

        if 'idactivities' in data:
            oldidas, newidas = self._update_idactivities(data.pop('idactivities'))
        else:
            oldidas = None

        changes = super().update(data, **kwargs)

        if oldidas is not None:
            changes['idactivities'] = (oldidas, newidas)

        return changes

    def _update_idactivities(self, ids):
        from .activity import Activity

        if isinstance(ids, str):
            ids = list(map(int, ids.split(',')))

        oldidas = [activity.idactivity for activity in self.activities]

        to_be_removed = []
        for activity in self.activities:
            if ids and activity.idactivity in ids:
                ids.remove(activity.idactivity)
            else:
                to_be_removed.append(activity)

        for activity in to_be_removed:
            self.activities.remove(activity)

        if ids:
            session = object_session(self) or DBSession()
            for id in ids:
                self.activities.append(session.query(Activity).get(id))

        newidas = [activity.idactivity for activity in self.activities]

        if set(oldidas) == set(newidas):
            oldidas = newidas = None

        return oldidas, newidas

    @property
    def fullname(self):
        # TRANSLATORS: this is the full name of a person
        return N_('$firstname $lastname',
                  mapping=dict(firstname=self.firstname,
                               lastname=self.lastname))

    @property
    def abbreviated_fullname(self):
        # TRANSLATORS: this is the abbreviated full name of a person
        return N_('$firstname_initial. $lastname',
                  mapping=dict(firstname_initial=self.firstname[0],
                               lastname=self.lastname))
