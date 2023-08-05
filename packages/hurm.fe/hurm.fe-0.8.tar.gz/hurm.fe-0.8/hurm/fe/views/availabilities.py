# -*- coding: utf-8 -*-
# :Project:   hurm -- Availabilities data view
# :Created:   mar 02 feb 2016 23:41:55 CET
# :Author:    Lele Gaifax <lele@metapensiero.it>
# :License:   GNU General Public License version 3 or later
# :Copyright: © 2016 Lele Gaifax
#

from pyramid.view import view_config

from sqlalchemy import func, select, text

from hurm.db.tables import availabilities, duties, persons, tasks

from ..i18n import translatable_string as _
from . import expose


_a = availabilities.alias('a')
_d = duties.alias('d')
_p = persons.alias('p')
_t = tasks.alias('t')

_nduties = (
    select([func.count()],
           from_obj=_d.join(_t))
    .where(_t.c.idedition == _a.c.idedition)
    .where(_t.c.date == _a.c.date)
    .where(_d.c.idperson == _p.c.idperson)
    .where(_d.c.starttime >= func.coalesce(_a.c.starttime, '00:00'))
    .where(_d.c.endtime <= func.coalesce(_a.c.endtime, '24:00'))
)

_ptime = (
    select([func.to_char(func.sum(_d.c.endtime - _d.c.starttime), 'HH24:MI')],
           from_obj=_d.join(_t))
    .where(_t.c.idedition == _a.c.idedition)
    .where(_t.c.date == _a.c.date)
    .where(_d.c.idperson == _p.c.idperson)
    .where(_d.c.starttime >= func.coalesce(_a.c.starttime, '00:00'))
    .where(_d.c.endtime <= func.coalesce(_a.c.endtime, '24:00'))
)

@view_config(route_name='availabilities', renderer='json')
@expose(select([_a.c.idavailability,
                _a.c.idedition,
                _a.c.idperson,
                # text() is needed here, to workaround default normalization
                # performed by the Name type decorator, sigh...
                (_p.c.lastname + text("' '") + _p.c.firstname).label('Person'),
                _a.c.date,
                _a.c.starttime,
                _a.c.endtime,
                _a.c.note,
                _nduties.as_scalar().label('NDuties'),
                _ptime.as_scalar().label('Time')],
               from_obj=_a.join(_p)),
        metadata=dict(
            NDuties=dict(
                hint=_("Number of duties assigned to the person"),
                label=_("Duties"),
            ),
            Person=dict(
                flex=1,
                hint=_('Full name of the person'),
                label=_('Person'),
                lookup=dict(url='/data/available_persons',
                            idField='idperson',
                            displayField='fullname'),
            ),
            Time=dict(
                label=_('Time'),
                hint=_('Assigned time'),
                width=50,
            ),
            endtime=dict(min='07:00'),
            starttime=dict(min='07:00'),
            note=dict(width=120),
        ))
def _availabilities(request, results):
    return results
