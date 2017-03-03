# -*- coding: utf-8 -*-

__all__ = [ 'op_name', 'process' ]

op_name = 'tag_list'


from api_exception import APIError
from libcreat import model
from libcreat.model import DBSession

def process(sid, params):

    print params['pid']
    podtags = DBSession.query(model.podtag).filter_by(pid=params['pid']).all()
    if not podtags:
        raise APIError(1,'pod is not existed')

    #podspecs = DBSession.query(model.podspec).filter_by(pid=55).all()
    return (podtags, 'success.')
