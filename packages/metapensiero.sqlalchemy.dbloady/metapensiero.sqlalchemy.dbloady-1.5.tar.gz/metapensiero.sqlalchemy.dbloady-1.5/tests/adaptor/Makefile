# -*- coding: utf-8 -*-
# :Project:   metapensiero.sqlalchemy.dbloady -- Adaptor functional test
# :Created:   sab 09 gen 2016 10:53:46 CET
# :Author:    Lele Gaifax <lele@metapensiero.it>
# :License:   GNU General Public License version 3 or later
# :Copyright: Copyright (C) 2016 Lele Gaifax
#

PYTHON3 ?= python3.5

.PHONY: test
test: env
	env/bin/python test.py

env:
	$(PYTHON3) -m venv env
	env/bin/pip install --upgrade pip
	env/bin/pip install sqlalchemy
	env/bin/pip install -e ../.. .

.PHONY: clean
clean:
	rm -rf env __pycache__ testdbloady.egg-info
