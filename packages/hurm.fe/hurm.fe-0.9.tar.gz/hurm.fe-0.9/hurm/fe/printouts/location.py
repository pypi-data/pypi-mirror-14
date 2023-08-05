# -*- coding: utf-8 -*-
# :Project:   hurm -- Location related printouts
# :Created:   sab 13 feb 2016 19:48:24 CET
# :Author:    Lele Gaifax <lele@metapensiero.it>
# :License:   GNU General Public License version 3 or later
# :Copyright: © 2016 Lele Gaifax
#

from itertools import groupby

from pyramid.view import view_config

from reportlab.lib.pagesizes import A4, landscape
from reportlab.platypus import TableStyle
from reportlab.platypus.tables import Table

from sqlalchemy.orm import object_session

from hurm.db.entities import Duty, Location, Task

from .. import DBSession
from ..i18n import translatable_string as _
from . import BasicEditionPrintout, ParameterError, create_pdf
from .calendar import CellContent, calendar_header, calendar_row


def _duties_to_cells(translate, duties):
    duties = list(duties)

    timings = []
    for duty in duties:
        t = duty.starttime
        if t not in timings:
            timings.append(t)
        t = duty.endtime
        if t not in timings:
            timings.append(t)

    timings.sort()

    cells = []
    for i, t in enumerate(timings[:-1]):
        cells.append(CellContent(t, timings[i+1], []))

    for cell in cells:
        cduties = [duty for duty in duties
                   if ((cell.starttime <= duty.starttime < cell.endtime)
                       or
                       (duty.starttime < cell.endtime <= duty.endtime))]
        if cell.endtime.hour - cell.starttime.hour > 1:
            persons = (translate(duty.person.fullname) for duty in cduties)
        else:
            persons = (translate(duty.person.abbreviated_fullname) for duty in cduties)
        cell.content.extend(sorted(persons))

    cells = [cell for cell in cells if cell.content]

    return cells


def duties_table(translate, document, location, edition):
    # TRANSLATORS: this is a Python strftime() format, see
    # http://docs.python.org/3/library/time.html#time.strftime
    datefmt = translate(_('%m-%d-%Y'))

    # TRANSLATORS: this is the Python strftime() template used to format times,
    # see http://docs.python.org/3/library/time.html#time.strftime
    timefmt = translate(_('%I:%M %p'))

    # TRANSLATORS: this is the strftime() template used to format hours,
    # see http://docs.python.org/3/library/time.html#time.strftime
    hourfmt = translate(_('%I %p'))

    session = object_session(location)
    allduties = session.query(Duty).join(Task) \
                .filter(Task.idlocation == location.idlocation) \
                .filter(Task.idedition == edition.idedition) \
                .order_by(Task.date, Duty.starttime) \
                .all()
    if allduties:
        min_time = min(duty.starttime for duty in allduties)
        if min_time.minute != 0:
            min_time = min_time.replace(minute=0)
        max_time = max(duty.endtime for duty in allduties)
        if max_time.minute != 0:
            max_time = max_time.replace(hour=max_time.hour+1, minute=0)

        cells, styles = calendar_header(hourfmt, font_size=4,
                                        min_time=min_time, max_time=max_time)
    else:
        cells, styles = calendar_header(hourfmt, font_size=4)

    rows = [cells]
    rownumber = 1

    task_date = lambda d: d.task.date

    for date, duties in groupby(allduties, task_date):
        ccells = _duties_to_cells(translate, duties)
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


class LocationDuties(BasicEditionPrintout):
    pagesize = landscape(A4)

    @classmethod
    def getArgumentsFromRequest(klass, session, request):
        args = super().getArgumentsFromRequest(session, request)

        t = args[0]

        try:
            idlocation = int(request.matchdict['idlocation'])
        except KeyError:
            raise ParameterError(t(_('Missing argument: $name',
                                     mapping=dict(name='idlocation'))))
        location = session.query(Location).get(idlocation)
        if location is None:
            raise ParameterError(t(_('No location with id $id',
                                 mapping=dict(id=str(idlocation)))))

        args.append(location)

        return args

    def __init__(self, output, translate, pluralize, edition, location):
        super().__init__(output, translate, pluralize, edition)
        self.location = location

    def getCenterHeader(self):
        return self.translate(_('Duties calendar for $location',
                                mapping=dict(location=self.location.description)))

    def getTitle(self):
        return self.location.description

    def getSubTitle(self):
        session = object_session(self.location)
        count = session.query(Duty).join(Task) \
                .filter(Task.idedition == self.edition.idedition) \
                .count()
        ngettext = self.pluralize
        return ngettext('$count duty', '$count duties', count,
                        mapping=dict(count=count))

    def getElements(self):
        yield from super().getElements()
        yield duties_table(self.translate, self.doc, self.location, self.edition)


@view_config(route_name='pdf_location_duties')
def _location_duties(request):
    return create_pdf(DBSession(), request, LocationDuties)
