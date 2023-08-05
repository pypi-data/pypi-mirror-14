# -*- coding: utf-8 -*-
# :Project:   metapensiero.sqlalchemy.dbloady -- Test model
# :Created:   gio 14 gen 2016 11:30:16 CET
# :Author:    Lele Gaifax <lele@metapensiero.it>
# :License:   GNU General Public License version 3 or later
# :Copyright: Copyright (C) 2016 Lele Gaifax
#

from sqlalchemy import create_engine, Column, Integer, String, Time
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()

class Event(Base):
    __tablename__ = 'events'

    id = Column(Integer, primary_key=True)
    description = Column(String(64))
    starttime = Column(Time())
    endtime = Column(Time())


url = 'sqlite:////tmp/testdbloady.sqlite'
e = create_engine(url)
Base.metadata.create_all(e)
