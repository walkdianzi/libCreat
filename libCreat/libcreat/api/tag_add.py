# -*- coding: utf-8 -*-

__all__ = [ 'op_name', 'process' ]

op_name = 'tag_add'

from libcreat import model
from libcreat.model import DBSession
from libcreat.script import creatScript
from api_exception import APIError
import copy
import traceback

def process(sid, params):

    #创建对应tag的二进制库
    pod = DBSession.query(model.podspec).filter_by(pid=params['pid']).first()
    
    try:
        creatScript.creatFramework(copy.deepcopy(pod),params['tag'],params['tagBranch'])
    except Exception, e:
        status, message = e.args
        if status == 4:
            raise APIError(4,message)
        else:
            raise APIError(1,traceback.format_exc())

    #创建成功则存入数据库
    newTag = model.podtag(tagBranch = params['tagBranch'],tag = params['tag'],pid = params['pid'])
    DBSession.add(newTag)
    DBSession.flush()

    #podspecs = DBSession.query(model.podspec).filter_by(pid=55).all()
    return (newTag, 'success.')
