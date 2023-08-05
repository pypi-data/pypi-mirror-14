# -*- coding: utf-8 -*-
# :Project:   hurm -- Abstract printouts
# :Created:   gio 11 feb 2016 17:14:12 CET
# :Author:    Lele Gaifax <lele@metapensiero.it>
# :License:   GNU General Public License version 3 or later
# :Copyright: © 2016 Lele Gaifax
#

from copy import copy
from datetime import datetime
import logging
from os import unlink
from tempfile import mktemp

from pyramid.httpexceptions import HTTPBadRequest, HTTPInternalServerError


logger = logging.getLogger(__name__)

BASE_FONT_NAME = 'DejaVuSans'

from reportlab import rl_settings
rl_settings.canvas_basefontname = BASE_FONT_NAME

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont, TTFError

try:
    for variant in ('', '-Bold', '-Oblique', '-BoldOblique'):
        pdfmetrics.registerFont(TTFont(BASE_FONT_NAME + variant,
                                       BASE_FONT_NAME + "%s.ttf" % variant))
except TTFError: # pragma: no cover
    from reportlab import rl_config

    logger.error('Could not find the "%s" font, using PDF default fonts', BASE_FONT_NAME)

    BASE_FONT_NAME = 'Times-Roman'
    rl_config.canvas_basefontname = rl_settings.canvas_basefontname = BASE_FONT_NAME
    BOLD_ITALIC_FONT_NAME = 'Times-BoldItalic'
    ITALIC_FONT_NAME = 'Times-Italic'
else:
    BOLD_ITALIC_FONT_NAME = BASE_FONT_NAME + '-BoldOblique'
    ITALIC_FONT_NAME = BASE_FONT_NAME + '-Oblique'

    from reportlab.lib.fonts import addMapping
    addMapping(BASE_FONT_NAME, 0, 0, BASE_FONT_NAME)
    addMapping(BASE_FONT_NAME, 0, 1, BASE_FONT_NAME + '-Oblique')
    addMapping(BASE_FONT_NAME, 1, 0, BASE_FONT_NAME + '-Bold')
    addMapping(BASE_FONT_NAME, 1, 1, BASE_FONT_NAME + '-BoldOblique')

from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import (
    BaseDocTemplate,
    Frame,
    FrameBreak,
    NextPageTemplate,
    PageTemplate,
    Paragraph,
    )

from hurm.db.entities import Edition

from ..i18n import gettext, pluralizer, translatable_string as _, translator



base_style = getSampleStyleSheet()
"The base style used to build the document"

title_style = copy(base_style['Title'])
"The style used for the title of the document"

title_style.fontSize = 28
title_style.leading = title_style.fontSize*1.1

subtitle_style = copy(base_style['Heading1'])
"The style used for the subtitle of the document"

subtitle_style.fontSize = 20
subtitle_style.leading = subtitle_style.fontSize*1.1
subtitle_style.alignment = TA_CENTER
subtitle_style.fontName = ITALIC_FONT_NAME

heading_style = copy(base_style['Heading2'])
"The style used for the heading paragraphs of the document"

heading_style.alignment = TA_CENTER

normal_style = copy(base_style['Normal'])
"The style used for most of the paragraphs of the document"

normal_style.fontSize = 14
normal_style.leading = normal_style.fontSize*1.1

caption_style = copy(base_style['Italic'])
"The style used for the caption of the table's columns"

caption_style.fontSize = 9
caption_style.leading = caption_style.fontSize*1.1


def reduce_fontsize_to_fit_width(text, maxwidth, *styles):
    """Reduce the font size of the given styles to fit a max width.

    :param text: the string of text
    :param maxwidth: maximum width that can be used
    :param styles: the list of styles that should be adapted
    :returns: a list of (copies of) the styles with the adapted font size
    """

    from reportlab.pdfbase.pdfmetrics import stringWidth

    copies = styles
    mainstyle = styles[0]

    while stringWidth(text, mainstyle.fontName, mainstyle.fontSize) > maxwidth:
        if mainstyle is styles[0]: # pragma: no cover
            copies = [copy(style) for style in styles]
            mainstyle = copies[0]

        for style in copies:
            style.fontSize -= 1
            style.leading = style.fontSize * 1.1

    return copies


