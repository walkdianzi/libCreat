from sqlalchemy import *
from sqlalchemy.orm import mapper, relation, relation, backref
from sqlalchemy import Table, ForeignKey, Column
from sqlalchemy.types import Integer, Unicode, DateTime

from libcreat.model import DeclarativeBase, metadata, DBSession
from datetime import datetime

class podspec(DeclarativeBase):
   __tablename__ = 'podspec'

   pid = Column(Integer, primary_key = True)
   repoName = Column(Unicode(20), nullable = False, default = '')
   podName = Column(Unicode(20), nullable = False, default = '')
   podspecName = Column(Unicode(20), nullable = False, default = '')
   sourceSSHUrl = Column(Unicode(100), nullable = False, default = '')
   sourceHttpUrl = Column(Unicode(100), nullable = False, default = '')
   libSSHUrl = Column(Unicode(100), nullable = False, default = '')
   libHttpUrl = Column(Unicode(100), nullable = False, default = '')
   tag = Column(Unicode(20), nullable = False, default = '')
   tagBranch = Column(Unicode(20), nullable = False, default = '')