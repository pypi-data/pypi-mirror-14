# -*- coding: utf-8 -*-
# :Project:   hurm -- Tests for the helper functions
# :Created:   mar 09 feb 2016 16:56:54 CET
# :Author:    Lele Gaifax <lele@metapensiero.it>
# :License:   GNU General Public License version 3 or later
# :Copyright: © 2016 Lele Gaifax
#

from datetime import date, time

from hurm.db import entities, tables, utils


def test_normalize():
    assert utils.normalize(None) is None
    assert utils.normalize('lele gaifax') == 'Lele Gaifax'
    assert utils.normalize('LELE') == 'Lele'
    assert utils.normalize('LeLe', title=False) == 'LeLe'


def test_njoin():
    assert utils.njoin([1,2,3]) == '1, 2 and 3'
    assert utils.njoin([1,2]) == '1 and 2'
    assert utils.njoin([1]) == '1'
    assert utils.njoin([]) == ''
    assert utils.njoin([1,2], stringify=lambda x: str(x*10)) == '10 and 20'
    assert utils.njoin(['first', None, False, '', 'last']) == 'first and last'
    assert utils.njoin([1,0,2]) == '1, 0 and 2'


def test_changes_summary():
    assert utils.changes_summary(dict(a=(None, 1))) == 'changed a to 1'
    assert utils.changes_summary(dict(a=(False, True))) == 'changed a from False to True'
    assert utils.changes_summary(dict(a=(0,1), b=('foo','bar'))) == \
        'changed a from 0 to 1 and b from "foo" to "bar"'
    assert utils.changes_summary(dict(a=(0,1), b=(None,'bar'), c=(True,None))) == \
        'changed a from 0 to 1, b to "bar" and c from True to None'


def test_table_from_primary_key(session):
    assert utils.table_from_primary_key('idedition') is tables.editions
    try:
        utils.table_from_primary_key('foobar')
    except RuntimeError:
        pass
    else:
        assert False, "Should raise a RuntimeError"


def test_entity_from_primary_key(session):
    assert utils.entity_from_primary_key('idedition') is entities.Edition
    try:
        utils.entity_from_primary_key('foobar')
    except RuntimeError:
        pass
    else:
        assert False, "Should raise a RuntimeError"


def test_save_changes(session, edition_test, presence, supervision):
    try:
        i, m, d = utils.save_changes(session, None,
                                     [('idedition', {'idedition': edition_test.idedition,
                                                     'description': 'this is a test',
                                                     'does_not_exist': 'dummy'}),
                                      ('idperson', {'firstname': 'foo',
                                                    'lastname': 'bar',
                                                    'password': 'simple',
                                                    'role': '',
                                                    'idactivities': [presence.idactivity]}),
                                     ('idavailability', {'idedition': edition_test.idedition,
                                                         'idperson': 0,
                                                         'date': date(2016, 4, 30),
                                                         'note': 'dummy note'})],
                                     [])
        assert list(i[0].keys()) == ['idperson']
        assert m == [{'idedition': edition_test.idedition}]
        assert d == []
        assert edition_test.description == 'this is a test'

        foobar_id = i[0]['idperson']
        foobar = session.query(entities.Person).get(foobar_id)
        assert foobar.firstname == 'Foo'
        assert foobar.lastname == 'Bar'
        assert foobar.password and tables.password_manager.check(foobar.password, 'simple')
        assert foobar.role is None
        assert foobar.availabilities[0].note == 'dummy note'
        assert len(foobar.activities) == 1
        assert foobar.activities[0] is presence

        i, m, d = utils.save_changes(session, None,
                                     [('idperson', {'idperson': foobar_id,
                                                    'password': 'sample',
                                                    'idactivities': [supervision.idactivity]})],
                                     [])

        foobar = session.query(entities.Person).get(foobar_id)
        assert foobar.password and tables.password_manager.check(foobar.password, 'sample')
        assert len(foobar.activities) == 1
        assert foobar.activities[0] is supervision

        i, m, d = utils.save_changes(session, None,
                                     [('idperson', {'idperson': foobar_id,
                                                    'idactivities': None})],
                                     [])

        foobar = session.query(entities.Person).get(foobar_id)
        assert len(foobar.activities) == 0

        idavail = foobar.availabilities[0].idavailability
        i, m, d = utils.save_changes(session, None, [],
                                     [('idavailability', idavail)])
        assert i == []
        assert m == []
        assert d == [{'idavailability': idavail}]

        idpers = foobar.idperson
        i, m, d = utils.save_changes(session, None, [],
                                     [('idperson', idpers)])
        assert i == []
        assert m == []
        assert d == [{'idperson': idpers}]
    finally:
        session.rollback()


