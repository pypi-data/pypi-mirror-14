# -*- coding: utf-8 -*-
# :Project:   hurm -- Authentication related views
# :Created:   lun 01 feb 2016 20:55:40 CET
# :Author:    Lele Gaifax <lele@metapensiero.it>
# :License:   GNU General Public License version 3 or later
# :Copyright: © 2016 Lele Gaifax
#

import logging

from pyramid.events import NewRequest, subscriber
from pyramid.httpexceptions import HTTPUnauthorized
from pyramid.i18n import get_localizer
from pyramid.view import view_config

from sqlalchemy.orm import exc as saexc

from hurm.db.tables import password_manager
from hurm.db.entities import DBSession, Person

from ..i18n import translatable_string as _
from . import get_request_logger


logger = logging.getLogger(__name__)

NO_SUCH_USER = _('No such user!')
WRONG_PASSWORD = _('Wrong password')
MANDATORY_FIELD = _('Mandatory field')
MISSING_FIELDS = _('Missing fields')

ADMIN_ROLE = "HuRM Admin"
"Special role to identify HuRM admins, those having full access"


@subscriber(NewRequest)
def check_authorized_request(event,
                             authorized_paths={'/',
                                               '/auth/login',
                                               '/catalog',
                                               '/extjs-l10n',
                                               }):
    """Assert the request is authorized.

    This function gets hooked at the Pyramid's ``NewRequest`` event,
    so it will be executed at the start of each new request.

    If the user has been authenticated, or if she is requesting a
    static resource or one of the authentication views, then nothing
    happens. Otherwise an HTTPUnauthorized exception is raised.
    """

    request = event.request
    rpath = request.path
    sw = rpath.startswith

    # Authenticated user?
    session = request.session
    if 'user_id' in session:
        t = get_localizer(request).translate
        if sw('/data/persons') and not session['is_admin']:
            raise HTTPUnauthorized(t(_('Unauthorized access')))
        return

    # Anonymous authorized path or static resource?
    if rpath in authorized_paths or sw('/static/') or sw('/desktop/'):
        return

    if sw('/scripts') and request.registry.settings.get('desktop.debug', False):
        return

    t = get_localizer(request).translate
    raise HTTPUnauthorized(t(_('You must re-authenticate yourself')))


MODULES = (
    dict(classname='HuRM.module.Activities'),
    dict(classname='HuRM.module.ActivityPayloads'),
    dict(classname='HuRM.module.Availabilities'),
    dict(classname='HuRM.module.Duties'),
    dict(classname='HuRM.module.Editions',
         shortcut=dict(
             name=_('Editions'),
             iconCls='editions-icon',
             moduleId='editions-win')),
    dict(classname='HuRM.module.LocationDuties'),
    dict(classname='HuRM.module.Locations',
         shortcut=dict(
             name=_('Locations'),
             iconCls='locations-icon',
             moduleId='locations-win')),
    dict(classname='HuRM.module.PersonDuties'),
    dict(classname='HuRM.module.Persons',
         shortcut=dict(
             name=_('Persons'),
             iconCls='persons-icon',
             moduleId='persons-win')),
    dict(classname='HuRM.module.Tasks'),
    )


@view_config(route_name='login', renderer='json')
def _auth_user(request):
    t = get_localizer(request).translate

    data = request.params

    email = data.get('email', None)
    password = data.get('password', None)

    if email and password:
        sasess = DBSession()
        try:
            user = sasess.query(Person).filter_by(email=email).one()
        except saexc.NoResultFound:
            user = None

        if user is None or not password_manager.check(user.password, password):
            # Do not give hints about either fields
            get_request_logger(request, logger).warning('Unsuccessful login attempt for %s',
                                                        email)
            return {'success': False,
                    'message': t(NO_SUCH_USER),
                    'errors': {'email': t(NO_SUCH_USER),
                               'password': t(WRONG_PASSWORD)}}


        s = request.session
        is_admin = s['is_admin'] = ADMIN_ROLE in user.role
        user_id = s['user_id'] = user.idperson
        s['user_name'] = user.email
        s['user_fn'] = user.firstname
        s['user_ln'] = user.lastname
        fullname = s['user_fullname'] = t(user.fullname)

        get_request_logger(request, logger).info('New %ssession for %s',
                                                 "admin " if is_admin else "", fullname)

        def translate_name(cfg):
            copy = dict(cfg)
            copy['name'] = t(copy['name'])
            return copy

        user_modules = [m for m in MODULES
                        if is_admin or m['classname'] != 'HuRM.module.Persons']

        return {'success': True,
                'fullname': fullname,
                'is_admin': is_admin,
                'user_id': user_id,
                'modules': [m['classname'] for m in user_modules],
                'shortcuts': [translate_name(m['shortcut'])
                              for m in user_modules
                              if 'shortcut' in m],
                'quickstart': [translate_name(m['quickstart'])
                               for m in user_modules
                               if 'quickstart' in m]}
    else:
        errors = {}
        if not email:
            errors['email'] = t(MANDATORY_FIELD)
        if not password:
            errors['password'] = t(MANDATORY_FIELD)
        return {'success': False,
                'message': t(MISSING_FIELDS),
                'errors': errors}


@view_config(route_name='logout', renderer='json')
def _logout(request):
    get_request_logger(request, logger).info('Session terminated')
    request.session.invalidate()
    return {'success': True, 'message': 'Goodbye'}
