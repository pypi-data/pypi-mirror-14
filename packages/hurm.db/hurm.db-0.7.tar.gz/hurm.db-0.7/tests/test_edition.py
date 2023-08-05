# -*- coding: utf-8 -*-
# :Project:   hurm
# :Created:   sab 23 gen 2016 19:30:39 CET
# :Author:    Lele Gaifax <lele@metapensiero.it>
# :License:   GNU General Public License version 3 or later
# :Copyright: © 2016 Lele Gaifax
#

from datetime import date

from sqlalchemy import exc as saexc


def test_edition_repr(session, edition_test):
    assert 'Edition ' in repr(edition_test)


def test_invalid_edition_period(session, edition_test):
    edition_test.startdate = date(1968, 3, 18)
    edition_test.enddate = date(1968, 3, 28)
    try:
        session.flush()
    except saexc.InternalError as e:
        assert 'availabilities outside edition period' in str(e)
    else:
        assert False, "Should raise an SQL error"
    finally:
        session.rollback()

    edition_test.enddate = date(2016, 5, 1)
    try:
        session.flush()
    except saexc.InternalError as e:
        assert 'tasks outside edition period' in str(e)
    else:
        assert False, "Should raise an SQL error"
    finally:
        session.rollback()
