# -*- coding: utf-8 -*-
# :Project:   hurm -- Test for the downloads views
# :Created:   mer 17 feb 2016 13:23:58 CET
# :Author:    Lele Gaifax <lele@metapensiero.it>
# :License:   GNU General Public License version 3 or later
# :Copyright: © 2016 Lele Gaifax
#

def test_yaml_dump(app, test_edition):
    response = app.get('/yaml/edition/%d' % test_edition.idedition)
    assert response.content_type == 'application/x-yaml'


def test_excel_dump(app, test_edition):
    response = app.get('/xls/edition/%d' % test_edition.idedition)
    assert response.content_type == 'application/vnd.ms-excel'
