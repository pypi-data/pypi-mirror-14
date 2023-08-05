# -*- coding: utf-8 -*-
# :Project:   metapensiero.sqlalchemy.dbloady -- YAML based data loader
# :Created:   mer 10 feb 2010 14:35:05 CET
# :Author:    Lele Gaifax <lele@metapensiero.it>
# :License:   GNU General Public License version 3 or later
# :Copyright: Copyright (C) 2010-2016 Lele Gaifax
#

from os.path import join, normpath

import yaml


def resolve_class_name(classname):
    """Import a particular Python class given its full dotted name.

    :param classname: full dotted name of the class,
                      such as "package.module.ClassName"
    :rtype: the Python class
    """

    modulename, _, classname = classname.rpartition('.')
    module = __import__(modulename, fromlist=[classname])
    return getattr(module, classname)


class File(yaml.YAMLObject):
    """Facility to read the content of an external file.

    The value of field may be loaded from an external file, given its pathname which is
    interpreted as relative to the position of the YAML file currently loading::

        - entity: cpi.models.Document
          key: filename
          data:
            - filename: image.gif
              content: !File {path: ../image.gif}
    """

    yaml_tag = '!File'

    basedir = None

    def __init__(self, path):
        self.path = path

    def read(self):
        fullpath = normpath(join(self.basedir, self.path))
        return open(fullpath).read()
