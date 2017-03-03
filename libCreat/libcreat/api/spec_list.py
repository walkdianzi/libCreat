# -*- coding: utf-8 -*-

__all__ = [ 'op_name', 'process' ]

op_name = 'spec_list'


from api_exception import APIError
from libcreat import model
from libcreat.model import DBSession

def process(sid, params):
    podspecs = DBSession.query(model.podspec).all()
    #podspecs = DBSession.query(model.podspec).filter_by(pid=55).all()
    return (podspecs, 'success.')