class BasicPrintout(object):
    """Abstract base class used to implement the printouts.

    This class implements the logic used by most printouts, producing a PDF document in the
    `output` filename.

    The document has a front page with an header, a body splitted into `columns` frames and
    a footer. Succeding pages do not have the header frame.
    """

    leftMargin = 1*cm
    "The width of the left margin, by default 1cm"

    rightMargin = 1*cm
    "The width of the right margin, by default 1cm"

    topMargin = 1*cm
    "The width of the top margin, by default 1cm"

    bottomMargin = 1*cm
    "The width of the bottom margin, by default 1cm"

    pagesize = A4
    "The page size, by default A4 in portrait orientation"

    @classmethod
    def getArgumentsFromRequest(klass, session, request):
        """Extract needed arguments for the constructor from the request.

        :param session: the SQLAlchemy session
        :param request: the Pyramid request instance
        :rtype: a sequence of arguments, the first one being a ``translate`` function
        """

        return [translator(request), pluralizer(request)]

    def __init__(self, output, translate, pluralize, columns=1):
        """Initialize the instance.

        :param output: a filename where the PDF will be written
        :param columns: number of columns
        """

        self.output = output
        self.translate = translate
        self.pluralize = pluralize
        self.columns = columns
        self.timestamp = datetime.now()

    @property
    def cache_max_age(self):
        "Compute the cache control max age, in seconds."

        return 0

    def createDocument(self):
        """Create the base Platypus document."""

        from pkg_resources import get_distribution

        version = get_distribution('hurm.fe').version

        doc = self.doc = BaseDocTemplate(
            self.output, pagesize=self.pagesize, showBoundary=0,
            leftMargin=self.leftMargin, rightMargin=self.rightMargin,
            topMargin=self.topMargin, bottomMargin=self.bottomMargin,
            author='HuRM %s' % version,
            creator="https://bitbucket.org/lele/hurm",
            subject=self.__class__.__name__,
            title='%s: %s' % (self.getTitle(), self.getSubTitle()))

        title_height = 3.0*cm
        title_width = doc.width
        title_frame = Frame(doc.leftMargin, doc.height + doc.bottomMargin - title_height,
                            title_width, title_height)
        self.title_width = title_width

        fp_frames = [title_frame]
        lp_frames = []

        fwidth = doc.width / self.columns
        fheight = doc.height

        bmargin = doc.bottomMargin
        for f in range(self.columns):
            lmargin = doc.leftMargin + f*fwidth
            fp_frames.append(Frame(lmargin, bmargin, fwidth, fheight-title_height,
                                   showBoundary=0))
            lp_frames.append(Frame(lmargin, bmargin, fwidth, fheight, showBoundary=0))

        templates = [PageTemplate(frames=fp_frames,
                                  id="firstPage",
                                  onPage=self.decoratePage),
                     PageTemplate(frames=lp_frames,
                                  id="laterPages",
                                  onPage=self.decoratePage)]
        doc.addPageTemplates(templates)

    def getLeftHeader(self):
        "The top left text."

        raise NotImplementedError("%s should implement this method!"
                                  % self.__class__)

    def getRightHeader(self):
        "The top right text."

        raise NotImplementedError("%s should implement this method!"
                                  % self.__class__)

    def getCenterHeader(self):
        "The top center text."
        # pragma: no cover
        raise NotImplementedError("%s should implement this method!"
                                  % self.__class__)

    def getTitle(self):
        "The title of the document."

        raise NotImplementedError("%s should implement this method!"
                                  % self.__class__)

    def getSubTitle(self):
        "The subtitle of the document."

        raise NotImplementedError("%s should implement this method!"
                                  % self.__class__)

    def getLeftFooter(self):
        "The bottom left text, SoL description and version by default."

        from pkg_resources import get_distribution

        dist = get_distribution('hurm.fe')
        description = dist.project_name
        version = dist.version

        return '%s %s %s' % (description, gettext('version'), version)

    def getRightFooter(self):
        "The bottom right text, current time by default."

        # TRANSLATORS: this is a Python strftime() format, see
        # http://docs.python.org/3/library/time.html#time.strftime
        return self.timestamp.strftime(str(gettext('%m-%d-%Y %I:%M %p')))

    def getCenterFooter(self):
        "The bottom center text, current page number by default."

        if self.doc.page > 1:
            return self.getSubTitle() + ', ' + gettext('page %d') % self.doc.page
        else:
            return gettext('page %d') % self.doc.page

    def decoratePage(self, canvas, doc):
        "Add standard decorations to the current page."

        canvas.saveState()
        canvas.setFont(BASE_FONT_NAME, 6)
        w, h = doc.pagesize
        hh = doc.bottomMargin + doc.height + doc.topMargin/2
        hl = doc.leftMargin
        hc = doc.leftMargin + doc.width/2.0
        hr = doc.leftMargin + doc.width
        canvas.drawString(hl, hh, self.getLeftHeader())
        canvas.drawCentredString(hc, hh, self.getCenterHeader())
        canvas.drawRightString(hr, hh, self.getRightHeader())
        fh = doc.bottomMargin/2
        canvas.drawString(hl, fh, self.getLeftFooter())
        canvas.drawCentredString(hc, fh, self.getCenterFooter())
        canvas.drawRightString(hr, fh, self.getRightFooter())
        canvas.restoreState()

    def execute(self, request):
        """Create and build the document.

        :param request: the Pyramid request instance
        """

        self.createDocument()
        self.doc.build(list(self.getElements()))

    def getElements(self):
        "Return a list or an iterator of all the elements."

        raise NotImplementedError("%s should implement this method!"
                                  % self.__class__)


