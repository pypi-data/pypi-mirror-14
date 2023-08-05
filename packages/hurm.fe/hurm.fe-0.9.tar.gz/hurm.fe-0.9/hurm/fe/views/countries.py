# -*- coding: utf-8 -*-
# :Project:   hurm -- Countries data view
# :Created:   mar 02 feb 2016 19:05:05 CET
# :Author:    Lele Gaifax <lele@metapensiero.it>
# :License:   GNU General Public License version 3 or later
# :Copyright: © 2016 Lele Gaifax
#

from operator import itemgetter

from pyramid.view import view_config


@view_config(route_name="countries", renderer="json")
def _countries(request):
    from gettext import translation
    from pycountry import LOCALES_DIR, countries

    lname = request.locale_name
    try:
        t = translation('iso3166', LOCALES_DIR, languages=[lname]).gettext
    except IOError:
        t = lambda x: x
    result = [dict(code=c.alpha2, name=t(c.name)) for c in countries]

    result.sort(key=itemgetter('name'))

    return dict(count=len(result),
                message="Ok",
                root=result,
                success=True)
