# -*- coding: utf-8 -*-
# :Project:   metapensiero.sqlalchemy.dbloady -- Dump functional test
# :Created:   gio 10 mar 2016 18:43:53 CET
# :Author:    Lele Gaifax <lele@metapensiero.it>
# :License:   GNU General Public License version 3 or later
# :Copyright: © 2016 Lele Gaifax
#

PYTHON3 ?= python3.5

.PHONY: test
test: env clean first.dump second.dump
	cmp first.dump second.dump

env:
	$(PYTHON3) -m venv env
	env/bin/pip install --upgrade pip
	env/bin/pip install sqlalchemy
	env/bin/pip install -e ../.. .

first.dump:
	rm -f /tmp/testdbloady.sqlite
	env/bin/python model.py
	env/bin/dbloady -u sqlite:////tmp/testdbloady.sqlite data.yaml
	echo ".dump" | sqlite3 /tmp/testdbloady.sqlite > first.dump
	env/bin/dbdumpy -u sqlite:////tmp/testdbloady.sqlite spec.yaml output.yaml

second.dump:
	rm -f /tmp/testdbloady.sqlite
	env/bin/python model.py
	env/bin/dbloady -u sqlite:////tmp/testdbloady.sqlite output.yaml
	echo ".dump" | sqlite3 /tmp/testdbloady.sqlite > second.dump

.PHONY: clean
clean:
	rm -f /tmp/testdbloady.sqlite output.yaml first.dump second.dump

.PHONY: realclean
realclean: clean
	rm -rf env __pycache__ testdbloady.egg-info
