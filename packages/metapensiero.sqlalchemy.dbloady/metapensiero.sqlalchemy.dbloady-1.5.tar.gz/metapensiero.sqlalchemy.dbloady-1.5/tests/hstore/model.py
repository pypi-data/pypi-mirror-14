# -*- coding: utf-8 -*-
# :Project:   metapensiero.sqlalchemy.dbloady -- Test model
# :Created:   gio 22 ott 2015 18:07:50 CEST
# :Author:    Lele Gaifax <lele@metapensiero.it>
# :License:   GNU General Public License version 3 or later
# :Copyright: Copyright (C) 2015, 2016 Lele Gaifax
#

from sqlalchemy import create_engine, Column, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import HSTORE
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship


Base = declarative_base()

class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True)
    description = Column(HSTORE)


class Attribute(Base):
    __tablename__ = 'attributes'

    id = Column(Integer, primary_key=True)
    name = Column(String(64))
    description = Column(HSTORE)


class Values(Base):
    __tablename__ = 'product_attributes'

    id = Column(Integer, primary_key=True)
    idproduct = Column(Integer,
                       ForeignKey('products.id', ondelete='CASCADE'),
                       nullable=False)
    idattribute = Column(Integer, ForeignKey('attributes.id', ondelete='CASCADE'),
                         nullable=False)
    value = Column(String(64))

    product = relationship('Product')
    attribute = relationship('Attribute')


url = 'postgresql://localhost/testdbloady'
e = create_engine(url)
Base.metadata.create_all(e)
