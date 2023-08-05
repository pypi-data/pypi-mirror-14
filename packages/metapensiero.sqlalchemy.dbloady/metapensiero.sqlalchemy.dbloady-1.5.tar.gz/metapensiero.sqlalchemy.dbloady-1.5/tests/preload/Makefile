# -*- coding: utf-8 -*-
# :Project:   metapensiero.sqlalchemy.dbloady -- Pre/post scripts test
# :Created:   gio 14 gen 2016 11:28:44 CET
# :Author:    Lele Gaifax <lele@metapensiero.it>
# :License:   GNU General Public License version 3 or later
# :Copyright: Copyright (C) 2016 Lele Gaifax
#

PYTHON3 ?= python3.5

.PHONY: test
test: env testdbloadydb
	env/bin/dbloady -u sqlite:////tmp/testdbloady.sqlite \
	                -p preload.py -P postload.py data.yaml

env:
	$(PYTHON3) -m venv env
	env/bin/pip install --upgrade pip
	env/bin/pip install sqlalchemy
	env/bin/pip install -e ../.. .

.PHONY: testdbloadydb
testdbloadydb:
	rm -f /tmp/testdbloady.sqlite
	env/bin/python model.py

.PHONY: clean
clean:
	rm -f /tmp/testdbloady.sqlite
	rm -rf env __pycache__ testdbloady.egg-info
