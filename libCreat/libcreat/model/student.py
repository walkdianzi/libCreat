from sqlalchemy import *
from sqlalchemy.orm import mapper, relation, relation, backref
from sqlalchemy import Table, ForeignKey, Column
from sqlalchemy.types import Integer, Unicode, DateTime

from libcreat.model import DeclarativeBase, metadata, DBSession
from datetime import datetime

class student(DeclarativeBase):
   __tablename__ = 'student'

   uid = Column(Integer, primary_key = True)
   name = Column(Unicode(20), nullable = False, default = '')
   city = Column(Unicode(20), nullable = False, default = '')
   address = Column(Unicode(100), nullable = False, default = '')
   pincode = Column(Unicode(10), nullable = False, default = '')