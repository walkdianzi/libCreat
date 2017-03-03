# -*- coding: utf-8 -*-

__all__ = [ 'op_name', 'process' ]

op_name = 'spec_find'


from api_exception import APIError
from libcreat import model
from libcreat.model import DBSession

def process(sid, params):
    print params['pid']
    pod = DBSession.query(model.podspec).get(params['pid'])
    if not pod:
        raise APIError(1,'pod is not existed')

    #podspecs = DBSession.query(model.podspec).filter_by(pid=55).all()
    return (pod, 'success.')
