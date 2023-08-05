# -*- coding: utf-8 -*-
# :Project:   hurm -- Functional tests configuration
# :Created:   dom 07 feb 2016 18:23:13 CET
# :Author:    Lele Gaifax <lele@metapensiero.it>
# :License:   GNU General Public License version 3 or later
# :Copyright: © 2016 Lele Gaifax
#

from datetime import date, time

from pyramid.paster import get_appsettings
from webtest import TestApp
import pytest

from hurm.db import entities
from hurm.fe import main


@pytest.fixture(scope="module")
def app():
    settings = get_appsettings('test.ini')
    app = TestApp(main({}, **settings))
    app.post('/auth/login', {'email': 'bob@example.com', 'password': 'test'})
    return app


@pytest.fixture(scope="module")
def session():
    return entities.DBSession()


@pytest.fixture
def test_edition(session):
    return session.query(entities.Edition).filter_by(description='Test edition').one()


@pytest.fixture
def jane_tree(session):
    return session.query(entities.Person).filter_by(lastname='Tree').one()


@pytest.fixture
def hugh_fiver(session):
    return session.query(entities.Person).filter_by(lastname='Fiver').one()


@pytest.fixture
def reception(session):
    return session.query(entities.Location).filter_by(description='Reception').one()


@pytest.fixture
def cinema_1(session):
    return session.query(entities.Location).filter_by(description='Cinema Modena, Room 1').one()


@pytest.fixture
def subtitles(session):
    return session.query(entities.Activity).filter_by(description='Subtitles').one()


@pytest.fixture
def the_giants_04_30(session, test_edition, subtitles, cinema_1):
    return session.query(entities.Task).filter_by(idedition=test_edition.idedition,
                                                  idactivity=subtitles.idactivity,
                                                  idlocation=cinema_1.idlocation,
                                                  date=date(2016, 4, 30),
                                                  starttime=time(20, 0)).one()

@pytest.fixture
def premiere_the_giants_04_30(session, hugh_fiver, the_giants_04_30):
    return session.query(entities.Duty).filter_by(idperson=hugh_fiver.idperson,
                                                  idtask=the_giants_04_30.idtask).one()
