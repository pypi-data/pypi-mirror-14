# -*- coding: utf-8 -*-
# :Project:   hurm -- Person related printouts
# :Created:   gio 11 feb 2016 17:33:12 CET
# :Author:    Lele Gaifax <lele@metapensiero.it>
# :License:   GNU General Public License version 3 or later
# :Copyright: © 2016 Lele Gaifax
#

from itertools import groupby

from pyramid.view import view_config

from reportlab.lib.pagesizes import A4, landscape
from reportlab.platypus import TableStyle
from reportlab.platypus.tables import Table

from hurm.db.entities import Person

from .. import DBSession
from ..i18n import translatable_string as _
from . import BasicEditionPrintout, ParameterError, create_pdf
from .calendar import CellContent, calendar_header, calendar_row


def duties_table(translate, document, person):
    # TRANSLATORS: this is a Python strftime() format, see
    # http://docs.python.org/3/library/time.html#time.strftime
    datefmt = translate(_('%m-%d-%Y'))

    # TRANSLATORS: this is the Python strftime() template used to format times,
    # see http://docs.python.org/3/library/time.html#time.strftime
    timefmt = translate(_('%I:%M %p'))

    # TRANSLATORS: this is the strftime() template used to format hours,
    # see http://docs.python.org/3/library/time.html#time.strftime
    hourfmt = translate(_('%I %p'))

    min_time = min(duty.starttime for duty in person.duties)
    if min_time.minute != 0:
        min_time = min_time.replace(minute=0)
    max_time = max(duty.endtime for duty in person.duties)
    if max_time.minute != 0:
        max_time = max_time.replace(hour=max_time.hour+1, minute=0)

    cells, styles = calendar_header(hourfmt, min_time=min_time, max_time=max_time)
    rows = [cells]
    rownumber = 1

    for date, duties in groupby(person.duties, lambda d: d.task.date):
        ccells = [CellContent(duty.starttime, duty.endtime,
                              [duty.task.activity.description,
                               duty.task.location.description])
                 for duty in duties]
        for cell in ccells:
            if (cell.endtime.hour - cell.starttime.hour) > 1:
                cell.content.insert(0,
                                    cell.starttime.strftime(timefmt)
                                    + " — "
                                    + cell.endtime.strftime(timefmt))
            else:
                cell.content.insert(0, cell.starttime.strftime(timefmt))
                cell.content.insert(1, cell.endtime.strftime(timefmt))
        cells, rowstyles = calendar_row(rownumber, ccells,
                                        min_time=min_time, max_time=max_time)
        rows.append([date.strftime(datefmt)] + cells)
        styles.extend(rowstyles)
        rownumber += 1

    ntimecells = len(rows[0]) - 1
    cwidths = [None] + [(document.width - 40) // ntimecells] * ntimecells
    return Table(rows, cwidths, style=TableStyle(styles), repeatRows=1)


class PersonDuties(BasicEditionPrintout):
    pagesize = landscape(A4)

    @classmethod
    def getArgumentsFromRequest(klass, session, request):
        args = super().getArgumentsFromRequest(session, request)

        t = args[0]

        try:
            idperson = int(request.matchdict['idperson'])
        except KeyError:
            raise ParameterError(t(_('Missing argument: $name',
                                     mapping=dict(name='idperson'))))
        person = session.query(Person).get(idperson)
        if person is None:
            raise ParameterError(t(_('No person with id $id',
                                 mapping=dict(id=str(idperson)))))

        args.append(person)

        return args

    def __init__(self, output, translate, pluralize, edition, person):
        super().__init__(output, translate, pluralize, edition)
        self.person = person

    def getCenterHeader(self):
        fullname = self.translate(self.person.fullname)
        return self.translate(_('Duties calendar for $person',
                                mapping=dict(person=fullname)))

    def getTitle(self):
        return self.translate(self.person.fullname)

    def getSubTitle(self):
        count = len(self.person.duties)
        ngettext = self.pluralize
        return ngettext('$count duty', '$count duties', count,
                        mapping=dict(count=count))

    def getElements(self):
        yield from super().getElements()
        yield duties_table(self.translate, self.doc, self.person)


@view_config(route_name='pdf_person_duties')
def _person_duties(request):
    return create_pdf(DBSession(), request, PersonDuties)
