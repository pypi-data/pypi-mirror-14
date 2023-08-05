# -*- coding: utf-8 -*-
# :Project:   hurm -- Subcountries data view
# :Created:   mar 02 feb 2016 19:47:59 CET
# :Author:    Lele Gaifax <lele@metapensiero.it>
# :License:   GNU General Public License version 3 or later
# :Copyright: © 2016 Lele Gaifax
#

from operator import itemgetter

from pyramid.view import view_config


@view_config(route_name="subcountries", renderer="json")
def _subcountries(request):
    from gettext import translation
    from pycountry import LOCALES_DIR, subdivisions

    country = request.params.get('country', 'IT')

    lname = request.locale_name
    try:
        t = translation('iso3166_2', LOCALES_DIR, languages=[lname]).gettext
    except IOError:
        t = lambda x: x

    result = [dict(code=s.code, name=t(s.name))
              for s in subdivisions.get(country_code=country)
              if country != 'IT' or s.type == 'Province']

    result.sort(key=itemgetter('name'))

    return dict(count=len(result),
                message="Ok",
                root=result,
                success=True)
