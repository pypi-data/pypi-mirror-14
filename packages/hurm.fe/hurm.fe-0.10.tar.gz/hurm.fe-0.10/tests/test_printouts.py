# -*- coding: utf-8 -*-
# :Project:   hurm -- Test for the PDF generation views
# :Created:   ven 12 feb 2016 10:26:38 CET
# :Author:    Lele Gaifax <lele@metapensiero.it>
# :License:   GNU General Public License version 3 or later
# :Copyright: © 2016 Lele Gaifax
#

from datetime import timedelta

import pytest

from hurm.fe.printouts import render_timedelta


def test_person_duties(app, test_edition, jane_tree):
    response = app.get('/pdf/duties/edition/%d/person/%d' %
                       (test_edition.idedition, jane_tree.idperson))
    assert response.content_type == 'application/pdf'


def test_location_duties(app, test_edition, reception):
    response = app.get('/pdf/duties/edition/%d/location/%d' %
                       (test_edition.idedition, reception.idlocation))
    assert response.content_type == 'application/pdf'


def test_by_location_duties(app, test_edition):
    response = app.get('/pdf/duties/edition/%d/locations' % test_edition.idedition)
    assert response.content_type == 'application/pdf'


def test_by_person_duties(app, test_edition):
    response = app.get('/pdf/duties/edition/%d/persons' % test_edition.idedition)
    assert response.content_type == 'application/pdf'


def test_persons_duties_summary(app, test_edition):
    response = app.get('/pdf/duties/edition/%d/summary' % test_edition.idedition)
    assert response.content_type == 'application/pdf'


@pytest.mark.parametrize('tdelta,expected', [
    (timedelta(hours=5, minutes=30), '5:30'),
    (timedelta(days=1, hours=5, minutes=45), '29:45'),
    (timedelta(days=-1, hours=4, minutes=15), '-19:45'),
    (None, '0:00'),
])
def test_render_timedelta(tdelta, expected):
    assert render_timedelta(tdelta) == expected
