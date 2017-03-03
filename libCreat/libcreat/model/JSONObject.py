from sqlalchemy import *
from sqlalchemy.orm import mapper, relation, relation, backref
from sqlalchemy import Table, ForeignKey, Column
from sqlalchemy.types import Integer, Unicode, DateTime

from libcreat.model import DeclarativeBase, metadata, DBSession
from datetime import datetime

import json
import os
import sys
import getopt 

class JSONObject:
    def __init__(self, d):
        self.__dict__ = d
