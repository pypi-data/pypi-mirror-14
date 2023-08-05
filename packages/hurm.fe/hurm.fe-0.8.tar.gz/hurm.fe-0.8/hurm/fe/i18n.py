# -*- coding: utf-8 -*-
# :Project:   hurm -- i18n related utilities
# :Created:   lun 01 feb 2016 20:21:13 CET
# :Author:    Lele Gaifax <lele@metapensiero.it>
# :License:   GNU General Public License version 3 or later
# :Copyright: © 2016 Lele Gaifax
#

from pyramid.i18n import TranslationStringFactory
from pyramid.events import NewRequest, subscriber


SERVER_DOMAIN = 'hurm-fe-server'
"The translation domain of the server side"

translatable_string = TranslationStringFactory(SERVER_DOMAIN)
"A function to make a translatable string."


available_languages = []

@subscriber(NewRequest)
def setAcceptedLanguagesLocale(event, _available_languages=available_languages):
    """Recognize the user preferred language.

    :param event: a Pyramid event
    :param _available_languages: the list of available languages (this is used
                                 as a cache, computed at the first call to this
                                 function)

    This function is automatically executed at each new request, and
    sets the ``_LOCALE_`` attribute of the request itself.
    """

    if not event.request.accept_language:
        return

    if not _available_languages:
        from pyramid.threadlocal import get_current_registry
        settings = get_current_registry().settings
        codes = settings.get('available_languages', 'en')
        # Put "en_US" before "en", otherwise the best_match()
        # mechanism does not work as expected
        _available_languages.extend(reversed(sorted(codes.split())))

    accepted = event.request.accept_language
    event.request._LOCALE_ = accepted.best_match(_available_languages, 'en')


def translator(request):
    """Return a function that translates a given string in the specified request

    :param request: either None or a Pyramid request instance

    This is an helper function that handles the case when the request
    does not exist, for example while testing::

      >>> t = translator(None)
      >>> t('$first $last', mapping=dict(first='Foo', last='Bar'))
      'Foo Bar'
    """

    if request is not None:
        def wrapper(*args, **kw):
            if 'domain' not in kw:
                kw['domain'] = SERVER_DOMAIN
            return request.localizer.translate(*args, **kw)
        return wrapper
    else:
        from string import Template
        return lambda s, **kw: Template(s).substitute(**kw.get('mapping', {}))


def pluralizer(request):
    """Return a function that translates a singular/plural strings in the specified request

    :param request: either None or a Pyramid request instance

    This is an helper function that handles the case when the request
    does not exist, for example while testing::

      >>> t = pluralizer(None)
      >>> count = 1
      >>> t('$count person', '$count persons', count, mapping=dict(count=count))
      '1 person'
    """

    if request is not None:
        def wrapper(*args, **kw):
            if 'domain' not in kw:
                kw['domain'] = SERVER_DOMAIN
            return request.localizer.pluralize(*args, **kw)
        return wrapper
    else:
        from string import Template
        return lambda s,p,n,**kw: Template(s if n==1 else p).substitute(**kw.get('mapping', {}))


def gettext(s, **kw):
    """Immediately translate the given string with current request locale

    :param s: either a string or a TranslationString instance
    """

    from pyramid.threadlocal import get_current_request

    if 'domain' not in kw:
        kw['domain'] = SERVER_DOMAIN

    request = get_current_request()
    if request is not None:
        return request.localizer.translate(s, **kw)
    else:
        from string import Template
        return Template(s).substitute(**kw.get('mapping', {}))


def ngettext(s, p, n, **kw):
    """Immediately translate the singular or plural form with current request locale

    :param s: either a string or a TranslationString instance with the
              singular form
    :param p: either a string or a TranslationString instance with the
              plural form
    :param n: an integer
    """

    from pyramid.threadlocal import get_current_request

    if 'domain' not in kw:
        kw['domain'] = SERVER_DOMAIN

    request = get_current_request()
    if request is not None:
        return request.localizer.pluralize(s, p, n, **kw)
    else:
        from string import Template
        return Template(s if n==1 else p).substitute(**kw.get('mapping', {}))
