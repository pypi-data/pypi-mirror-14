# -*- coding: utf-8 -*-
# :Project:   hurm -- Duties data view
# :Created:   mer 03 feb 2016 21:19:58 CET
# :Author:    Lele Gaifax <lele@metapensiero.it>
# :License:   GNU General Public License version 3 or later
# :Copyright: © 2016 Lele Gaifax
#

from pyramid.view import view_config

from sqlalchemy import select, text

from hurm.db.tables import activities, duties, locations, persons, tasks

from ..i18n import translatable_string as _
from . import expose

_a = activities.alias('a')
_d = duties.alias('d')
_l = locations.alias('l')
_p = persons.alias('p')
_t = tasks.alias('t')

query = select(
    [_d.c.idduty,
     _d.c.idtask,
     _d.c.idperson,
     # text() is needed here, to workaround default normalization
     # performed by the Name type decorator, sigh...
     (_p.c.lastname + text("' '") + _p.c.firstname).label('Person'),
     _t.c.date,
     _d.c.starttime,
     _d.c.endtime,
     _l.c.description.label('Location'),
     _a.c.description.label('Activity'),
     _d.c.note],
    from_obj=_d.join(_p).join(_t).join(_a).join(_l))

@view_config(route_name='duties', renderer='json')
@expose(query,
        metadata=dict(
            Activity=dict(width=120),
            Location=dict(flex=1),
            Person=dict(
                flex=1,
                hint=_('Full name of the person'),
                label=_('Person'),
                lookup=dict(
                    displayField='fullname',
                    idField='idperson',
                    url='/data/available_persons',
                    otherFields='Preferred',
                    innerTpl='<div><tpl if="Preferred"><strong></tpl>{fullname}<tpl if="Preferred"></strong></tpl></div>',
                ),
            ),
            endtime=dict(min='07:00'),
            note=dict(width=120),
            payloads=dict(hidden=True),
            starttime=dict(min='07:00'),
        ))
def _duties(request, results):
    if 'metadata' in results:
        results['metadata']['fields'].append({
            'name': 'payloads',
            'hidden': True,
            'label': 'Payloads',
        })

    if 'root' in results:
        for result in results['root']:
            result['payloads'] = []


    return results
