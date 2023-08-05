# -*- coding: utf-8 -*-
# :Project:   hurm -- Tests on Person entity
# :Created:   gio 03 mar 2016 11:08:57 CET
# :Author:    Lele Gaifax <lele@metapensiero.it>
# :License:   GNU General Public License version 3 or later
# :Copyright: © 2016 Lele Gaifax
#

from hurm.db.entities import Person


def test_repr(jane_tree):
    assert "Tree Jane" in repr(jane_tree)


def test_preferred_activities(session, subtitles, supervision):
    foobar = Person(firstname='Foo', lastname='Bar',
                    idactivities='%d,%d' % (subtitles.idactivity,
                                            supervision.idactivity))
    session.add(foobar)
    session.commit()

    assert len(foobar.activities) == 2

    foobar.update(dict(idactivities=''))
    session.commit()

    assert len(foobar.activities) == 0

    foobar.delete(session)
    session.commit()


def test_deletion_with_preferred_activities(session, subtitles, supervision):
    foobar = Person(firstname='Foo', lastname='Bar',
                    idactivities='%d,%d' % (subtitles.idactivity,
                                            supervision.idactivity))
    session.add(foobar)
    session.commit()

    assert len(foobar.activities) == 2

    foobar.delete(session)
    try:
        session.commit()
    finally:
        session.rollback()
