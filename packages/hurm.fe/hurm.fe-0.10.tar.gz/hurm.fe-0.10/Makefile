# -*- coding: utf-8 -*-
# :Project:   hurm -- Frontend main makefile
# :Created:   lun 01 feb 2016 19:46:33 CET
# :Author:    Lele Gaifax <lele@metapensiero.it>
# :License:   GNU General Public License version 3 or later
# :Copyright: © 2016 Lele Gaifax
#

PYTHON ?= $(BINDIR)python
PSERVE := $(BINDIR)pserve
HURMSRC := $(CURDIR)/hurm/fe
PYTEST := $(BINDIR)py.test --cov=hurm/fe --cov-report=term-missing

.PHONY: run-development
run-development:
	$(PSERVE) development.ini

.PHONY: run-production
run-production:
	$(PSERVE) production.ini

.PHONY: test
test::
	$(PYTEST) tests

include Makefile.i18n
include Makefile.production
include Makefile.release
