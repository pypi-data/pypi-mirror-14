# -*- coding: utf-8 -*-
# :Project:   hurm
# :Created:   ven 22 gen 2016 16:48:43 CET
# :Author:    Lele Gaifax <lele@metapensiero.it>
# :License:   GNU General Public License version 3 or later
# :Copyright: © 2016 Lele Gaifax
#

from datetime import date, time

from sqlalchemy import exc as saexc

from hurm.db import entities


def test_out_edition_availability(session, edition_test, john_doe):
    na = entities.Availability()
    na.edition = edition_test
    na.person = john_doe
    na.date = date(2015, 5, 1)
    na.starttime = time(14, 0)
    na.endtime = time(16, 0)
    session.add(na)
    try:
        session.flush()
    except saexc.InternalError as e:
        assert 'availability date outside allowed period' in str(e)
    else:
        assert False, "Should raise an SQL error"
    finally:
        session.rollback()


def test_non_overlapping_availability(session, edition_test, john_doe):
    na = entities.Availability()
    na.edition = edition_test
    na.person = john_doe
    na.date = date(2016, 5, 1)
    na.starttime = time(15, 0)
    na.endtime = time(16, 0)
    session.add(na)
    try:
        session.flush()
    finally:
        session.rollback()


def test_overlapping_availability(session, edition_test, john_doe, bob_quartz):
    na = entities.Availability()
    na.edition = edition_test
    na.person = john_doe
    na.date = date(2016, 5, 1)
    na.starttime = time(14, 0)
    na.endtime = time(16, 0)
    session.add(na)
    try:
        session.flush()
    except saexc.InternalError as e:
        assert 'overlapped availability' in str(e)
    else:
        assert False, "Should raise an SQL error"
    finally:
        session.rollback()

    na = entities.Availability()
    na.edition = edition_test
    na.person = bob_quartz
    na.date = date(2016, 5, 1)
    na.starttime = time(8, 0)
    na.endtime = time(9, 0)
    session.add(na)
    try:
        session.flush()
    except saexc.InternalError as e:
        assert 'overlapped availability' in str(e)
    else:
        assert False, "Should raise an SQL error"
    finally:
        session.rollback()


def test_invalid_availability_edit(session, availability_john_doe_05_01):
    session.delete(availability_john_doe_05_01)
    try:
        session.flush()
    except saexc.InternalError as e:
        assert 'duties outside person availability' in str(e)
    else:
        assert False, "Should raise an SQL error"
    finally:
        session.rollback()

    availability_john_doe_05_01.endtime = time(10, 10)
    try:
        session.flush()
    except saexc.InternalError as e:
        assert 'duties outside person availability' in str(e)
    else:
        assert False, "Should raise an SQL error"
    finally:
        session.rollback()


def test_valid_availability_edit(session, availability_john_doe_04_30):
    availability_john_doe_04_30.note = 'Foo bar'
    try:
        session.flush()
    finally:
        session.rollback()

    availability_john_doe_04_30.starttime = time(10, 0)
    availability_john_doe_04_30.endtime = time(19, 0)
    try:
        session.flush()
    finally:
        session.rollback()
