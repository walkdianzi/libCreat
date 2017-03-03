# -*- coding: utf-8 -*-
"""Main Controller"""

from tg import expose, flash, require, url, lurl
from tg import request, redirect, tmpl_context
from tg.i18n import ugettext as _, lazy_ugettext as l_
from tg.exceptions import HTTPFound
from tg import predicates
from libcreat import model
from libcreat.controllers.secure import SecureController
from libcreat.model import DBSession
from tgext.admin.tgadminconfig import BootstrapTGAdminConfig as TGAdminConfig
from tgext.admin.controller import AdminController

from libcreat.lib.base import BaseController
from libcreat.controllers.error import ErrorController
from libcreat.controllers.studentform import StudentForm
from libcreat.model.student import student
from libcreat.model.podspec import podspec
from libcreat.model.JSONObject import JSONObject
from tw2.forms import DataGrid
from tg.decorators import paginate

import json
import os
import sys
import getopt 

__all__ = ['BlogController']

class BlogController(BaseController):

   @expose('libcreat.templates.blog.blog')
   def index(self):
      return {}
        
   @expose('libcreat.templates.blog.post')
   def post(self):
      from datetime import date
      now = date.today().strftime("%d-%m-%y")
      return {'date':now}
