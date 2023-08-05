# -*- coding: utf-8 -*-
# :Project:   hurm -- Tests for the data views
# :Created:   dom 07 feb 2016 18:38:43 CET
# :Author:    Lele Gaifax <lele@metapensiero.it>
# :License:   GNU General Public License version 3 or later
# :Copyright: © 2016 Lele Gaifax
#

import pytest

from metapensiero.sqlalchemy.proxy.json import py2json

@pytest.mark.parametrize("view", [
    '/data/activities',
    '/data/availabilities',
    '/data/available_persons',
    '/data/countries',
    '/data/duties',
    '/data/editions',
    '/data/locations',
    '/data/persons',
    '/data/subcountries',
    '/data/tasks',
])
def test_fetch(app, view):
    response = app.get(view)
    result = response.json
    assert result['success'] is True
    assert result['message'] == "Ok"
    assert result['count'] > 0
    assert isinstance(result['root'], list)
    assert isinstance(result['root'][0], dict)


def test_available_persons_for_task(app, test_edition):
    task = test_edition.tasks[0]
    response = app.get('/data/available_persons?idtask=%d' % task.idtask)
    result = response.json
    assert result['success'] is True
    assert result['message'] == "Ok"
    assert result['count'] > 0
    assert isinstance(result['root'], list)
    assert isinstance(result['root'][0], dict)


def test_preferred_activities(app):
    response = app.get('/data/preferred_activities?sort=Persons&dir=DESC')
    result = response.json
    assert result['success'] is True
    assert result['message'] == "Ok"
    assert result['count'] > 0
    assert isinstance(result['root'], list)
    assert isinstance(result['root'][0], dict)
    assert result['root'][0]['Persons'] == 2


def test_activity_payloads(app, subtitles):
    response = app.get('/data/activity_payloads?idactivity=%d' % subtitles.idactivity)
    result = response.json
    assert result['success'] is True
    assert result['message'] == "Ok"
    assert result['count'] > 0
    assert isinstance(result['root'], list)
    assert isinstance(result['root'][0], dict)


def test_duty_payloads(app, premiere_the_giants_04_30):
    response = app.get('/data/duty_payloads?iduty=%d' % premiere_the_giants_04_30.idduty)
    result = response.json
    assert result['success'] is True
    assert result['message'] == "Ok"
    assert result['count'] > 0
    assert isinstance(result['root'], list)
    assert isinstance(result['root'][0], dict)


@pytest.mark.parametrize("view", [
    '/data/activities',
    '/data/availabilities',
    '/data/duties',
    '/data/editions',
    '/data/locations',
    '/data/persons',
    '/data/tasks',
])
def test_update(app, view):
    response = app.get(view, {'limit': 1, 'metadata': 'metadata'})
    result = response.json
    assert result['success'] is True
    assert result['message'] == "Ok"
    assert isinstance(result['root'], list)
    assert len(result['root']) == 1

    pkname = result['metadata']['primary_key']
    pkvalue = result['root'][0][pkname]
    change = (pkname, {pkname: pkvalue, 'note': 'Foo bar'})
    response = app.post(view, {'modified_records': py2json([change]),
                               'deleted_records': py2json([])})
    result = response.json
    assert result['success'] is True
    assert result['message'] == "Ok"

    response = app.get(view, {'limit': 1, 'filter_' + pkname: pkvalue})
    result = response.json
    assert result['success'] is True
    assert result['message'] == "Ok"
    assert result['root'][0]['note'] == 'Foo bar'
