# -*- coding: utf-8 -*-
# :Project:   hurm -- Activities data view
# :Created:   mar 02 feb 2016 17:36:07 CET
# :Author:    Lele Gaifax <lele@metapensiero.it>
# :License:   GNU General Public License version 3 or later
# :Copyright: © 2016 Lele Gaifax
#

from pyramid.view import view_config

from sqlalchemy import func, select

from hurm.db.tables import activities, personactivities, tasks

from ..i18n import translatable_string as _
from . import expose


_a = activities.alias('a')
_t = tasks.alias('t')

@view_config(route_name='activities', renderer='json')
@expose(select([_a.c.idactivity,
                _a.c.description,
                _a.c.allowoverlappedduties,
                _a.c.allowoverlappedtasks,
                _a.c.note,
                select([func.count(_t.c.idtask)],
                       _t.c.idactivity == _a.c.idactivity)
                .as_scalar().label('Tasks')]),
        metadata=dict(
            Tasks=dict(
                hidden=True,
                label=_('Tasks'),
                hint=_('Number of tasks associated to the activity, in any edition.')
            ),
            allowoverlappedduties=dict(hidden=True),
            allowoverlappedtasks=dict(hidden=True),
            description=dict(flex=1),
            note=dict(width=120),
        ))
def _activities(request, results):
    return results


_pa = personactivities.alias('pa')

@view_config(route_name='preferred_activities', renderer='json')
@expose(select([_a.c.idactivity,
                _a.c.description,
                select([func.count(_pa.c.idperson)],
                       _pa.c.idactivity == _a.c.idactivity)
                .as_scalar().label('Persons')]),
        metadata=dict(
        ))
def _preferred_activities(request, results):
    return results
