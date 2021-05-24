from sqlalchemy import Column, Integer, String

from database import Base


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    name = Column(String(64))
    user = Column(String(64))
    password = Column(String(64))


class Product(Base):
    __tablename__ = 'product'
    id = Column(Integer, primary_key=True)
    name = Column(String(128))
    sku = Column(String(64), index=True)
    description = Column(String(1024))
