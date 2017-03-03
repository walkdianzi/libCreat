from libcreat.lib.base import BaseController
from tg import expose, flash, redirect, request,url, lurl
from tg import redirect, validate
from libcreat import model
from libcreat.model import DBSession
from tgext.admin.tgadminconfig import BootstrapTGAdminConfig as TGAdminConfig
from tgext.admin.controller import AdminController
from tg.exceptions import HTTPFound

from libcreat import api

class RootController(BaseController):
   admin = AdminController(model, DBSession, config_type =  TGAdminConfig)

   @expose('libcreat.templates.index')
   def index(self):
      return dict(page = 'index')

   @expose('jsonp')
   def api(self, m='', sid='', **kw):
      if m == '':
          return {
              'info': 'missing api name.',
              'data': {},
              'status': 1
          }
      if sid == '' and m != 'config':
          return {
              'info': 'missing sid.',
              'data': {},
              'status': 10
          }
      # print request.remote_addr
      return api.process_request(m, sid, kw)

   @expose('libcreat.templates.login')
   def login(self, came_from = lurl('/'), failure = None,    login = ''):
    
      if failure is not None:
         if failure == 'user-not-found':
            flash(_('User not found'), 'error')
         elif failure == 'invalid-password':
            flash(_('Invalid Password'), 'error')
            
      login_counter = request.environ.get('repoze.who.logins', 0)
        
      if failure is None and login_counter > 0:
         flash(_('Wrong credentials'), 'warning')
         
      return dict(page = 'login', login_counter = str(login_counter), 
         came_from = came_from, login = login)
   @expose()
    
   def post_login(self, came_from = lurl('/')):
      if not request.identity:
         
         login_counter = request.environ.get('repoze.who.logins', 0) + 1
         redirect('/login', params = dict(came_from = came_from,__logins = login_counter))
        
         userid = request.identity['repoze.who.userid']
         flash(('Welcome back, %s!') % userid)
            
         return HTTPFound(location = came_from)