# -*- coding: utf-8 -*-
# :Project:   metapensiero.sqlalchemy.dbloady -- HSTORE functional test
# :Created:   gio 22 ott 2015 18:15:12 CEST
# :Author:    Lele Gaifax <lele@metapensiero.it>
# :License:   GNU General Public License version 3 or later
# :Copyright: Copyright (C) 2015, 2016 Lele Gaifax
#

PYTHON3 ?= python3.5

.PHONY: test
test: env testdbloadydb
	env/bin/dbloady -u postgresql://localhost/testdbloady -s state.yaml data.yaml
	env/bin/dbloady -u postgresql://localhost/testdbloady -D state.yaml

env:
	$(PYTHON3) -m venv env
	env/bin/pip install --upgrade pip
	env/bin/pip install sqlalchemy psycopg2
	env/bin/pip install -e ../.. .

.PHONY: testdbloadydb
testdbloadydb:
	dropdb --if-exists testdbloady
	createdb testdbloady
	psql -c "CREATE EXTENSION hstore" testdbloady
	env/bin/python model.py
	rm -f state.yaml

.PHONY: clean
clean:
	-dropdb testdbloady
	rm -rf env __pycache__ testdbloady.egg-info
