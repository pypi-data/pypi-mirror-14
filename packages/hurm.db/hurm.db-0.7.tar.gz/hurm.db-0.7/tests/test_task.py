# -*- coding: utf-8 -*-
# :Project:   hurm
# :Created:   ven 22 gen 2016 21:37:30 CET
# :Author:    Lele Gaifax <lele@metapensiero.it>
# :License:   GNU General Public License version 3 or later
# :Copyright: © 2016 Lele Gaifax
#

from datetime import date, time

from sqlalchemy import exc as saexc, sql

from hurm.db import entities


def test_out_edition_task(session, edition_test, presence, reception):
    t = entities.Task()
    t.edition = edition_test
    t.location = reception
    t.activity = presence
    t.date = date(2015, 5, 1)
    t.starttime = time(14, 0)
    t.endtime = time(16, 0)
    t.npersons = 1
    session.add(t)
    try:
        session.flush()
    except saexc.InternalError as e:
        assert 'task date outside allowed period' in str(e)
    else:
        assert False, "Should raise an SQL error"
    finally:
        session.rollback()


def test_non_overlapping_task(session, edition_test, presence, reception):
    t = entities.Task()
    t.edition = edition_test
    t.location = reception
    t.activity = presence
    t.date = date(2016, 5, 1)
    t.starttime = time(22, 0)
    t.endtime = time(23, 0)
    t.npersons = 1
    session.add(t)
    try:
        session.flush()
    finally:
        session.rollback()


def test_overlapping_task(session, edition_test, presence, reception):
    t = entities.Task()
    t.edition = edition_test
    t.location = reception
    t.activity = presence
    t.date = date(2016, 5, 1)
    t.starttime = time(14, 0)
    t.endtime = time(16, 0)
    t.npersons = 1
    session.add(t)
    try:
        session.flush()
    except saexc.InternalError as e:
        assert 'overlapped task' in str(e)
    else:
        assert False, "Should raise an SQL error"
    finally:
        session.rollback()


def test_invalid_task_edit(session, reception_presence_05_01):
    reception_presence_05_01.endtime = time(9, 0)
    try:
        session.flush()
    except saexc.InternalError as e:
        assert 'duties outside task time range' in str(e)
    else:
        assert False, "Should raise an SQL error"
    finally:
        session.rollback()


def test_task_timeline(session, reception_presence_05_01):
    c = session.connection()
    q = sql.text("SELECT starttime, endtime, npersons FROM task_timeline(:idtask)")
    r = c.execute(q, idtask=reception_presence_05_01.idtask).fetchall()
    assert len(r) == 4
    assert r[0]['starttime'] == reception_presence_05_01.starttime
    assert r[-1]['endtime'] == reception_presence_05_01.endtime
