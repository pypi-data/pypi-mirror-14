# -*- coding: utf-8 -*-
# :Project:   hurm -- Editions data view
# :Created:   mar 02 feb 2016 16:54:48 CET
# :Author:    Lele Gaifax <lele@metapensiero.it>
# :License:   GNU General Public License version 3 or later
# :Copyright: © 2016 Lele Gaifax
#

from pyramid.view import view_config

from sqlalchemy import func, select

from hurm.db.tables import editions, tasks

from ..i18n import translatable_string as _
from . import expose


_e = editions.alias('e')
_t = tasks.alias('t')

@view_config(route_name='editions', renderer='json')
@expose(select([_e.c.idedition,
                _e.c.description,
                _e.c.startdate,
                _e.c.enddate,
                _e.c.note,
                select([func.count(_t.c.idtask)],
                       _t.c.idedition == _e.c.idedition)
                .as_scalar().label('Tasks')]),
        metadata=dict(
            Tasks=dict(
                label=_('Tasks'),
                hint=_('Number of tasks defined for the edition.')
            ),
            description=dict(flex=1),
            note=dict(width=120),
        ))
def _editions(request, results):
    return results
