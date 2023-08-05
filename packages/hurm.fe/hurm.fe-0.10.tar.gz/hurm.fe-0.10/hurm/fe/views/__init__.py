# -*- coding: utf-8 -*-
# :Project:   hurm -- Views declaration
# :Created:   lun 01 feb 2016 20:54:33 CET
# :Author:    Lele Gaifax <lele@metapensiero.it>
# :License:   GNU General Public License version 3 or later
# :Copyright: © 2016 Lele Gaifax
#

import logging

from metapensiero.sqlalchemy.proxy.pyramid import expose

from hurm.db import logger as changes_logger
from hurm.db.entities import DBSession
from hurm.db.utils import save_changes


class LoggerAdapter(logging.LoggerAdapter):
    "Add username and remote IP to the logged message"

    def process(self, msg, kwargs):
        extra = self.extra
        msg = "[%s@%s] " % (extra['user'], extra['ip']) + msg
        return msg, kwargs


def get_request_logger(request, logger):
    "Get a specialized `logger` for a Pyramid `request`"

    extra = dict(
        ip=request.client_addr,
        user=request.session.get('user_fullname') or 'anonymous')

    return LoggerAdapter(logger, extra)


def logged_save_changes(sasess, request, modified, deleted):
    "Save changes logging changes with user information"

    return save_changes(sasess, request, modified, deleted,
                        clogger=get_request_logger(request, changes_logger))


# Configure the `expose` decorator
expose.create_session = staticmethod(lambda request: DBSession())
expose.save_changes = staticmethod(logged_save_changes)
