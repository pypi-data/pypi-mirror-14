# -*- coding: utf-8 -*-
# :Project:   metapensiero.sqlalchemy.dbloady -- YAML based data loader
# :Created:   ven  1 gen 2016, 16.19.54, CET
# :Author:    Lele Gaifax <lele@metapensiero.it>
# :License:   GNU General Public License version 3 or later
# :Copyright: Copyright (C) 2016 Lele Gaifax
#

all: help

help::
	@printf "Development targets\n"
	@printf "===================\n\n"

help::
	@printf "test\n\tRun basic functional test (needs PostgreSQL)\n"

.PHONY: test
test:
	$(MAKE) -C tests/adaptor test
	$(MAKE) -C tests/fields test
	$(MAKE) -C tests/hstore test
	$(MAKE) -C tests/preload test
	$(MAKE) -C tests/dump test

.PHONY: clean
clean:
	$(MAKE) -C tests/adaptor clean
	$(MAKE) -C tests/fields clean
	$(MAKE) -C tests/hstore clean
	$(MAKE) -C tests/preload clean
	$(MAKE) -C tests/dump clean

include Makefile.release
