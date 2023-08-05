# -*- coding: utf-8 -*-
# :Project:   hurm -- Persons data view
# :Created:   mar 02 feb 2016 09:58:18 CET
# :Author:    Lele Gaifax <lele@metapensiero.it>
# :License:   GNU General Public License version 3 or later
# :Copyright: © 2016 Lele Gaifax
#

from pyramid.view import view_config

from sqlalchemy import and_, bindparam, cast, desc, exists, func, select, text, Text
from sqlalchemy.sql.expression import literal_column
from sqlalchemy.types import String

from hurm.db.tables import (
    activities,
    availabilities,
    duties,
    persons,
    personactivities,
    tasks
    )

from ..i18n import translatable_string as _
from . import expose


_a = availabilities.alias('a')
_d = duties.alias('d')
_p = persons.alias('p')
_t = tasks.alias('t')
_pa = personactivities.alias('pa')
_act = activities.alias('act')

# Subquery is needed to order the result alphabetically without
# using PG specific syntax, see
# http://www.postgresql.org/docs/current/static/sql-expressions.html#SYNTAX-AGGREGATES
# With SA 1.1 will be easier:
# http://docs.sqlalchemy.org/en/latest/dialects/postgresql.html#sqlalchemy.dialects.postgresql.aggregate_order_by

_ppa = (select([cast(_act.c.idactivity, Text).label('idactivity'),
                cast(_act.c.description, Text).label('description')],
               and_(_pa.c.idperson == _p.c.idperson,
                    _act.c.idactivity == _pa.c.idactivity))
        .order_by(_act.c.description)
        .correlate(_p)
        .alias('ppa'))

@view_config(route_name='persons', renderer='json')
@expose(select([_p.c.idperson,
                _p.c.lastname,
                _p.c.firstname,
                # text() is needed here, to workaround default normalization
                # performed by the Name type decorator, sigh...
                (_p.c.lastname + text("' '") + _p.c.firstname).label('FullName'),
                _p.c.phone,
                _p.c.mobile,
                _p.c.email,
                _p.c.birthdate,
                _p.c.role,
                select([func.string_agg(_ppa.c.idactivity, ',')])
                .as_scalar().label('idactivities'),
                select([func.string_agg(_ppa.c.description, ', ')])
                .as_scalar().label('Activities'),
                _p.c.note,
                literal_column("'*'", String).label('password'),
                select([func.count(_d.c.idduty)],
                       _d.c.idperson == _p.c.idperson)
                .as_scalar().label('Duties'),
                select([func.count(_a.c.idavailability)],
                       _a.c.idperson == _p.c.idperson)
                .as_scalar().label('Availabilities')]),
        metadata=dict(
            Activities=dict(
                label=_('Activities'),
                hint=_('Preferred activities of the person.'),
                width=140,
                lookup=dict(url='/data/preferred_activities',
                            sorters=[{'property': 'Persons', 'direction': "DESC"},
                                     {'property': 'description'}],
                            idField='idactivity',
                            displayField='description',
                            otherFields='Persons',
                            innerTpl='<div><tpl if="Persons"><strong></tpl>{description}<tpl if="Persons"> ({Persons})</strong></tpl></div>',
                ),
            ),
            Availabilities=dict(
                hidden=True,
                label=_('Availabilities'),
                hint=_('Number of availabilities of the person, in any edition.')
            ),
            Duties=dict(
                hidden=True,
                label=_('Duties'),
                hint=_('Number of duties assigned to the person, in any edition.')
            ),
            FullName=dict(
                flex=1,
                hint=_('Full name of the person'),
                label=_('Full name'),
            ),
            birthdate=dict(hidden=True),
            email=dict(width=140, vtype='email'),
            idactivities=dict(
                hidden=True,
                nullable=True,
                label=_('Activities'),
                hint=_('Preferred activities of the person.'),
            ),
            firstname=dict(hidden=True),
            lastname=dict(hidden=True),
            mobile=dict(hidden=True, vtype='phone'),
            note=dict(width=120),
            password=dict(
                hidden=True,
                hint=_('Login password of the user'),
                label=_('Password'),
                nullable=True,
                password=True,
                width=70,
            ),
            phone=dict(hidden=True, vtype='phone'),
            role=dict(hidden=True, width=140),
        ))
def _persons(request, results):
    return results


_t2 = tasks.alias('t2')

@view_config(route_name='available_persons', renderer='json')
@expose(select([_p.c.idperson,
                # text() is needed here, to workaround default normalization
                # performed by the Name type decorator, sigh...
                (_p.c.lastname + text("' '") + _p.c.firstname).label('fullname'),
                exists()
                .where(_pa.c.idperson == _p.c.idperson)
                .where(_t2.c.idtask == bindparam('idtask'))
                .where(_t2.c.idactivity == _pa.c.idactivity)
                .label('Preferred')])
        .order_by(desc('Preferred'), 'lastname', 'firstname'))
def _available_persons():
    request, params = (yield)
    if 'idtask' in params:
        idtask = int(params.pop('idtask'))
        bparams = params.setdefault('params', {})
        bparams['idtask'] = idtask
        conditions = (exists()
                      .where(_t.c.idtask == idtask)
                      .where(_a.c.date == _t.c.date)
                      .where(_a.c.idperson == _p.c.idperson)
                      .where(text("(COALESCE(a.starttime, '00:00'),"
                                  " COALESCE(a.endtime, '24:00'))"
                                  " OVERLAPS "
                                  "(t.starttime,"
                                  " COALESCE(t.endtime, '24:00'))")),)
        result = yield params, conditions
    else:
        bparams = params.setdefault('params', {})
        bparams['idtask'] = None
        result = yield params
    yield result
