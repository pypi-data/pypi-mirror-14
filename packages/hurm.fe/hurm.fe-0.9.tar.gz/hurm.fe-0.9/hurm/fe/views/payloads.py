# -*- coding: utf-8 -*-
# :Project:   hurm -- Activity payloads data view
# :Created:   dom 28 feb 2016 01:06:25 CET
# :Author:    Lele Gaifax <lele@metapensiero.it>
# :License:   GNU General Public License version 3 or later
# :Copyright: © 2016 Lele Gaifax
#

from pyramid.view import view_config

from sqlalchemy import and_, func, select

from hurm.db.tables import activitypayloads, duties, dutypayloads, tasks

from ..i18n import translatable_string as _
from . import expose


_ap = activitypayloads.alias('ap')
_d = duties.alias('d')
_dp = dutypayloads.alias('dp')
_t = tasks.alias('t')


@view_config(route_name='activity_payloads', renderer='json')
@expose(select([_ap.c.idactivitypayload,
                _ap.c.idactivity,
                _ap.c.description,
                _ap.c.note,
                _ap.c.unitcost,
                select([func.count(_dp.c.iddutypayload)],
                       _dp.c.idactivitypayload == _ap.c.idactivitypayload)
                .as_scalar().label('DutyPayloads')]),
        metadata=dict(
            DutyPayloads=dict(
                hidden=True,
                label=_('Duty payloads'),
                hint=_('Number of duty payloads associated to the activity payload,'
                       ' in any edition.')
            ),
            description=dict(flex=1),
            note=dict(width=120),
        ))
def _activity_payloads(request, results):
    return results


@view_config(route_name='duty_payloads', renderer='json')
@expose(select([_d.c.idduty, # this is needed to avoid warning about ambiguous idduty
                _ap.c.idactivitypayload,
                _ap.c.description,
                _ap.c.note,
                _dp.c.value],
               from_obj=_d.join(_t).join(_ap, _ap.c.idactivity == _t.c.idactivity)
               .outerjoin(_dp, and_(_dp.c.idduty == _d.c.idduty,
                                    _dp.c.idactivitypayload == _ap.c.idactivitypayload))))
def _duty_payloads(request, results):
    return results
