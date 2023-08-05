# -*- coding: utf-8 -*-
# :Project:   hurm
# :Created:   ven 22 gen 2016 16:53:21 CET
# :Author:    Lele Gaifax <lele@metapensiero.it>
# :License:   GNU General Public License version 3 or later
# :Copyright: © 2016 Lele Gaifax
#

from datetime import date
from os import getenv

import pytest

from sqlalchemy import create_engine

from hurm.db import metadata, entities


@pytest.fixture(scope="session", autouse=True)
def engine():
    metadata.bind = entities.DBSession.bind = create_engine(getenv('TEST_DB_URL'))


@pytest.fixture(scope="module")
def session():
    return entities.DBSession()


@pytest.fixture
def edition_test(session):
    return session.query(entities.Edition).filter_by(description='Test edition').one()


@pytest.fixture
def john_doe(session):
    return session.query(entities.Person).filter_by(lastname='Doe').one()


@pytest.fixture
def jane_tree(session):
    return session.query(entities.Person).filter_by(lastname='Tree').one()


@pytest.fixture
def bob_quartz(session):
    return session.query(entities.Person).filter_by(lastname='Quartz').one()


@pytest.fixture
def hugh_fiver(session):
    return session.query(entities.Person).filter_by(lastname='Fiver').one()


@pytest.fixture
def presence(session):
    return session.query(entities.Activity).filter_by(description='Presence').one()


@pytest.fixture
def supervision(session):
    return session.query(entities.Activity).filter_by(description='Supervision').one()


@pytest.fixture
def subtitles(session):
    return session.query(entities.Activity).filter_by(description='Subtitles').one()


@pytest.fixture
def reception(session):
    return session.query(entities.Location).filter_by(description='Reception').one()


@pytest.fixture
def cinema(session):
    return session.query(entities.Location).filter_by(description='Cinema Modena').one()


@pytest.fixture
def reception_presence_05_01(session, edition_test, presence, reception):
    return session.query(entities.Task).filter_by(idedition=edition_test.idedition,
                                                  idactivity=presence.idactivity,
                                                  idlocation=reception.idlocation,
                                                  date=date(2016, 5, 1)).one()


@pytest.fixture
def premiere_lizards(session, edition_test, subtitles, cinema):
    return session.query(entities.Task).filter_by(idedition=edition_test.idedition,
                                                  idactivity=subtitles.idactivity,
                                                  idlocation=cinema.idlocation,
                                                  date=date(2016, 5, 1)).one()


@pytest.fixture
def availability_john_doe_04_30(session, edition_test, john_doe):
    return session.query(entities.Availability).filter_by(idedition=edition_test.idedition,
                                                          idperson=john_doe.idperson,
                                                          date=date(2016, 4, 30)).one()


@pytest.fixture
def availability_john_doe_05_01(session, edition_test, john_doe):
    return session.query(entities.Availability).filter_by(idedition=edition_test.idedition,
                                                          idperson=john_doe.idperson,
                                                          date=date(2016, 5, 1)).one()


@pytest.fixture
def subtitles_count(session, subtitles):
    return session.query(entities.ActivityPayload).filter_by(
        idactivity=subtitles.idactivity, description="Subtitles").one()


@pytest.fixture
def synchro_subtitles_count(session, subtitles):
    return session.query(entities.ActivityPayload).filter_by(
        idactivity=subtitles.idactivity, description="Synchro subtitles").one()
