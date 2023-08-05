# -*- coding: utf-8 -*-
# :Project:   hurm -- Utility functions related to calendar printouts
# :Created:   sab 13 feb 2016 19:36:10 CET
# :Author:    Lele Gaifax <lele@metapensiero.it>
# :License:   GNU General Public License version 3 or later
# :Copyright: © 2016 Lele Gaifax
#

from collections import namedtuple
from datetime import date, datetime, time, timedelta

from reportlab.lib import colors

from ..i18n import translatable_string as _


START_TIME = time(8, 0)
END_TIME = time(23, 59)
MINUTES_PER_CELL = 5
RESOLUTION = timedelta(minutes=MINUTES_PER_CELL)
COLS_PER_HOUR = 60 // MINUTES_PER_CELL


def calendar_header(hourfmt, font_size=6, min_time=START_TIME, max_time=END_TIME):
    """Generate the table's header row and the basic styles for a calendar printout."""

    dtcurr = datetime.combine(date.today(), min_time)
    dtstop = datetime.combine(date.today(), max_time)
    cells = [_('Date')]
    styles = [
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('SIZE', (0, 1), (0, -1), 8),
        ('SIZE', (1, 1), (-1, -1), font_size),
        ('TOPPADDING', (1, 1), (-1, -1), 2),
        ('RIGHTPADDING', (1, 1), (-1, -1), 2),
        ('BOTTOMPADDING', (1, 1), (-1, -1), 2),
        ('LEFTPADDING', (1, 1), (-1, -1), 2),
    ]
    cellnumber = 1

    while dtcurr < dtstop:
        currtime = dtcurr.time()
        if currtime.minute == 0:
            cells.append(currtime.strftime(hourfmt))
            styles.append(('SPAN', (cellnumber, 0), (cellnumber+COLS_PER_HOUR-1, 0)))
        else:
            cells.append('')
        cellnumber += 1
        dtcurr += RESOLUTION

    return cells, styles


def _generate_cells(rownumber, firstcellnumber, content, start, stop,
                    min_time=START_TIME, max_time=END_TIME):
    "Generate row cells and styles in the given time span."

    dtcurr = datetime.combine(date.today(), start or min_time)
    dtstop = datetime.combine(date.today(), stop or max_time)
    cells = []
    ncells = 0
    styles = []

    if content:
        currcontent = '\n'.join(content)
    else:
        currcontent = ''

    while dtcurr < dtstop:
        cells.append(currcontent)
        if currcontent:
            currcontent = ''
        ncells += 1
        dtcurr += RESOLUTION

    if content and ncells > 1:
        styles.append(('BOX',
                       (firstcellnumber, rownumber),
                       (firstcellnumber+ncells-1, rownumber), 1, colors.black))
        styles.append(('SPAN',
                       (firstcellnumber, rownumber),
                       (firstcellnumber+ncells-1, rownumber)))

    return cells, styles, dtstop.time()


CellContent = namedtuple('CellContent', 'starttime, endtime, content')


def calendar_row(rownumber, cells, min_time=START_TIME, max_time=END_TIME):
    """Generate the table's row and styles for duties of a particular day."""

    lt = None
    rowcells = []
    rowstyles = []
    cellnumber = 1

    for cell in cells:
        st = cell.starttime
        et = cell.endtime

        cells, styles, lt = _generate_cells(rownumber, cellnumber, None,
                                            lt, st, min_time, max_time)
        rowcells.extend(cells)
        rowstyles.extend(styles)
        cellnumber += len(cells)

        cells, styles, lt = _generate_cells(rownumber, cellnumber, cell.content,
                                            lt, et, min_time, max_time)
        rowcells.extend(cells)
        rowstyles.extend(styles)
        cellnumber += len(cells)

    cells, styles, _ = _generate_cells(rownumber, cellnumber, None, lt, None,
                                       min_time, max_time)
    rowcells.extend(cells)
    rowstyles.extend(styles)

    return rowcells, rowstyles
