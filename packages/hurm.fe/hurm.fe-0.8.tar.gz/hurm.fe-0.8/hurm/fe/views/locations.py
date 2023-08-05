# -*- coding: utf-8 -*-
# :Project:   hurm -- Locations data view
# :Created:   mar 02 feb 2016 18:50:01 CET
# :Author:    Lele Gaifax <lele@metapensiero.it>
# :License:   GNU General Public License version 3 or later
# :Copyright: © 2016 Lele Gaifax
#

from pyramid.view import view_config

from sqlalchemy import func, select

from hurm.db.tables import locations, tasks

from ..i18n import translatable_string as _, translator
from . import expose


_l = locations.alias('l')
_t = tasks.alias('t')

@view_config(route_name='locations', renderer='json')
@expose(select([_l.c.idlocation,
                _l.c.description,
                _l.c.address,
                _l.c.city,
                _l.c.province,
                _l.c.zip,
                _l.c.country,
                _l.c.latitude,
                _l.c.longitude,
                _l.c.phone,
                _l.c.mobile,
                _l.c.email,
                _l.c.note,
                select([func.count(_t.c.idtask)],
                       _t.c.idlocation == _l.c.idlocation)
                .as_scalar().label('Tasks')]),
        metadata=dict(
            Tasks=dict(
                hidden=True,
                label=_('Tasks'),
                hint=_('Number of tasks associated to the location, in any edition.')
            ),
            address=dict(width=150),
            city=dict(width=70),
            country=dict(hidden=True),
            description=dict(flex=1),
            email=dict(hidden=True, width=100, vtype='email'),
            latitude=dict(hidden=True),
            longitude=dict(hidden=True),
            mobile=dict(hidden=True, vtype='phone'),
            note=dict(width=120),
            phone=dict(hidden=True, vtype='phone'),
            province=dict(hidden=True),
            zip=dict(hidden=True),
        ))
def _locations(request, results):
    from gettext import translation
    from pycountry import LOCALES_DIR, countries, subdivisions

    if 'metadata' in results:
        t = translator(request)
        results['metadata']['fields'].append({
            'label': t(_('Country')),
            'hint': t(_('The name of the country')),
            'name': 'Country',
            'nullable': True,
            'hidden': True,
            'lookup': dict(url='/data/countries',
                           remoteFilter=False,
                           lookupField='country',
                           idField='code',
                           displayField='name'),
        })
        results['metadata']['fields'].append({
            'label': t(_('Province')),
            'hint': t(_('The name of the province')),
            'name': 'Province',
            'nullable': True,
            'hidden': True,
            'lookup': dict(url='/data/subcountries',
                           remoteFilter=False,
                           lookupField='province',
                           idField='code',
                           displayField='name'),
        })

    if 'root' in results:
        lname = request.locale_name
        try:
            tc = translation('iso3166', LOCALES_DIR, languages=[lname]).gettext
        except IOError:
            tc = lambda x: x
        try:
            tp = translation('iso3166_2', LOCALES_DIR, languages=[lname]).gettext
        except IOError:
            tp = lambda x: x

        locations = results['root']
        for location in locations:
            code = location.get('country', False)
            if code:
                location['Country'] = tc(countries.get(alpha2=code).name)
            elif code is not False:
                location['Country'] = None
            code = location.get('province', False)
            if code:
                location['Province'] = tp(subdivisions.get(code=code).name)
            elif code is not False:
                location['Province'] = None

    return results