class ParameterError(ValueError):
    pass


class BasicEditionPrintout(BasicPrintout):
    @classmethod
    def getArgumentsFromRequest(klass, session, request):
        args = super().getArgumentsFromRequest(session, request)
        t = args[0]
        try:
            idedition = int(request.matchdict['idedition'])
        except KeyError:
            raise ParameterError(t(_('Missing argument: $name',
                                     mapping=dict(name='idedition'))))

        edition = session.query(Edition).get(idedition)
        if edition is None:
            raise ParameterError(t(_('No edition with id $id',
                                     mapping=dict(id=str(idedition)))))

        args.append(edition)
        return args

    def __init__(self, output, translate, pluralize, edition):
        super().__init__(output, translate, pluralize)
        self.edition = edition

    def getLeftHeader(self):
        "Return edition's description."

        return self.edition.description

    def getRightHeader(self):
        "Return edition's period."

        # TRANSLATORS: this is a Python strftime() format, see
        # http://docs.python.org/3/library/time.html#time.strftime
        dateformat = gettext('%m-%d-%Y')

        return "%s — %s" % (self.edition.startdate.strftime(dateformat),
                            self.edition.enddate.strftime(dateformat))

    def getElements(self):
        "Yield basic elements for the title frame in the first page."

        title = self.getTitle()
        tstyle, ststyle = reduce_fontsize_to_fit_width(title, self.title_width - 1*cm,
                                                       title_style, subtitle_style)

        yield Paragraph(title, tstyle)
        yield Paragraph(self.getSubTitle(), ststyle)
        yield FrameBreak()
        yield NextPageTemplate('laterPages')


def create_pdf(session, request, maker):
    try:
        output = mktemp(prefix='hurm')
        args = maker.getArgumentsFromRequest(session, request)
        builder = maker(output, *args)
        try:
            builder.execute(request)

            f = open(output, 'rb')
            content = f.read()
            f.close()
        finally:
            try:
                unlink(output)
            except OSError:
                pass

        response = request.response
        response.content_type = 'application/pdf'
        cdisp = 'attachment; filename=%s.pdf' % maker.__name__
        response.content_disposition = cdisp
        response.body = content
        response.cache_control.public = True
        response.cache_control.max_age = builder.cache_max_age
        return response
    except ParameterError as e:
        logger.error("Couldn't create report %s: %s", maker.__name__, e)
        raise HTTPBadRequest(str(e))
    except Exception as e:
        logger.critical("Couldn't create report %s: %s", maker.__name__, e, exc_info=True)
        raise HTTPInternalServerError(str(e))


def render_timedelta(tdelta):
    """Convert a datetime.timedelta to a compact string.

    Examples::

      >>> import datetime
      >>> td = datetime.timedelta(hours=5, minutes=30)
      >>> print render_timedelta(td)
      5:30
      >>> td = datetime.timedelta(days=1, hours=5, minutes=45)
      >>> print render_timedelta(td)
      29:45
      >>> td = datetime.timedelta(days=-1, hours=4, minutes=15)
      >>> print render_timedelta(td)
      -19:45
      >>> print render_timedelta(None)
      0:00
    """

    if not tdelta:
        return '0:00'

    days = tdelta.days
    secs = tdelta.seconds

    if days<0:
        minus = "-"
        secs = 24*60*60 - secs
        days = -days - 1
    else:
        minus = ""

    secs += days * 24*60*60
    secs /= 60
    mm = secs % 60
    secs /= 60
    hh = secs

    return "%s%d:%02d" % (minus, hh, mm)
