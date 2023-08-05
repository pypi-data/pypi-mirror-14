# -*- coding: utf-8 -*-
# :Project:   hurm -- Edition related printouts
# :Created:   dom 14 feb 2016 19:27:54 CET
# :Author:    Lele Gaifax <lele@metapensiero.it>
# :License:   GNU General Public License version 3 or later
# :Copyright: © 2016 Lele Gaifax
#

from datetime import datetime, timedelta
from itertools import groupby

from pyramid.view import view_config

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.units import cm
from reportlab.platypus import CondPageBreak, KeepTogether, Paragraph, Spacer

from reportlab.platypus import TableStyle
from reportlab.platypus.tables import Table

from sqlalchemy.orm import object_session

from hurm.db.entities import Location, Task

from .. import DBSession
from ..i18n import translatable_string as _
from . import BasicEditionPrintout, create_pdf, render_timedelta, subtitle_style


class ByLocationDuties(BasicEditionPrintout):
    pagesize = landscape(A4)

    def __init__(self, output, translate, pluralize, edition):
        super().__init__(output, translate, pluralize, edition)
        session = object_session(edition)
        self.locations = session.query(Location).join(Task) \
                         .filter(Task.idedition == edition.idedition) \
                         .order_by(Location.description) \
                         .all()

    def getCenterHeader(self):
        return self.getTitle()

    def getTitle(self):
        return self.translate(_('Duties calendar by location'))

    def getSubTitle(self):
        ngettext = self.pluralize
        count = len(self.locations)
        return ngettext('$count location', '$count locations', count,
                        mapping=dict(count=count))

    def getElements(self):
        from .location import duties_table

        yield from super().getElements()

        for location in self.locations:
            yield Spacer(0, 10)
            yield KeepTogether([Paragraph(location.description, subtitle_style),
                                Spacer(0, 5),
                                duties_table(self.translate, self.doc, location, self.edition)])


@view_config(route_name='pdf_by_location_duties')
def _by_location_duties(request):
    return create_pdf(DBSession(), request, ByLocationDuties)


class ByPersonDuties(BasicEditionPrintout):
    pagesize = landscape(A4)

    def __init__(self, output, translate, pluralize, edition):
        super().__init__(output, translate, pluralize, edition)
        persons = set(duty.person for task in edition.tasks for duty in task.duties)
        self.persons = sorted(persons, key=lambda p: self.translate(p.fullname))

    def getCenterHeader(self):
        return self.getTitle()

    def getTitle(self):
        return self.translate(_('Duties calendar by person'))

    def getSubTitle(self):
        ngettext = self.pluralize
        count = len(self.persons)
        return ngettext('$count person', '$count persons', count,
                        mapping=dict(count=count))

    def getElements(self):
        from .person import duties_table

        yield from super().getElements()

        for person in self.persons:
            yield Spacer(0, 10)
            yield KeepTogether([Paragraph(self.translate(person.fullname), subtitle_style),
                                Spacer(0, 5),
                                duties_table(self.translate, self.doc, person)])


@view_config(route_name='pdf_by_person_duties')
def _by_person_duties(request):
    return create_pdf(DBSession(), request, ByPersonDuties)


class PersonsDutiesSummary(BasicEditionPrintout):
    def __init__(self, output, translate, pluralize, edition):
        from ..views.duties import query

        super().__init__(output, translate, pluralize, edition)
        conn = object_session(edition).connection()
        self.persons = conn.execute(query.order_by("Person", "date", "starttime")).fetchall()

    def getCenterHeader(self):
        return self.getTitle()

    def getTitle(self):
        return self.translate(_('Persons duties summary'))

    def getSubTitle(self):
        ngettext = self.pluralize
        count = len(set(p.Person for p in self.persons))
        return ngettext('$count person', '$count persons', count,
                        mapping=dict(count=count))

    def getElements(self):
        yield from super().getElements()

        # TRANSLATORS: this is a Python strftime() format, see
        # http://docs.python.org/3/library/time.html#time.strftime
        datefmt = self.translate(_('%m-%d-%Y'))

        # TRANSLATORS: this is the Python strftime() template used to format times,
        # see http://docs.python.org/3/library/time.html#time.strftime
        timefmt = self.translate(_('%I:%M %p'))

        combine = datetime.combine

        for person, dates in groupby(self.persons, lambda p: p.Person):
            styles = [
                ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
                ('ALIGN', (0, 0), (1, -1), 'CENTER'),
                ('SIZE', (0, 0), (-1, 0), 14),
            ]

            rows = [
                [ self.translate(s) for s in (_('Date'), _('Start'), _('End'),
                                              _('Location'), _('Activity')) ],
            ]

            pdate = None
            dtime = timedelta(0)
            rownum = 1

            for d in dates:
                if pdate is not None and pdate != d.date:
                    rows.append([self.translate(_('Total time')), render_timedelta(dtime),
                                 '', '', ''])
                    rows.append([''] * len(rows[0]))
                    styles.append(('LINEABOVE', (1, rownum), (2, rownum), 0.25, colors.black))
                    styles.append(('SPAN', (1, rownum), (2, rownum)))
                    styles.append(('NOSPLIT', (0, rownum-1), (-1, (rownum+1))))
                    dtime = timedelta(0)
                    rownum += 2

                rows.append([d.date.strftime(datefmt) if pdate != d.date else '"',
                             d.starttime.strftime(timefmt),
                             d.endtime.strftime(timefmt),
                             d.Location,
                             d.Activity])
                rownum += 1

                dtime += (combine(d.date, d.endtime) - combine(d.date, d.starttime))
                pdate = d.date

            rows.append(['', render_timedelta(dtime), '', '', ''])
            rows.append([''] * len(rows[0]))
            styles.append(('LINEABOVE', (1, rownum), (2, rownum), 0.25, colors.black))
            styles.append(('SPAN', (1, rownum), (2, rownum)))
            styles.append(('NOSPLIT', (0, rownum-1), (-1, (rownum+1))))

            yield CondPageBreak(4*cm)
            yield Spacer(0, 15)
            yield Paragraph(person, subtitle_style)
            yield Spacer(0, 5)
            yield Table(rows, style=TableStyle(styles), repeatRows=1)


@view_config(route_name='pdf_persons_duties_summary')
def _persons_duties_summary(request):
    return create_pdf(DBSession(), request, PersonsDutiesSummary)
