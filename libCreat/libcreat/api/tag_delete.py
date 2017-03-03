# -*- coding: utf-8 -*-

__all__ = [ 'op_name', 'process' ]

op_name = 'tag_delete'


from api_exception import APIError
from libcreat import model
from libcreat.model import DBSession
from libcreat.script import deleteScript
import update_no_lib
import copy
import traceback

def process(sid, params):

    podtag = DBSession.query(model.podtag).get(params['tid'])
    if not podtag:
        return dict(errors={'podtag':'podtag not found'})

    #删除对应tag的二进制库
    pod = DBSession.query(model.podspec).filter_by(pid=params['pid']).first()
    try:
        deleteScript.deleteFramework(copy.deepcopy(pod),podtag.tag,podtag.tagBranch)
    except Exception, e:
        status, message = e.args
        if status == 4:
            raise APIError(4,message)
        else:
            raise APIError(1,traceback.format_exc())

    #删除数据库中的tag信息
    DBSession.delete(podtag)

    # 删除成功之后更新未二进制的podspec
    update_no_lib.process(sid,params)

    #podspecs = DBSession.query(model.podspec).filter_by(pid=55).all()
    return (podtag, 'success.')

def processNoUpdate(sid, params):
    podtag = DBSession.query(model.podtag).get(params['tid'])
    if not podtag:
        return dict(errors={'podtag':'podtag not found'})

    #删除对应tag的二进制库
    pod = DBSession.query(model.podspec).filter_by(pid=params['pid']).first()
    try:
        deleteScript.deleteFramework(copy.deepcopy(pod),podtag.tag,podtag.tagBranch)
    except Exception, e:
        status, message = e.args
        if status == 4:
            raise APIError(4,message)
        else:
            raise APIError(1,traceback.format_exc())

    #删除数据库中的tag信息
    DBSession.delete(podtag)

    #podspecs = DBSession.query(model.podspec).filter_by(pid=55).all()
    return (podtag, 'success.')