def test_save_changes_payloads(session, edition_test, hugh_fiver, premiere_lizards,
                               subtitles_count, synchro_subtitles_count):
    try:
        i, m, d = utils.save_changes(
            session, None,
            [('idduty',
              {'idperson': hugh_fiver.idperson,
               'idtask': premiere_lizards.idtask,
               'starttime': time(21, 0),
               'endtime': time(22, 0),
               'payloads': [{'idactivitypayload': subtitles_count.idactivitypayload,
                             'value': 234},
                            {'idactivitypayload': synchro_subtitles_count.idactivitypayload,
                             'value': 123}]})],
            [])
        assert list(i[0].keys()) == ['idduty']
        idduty = i[0]['idduty']
        duty = session.query(entities.Duty).get(idduty)
        payloads = duty.payloads
        assert len(payloads) == 2
        for payload in payloads:
            if payload.idactivitypayload == subtitles_count.idactivitypayload:
                assert payload.value == 234
            else:
                assert payload.value == 123

        i, m, d = utils.save_changes(
            session, None,
            [('idduty',
              {'idduty': idduty,
               'payloads': [{'idactivitypayload': subtitles_count.idactivitypayload,
                             'value': 23},
                            {'idactivitypayload': synchro_subtitles_count.idactivitypayload,
                             'value': 12}]})],
            [])

        duty = session.query(entities.Duty).get(idduty)
        payloads = duty.payloads
        assert len(payloads) == 2
        for payload in payloads:
            if payload.idactivitypayload == subtitles_count.idactivitypayload:
                assert payload.value == 23
            else:
                assert payload.value == 12
    finally:
        session.rollback()


def test_save_changes_payloads_2(session, edition_test, hugh_fiver, premiere_lizards,
                                 subtitles):
    i, m, d = utils.save_changes(
        session, None,
        [('idactivitypayload',
          {'idactivity': subtitles.idactivity,
           'description': 'Foo',
           'note': 'Bar'})],
        [])
    assert list(i[0].keys()) == ['idactivitypayload']
    idapl = i[0]['idactivitypayload']

    session.commit()

    i, m, d = utils.save_changes(
        session, None,
        [('idduty',
          {'idperson': hugh_fiver.idperson,
           'idtask': premiere_lizards.idtask,
           'starttime': time(21, 0),
           'endtime': time(22, 0),
           'payloads': [{'idactivitypayload': idapl, 'value': 234}]})],
        [])
    assert list(i[0].keys()) == ['idduty']
    idduty = i[0]['idduty']
    duty = session.query(entities.Duty).get(idduty)
    assert len(duty.payloads) == 1

    session.commit()

    i, m, d = utils.save_changes(session, None, [],
                                 [('idactivitypayload', idapl)])
    assert len(d) == 1

    session.commit()

    duty = session.query(entities.Duty).get(idduty)
    assert len(duty.payloads) == 0


def test_dumpy(edition_test):
    dump = utils.dump(edition_test, [{
        'entity': 'hurm.db.entities.edition.Edition',
        'key': 'description',
        'other': 'startdate,enddate,tasks'.split(',')
    }, {
        'entity': 'hurm.db.entities.activity.Activity',
        'key': 'description'
    }, {
        'entity': 'hurm.db.entities.location.Location',
        'key': 'description',
        'other': 'address,city,country,province,zip'.split(',')
    }, {
        'entity': 'hurm.db.entities.task.Task',
        'key': 'edition,activity,location,date,starttime'.split(','),
        'other': 'endtime,npersons,duties'.split(',')
    }, {
        'entity': 'hurm.db.entities.person.Person',
        'key': 'lastname,firstname'.split(','),
        'other': 'birthdate,mobile,phone,email,role,availabilities,preferred_activities'.split(',')
    }, {
        'entity': 'hurm.db.entities.personactivity.PersonActivity',
        'key': 'person,activity'.split(','),
    }, {
        'entity': 'hurm.db.entities.availability.Availability',
        'key': 'edition,person,date,starttime'.split(','),
        'other': 'endtime'
    }, {
        'entity': 'hurm.db.entities.duty.Duty',
        'key': 'person,task,starttime'.split(','),
        'other': 'endtime'
    }])

    assert dump[0]['data'][0]['description'] == edition_test.description
