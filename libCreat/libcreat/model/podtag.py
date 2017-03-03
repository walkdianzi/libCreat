from sqlalchemy import *
from sqlalchemy.orm import mapper, relation, relation, backref
from sqlalchemy import Table, ForeignKey, Column
from sqlalchemy.types import Integer, Unicode, DateTime

from libcreat.model import DeclarativeBase, metadata, DBSession
from datetime import datetime

class podtag(DeclarativeBase):
   __tablename__ = 'podtag'

   tid = Column(Integer, primary_key = True)
   pid = Column(Integer, nullable = False, default = 0)
   tag = Column(Unicode(20), nullable = False, default = '')
   tagBranch = Column(Unicode(20), nullable = False, default = '')