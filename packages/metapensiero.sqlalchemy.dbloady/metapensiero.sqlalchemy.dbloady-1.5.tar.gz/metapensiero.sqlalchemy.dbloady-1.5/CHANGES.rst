.. -*- coding: utf-8 -*-

Changes
-------

1.5 (2016-03-12)
~~~~~~~~~~~~~~~~

- New complementary dump functionality, exposed by a new cli tool, dbdumpy

- Cosmetic, backward compatible, changes to the YAML format, for nicer sorting


1.4 (2016-02-10)
~~~~~~~~~~~~~~~~

- Data files and preload/postload scripts may be specified also as package relative resources


1.3 (2016-01-14)
~~~~~~~~~~~~~~~~

- New --preload and --postload options to execute arbitrary Python scripts before or after the
  load


1.2 (2016-01-09)
~~~~~~~~~~~~~~~~

- Fix source distribution


1.1 (2016-01-09)
~~~~~~~~~~~~~~~~

- Fix data refs when loading from compact representation


1.0 (2016-01-07)
~~~~~~~~~~~~~~~~

- Allow more compact representation when all instances share the same fields

- Extract dbloady from metapensiero.sphinx.patchdb 1.4.2 into a standalone package
