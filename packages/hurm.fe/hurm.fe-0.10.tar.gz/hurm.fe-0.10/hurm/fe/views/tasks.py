# -*- coding: utf-8 -*-
# :Project:   hurm -- Tasks data view
# :Created:   mer 03 feb 2016 19:02:42 CET
# :Author:    Lele Gaifax <lele@metapensiero.it>
# :License:   GNU General Public License version 3 or later
# :Copyright: © 2016 Lele Gaifax
#

from pyramid.view import view_config

from sqlalchemy import select, Boolean, Integer
from sqlalchemy.sql.expression import literal_column

from hurm.db.tables import activities, locations, tasks

from ..i18n import translatable_string as _
from . import expose


_a = activities.alias('a')
_l = locations.alias('l')
_t = tasks.alias('t')

@view_config(route_name='tasks', renderer='json')
@expose(select([_t.c.idtask,
                _t.c.idedition,
                _t.c.idlocation,
                _l.c.description.label('Location'),
                _t.c.date,
                _t.c.starttime,
                _t.c.endtime,
                _t.c.idactivity,
                _a.c.description.label('Activity'),
                _t.c.npersons,
                literal_column(
                    "not exists (select 1 from task_timeline(t.idtask) tl"
                    " where tl.npersons < t.npersons)"
                    , Boolean).label('Complete'),
                literal_column(
                    "cast(100 *"
                    " extract(epoch from (select sum((tl.endtime-tl.starttime)*tl.npersons)"
                    " from task_timeline(t.idtask) tl))"
                    " /"
                    " extract(epoch from (coalesce(t.endtime, '24:00')-t.starttime)*t.npersons) as integer)"
                    , Integer).label('Coverage'),
                _t.c.note],
               from_obj=_t.join(_l).join(_a)),
        metadata=dict(
            Activity=dict(
                hint=_('Description of the activity'),
                label=_('Activity'),
                lookup=dict(url='/data/activities?only_cols=idactivity,description'
                            '&sort=description',
                            idField='idactivity',
                            displayField='description'),
                width=100,
            ),
            Complete=dict(
                hint=_('Whether the task is completely covered'),
                label=_('Complete'),
                width=60,
            ),
            Coverage=dict(
                hint=_('Percentage of time covered by assigned duties'),
                label=_('%'),
                width=50,
            ),
            Location=dict(
                flex=1,
                hint=_('Description of the location'),
                label=_('Location'),
                lookup=dict(url='/data/locations?only_cols=idlocation,description'
                            '&sort=description',
                            idField='idlocation',
                            displayField='description'),
            ),
            endtime=dict(min='07:00'),
            note=dict(width=120),
            npersons=dict(min=1),
            starttime=dict(min='07:00'),
        ))
def _tasks(request, results):
    return results
