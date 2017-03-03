# -*- coding: utf-8 -*-

__all__ = [ 'op_name', 'process' ]

op_name = 'update_no_lib'


from api_exception import APIError
from libcreat import model
from libcreat.model import DBSession
from libcreat.script import updateNoLibScript

def process(sid, params):
    print sid
    try:
        updateNoLibScript.update()
    except Exception, e:
        status, message = e.args
        if status == 4:
            raise APIError(4,message)
        else:
            raise APIError(1,traceback.format_exc())

    #podspecs = DBSession.query(model.podspec).filter_by(pid=55).all()
    return ({}, 'success.')
