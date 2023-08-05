# -*- coding: utf-8 -*-
# :Project:   hurm
# :Created:   sab 23 gen 2016 09:55:21 CET
# :Author:    Lele Gaifax <lele@metapensiero.it>
# :License:   GNU General Public License version 3 or later
# :Copyright: © 2016 Lele Gaifax
#

from datetime import time

from sqlalchemy import exc as saexc

from hurm.db import entities


def test_out_task_duty(session, reception_presence_05_01, bob_quartz):
    d = entities.Duty()
    d.person = bob_quartz
    d.task = reception_presence_05_01
    d.starttime = time(7, 0)
    d.endtime = time(8, 0)
    session.add(d)
    try:
        session.flush()
    except saexc.InternalError as e:
        assert 'duty time outside task time' in str(e)
    else:
        assert False, "Should raise an SQL error"
    finally:
        session.rollback()


def test_out_person_duty(session, reception_presence_05_01, john_doe):
    d = entities.Duty()
    d.person = john_doe
    d.task = reception_presence_05_01
    d.starttime = time(15, 0)
    d.endtime = time(16, 0)
    session.add(d)
    try:
        session.flush()
    except saexc.InternalError as e:
        assert 'duty time outside person availability' in str(e)
    else:
        assert False, "Should raise an SQL error"
    finally:
        session.rollback()


def test_non_overlapping_duty(session, reception_presence_05_01, bob_quartz):
    d = entities.Duty()
    d.person = bob_quartz
    d.task = reception_presence_05_01
    d.starttime = time(8, 0)
    d.endtime = time(10, 0)
    session.add(d)
    try:
        session.flush()
    finally:
        session.rollback()


def test_overlapping_duty(session, reception_presence_05_01, jane_tree):
    d = entities.Duty()
    d.person = jane_tree
    d.task = reception_presence_05_01
    d.starttime = time(11, 0)
    d.endtime = time(11, 30)
    session.add(d)
    try:
        session.flush()
    except saexc.InternalError as e:
        assert 'overlapped duty' in str(e)
    else:
        assert False, "Should raise an SQL error"
    finally:
        session.rollback()
