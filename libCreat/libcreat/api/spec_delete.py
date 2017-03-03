# -*- coding: utf-8 -*-

__all__ = [ 'op_name', 'process' ]

op_name = 'spec_delete'


from api_exception import APIError
from libcreat import model
from libcreat.model import DBSession
import tag_delete
import update_no_lib

def process(sid, params):

    #删除所有的tag
    podtags = DBSession.query(model.podtag).filter_by(pid=params['pid']).all()
    for podtag in podtags:
        tag_delete.processNoUpdate(sid,{"pid":params['pid'],"tid":podtag.tid})

    #删除pod
    pod = DBSession.query(model.podspec).filter_by(pid=params['pid']).first()
    if not pod:
        return dict(errors={'pod':'pod not found'})
    DBSession.delete(pod)

    # 删除成功之后更新未二进制的podspec
    update_no_lib.process(sid,params)

    #podspecs = DBSession.query(model.podspec).filter_by(pid=55).all()
    return ({}, 'success.')