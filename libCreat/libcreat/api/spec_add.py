# -*- coding: utf-8 -*-

__all__ = [ 'op_name', 'process' ]

op_name = 'spec_add'


from api_exception import APIError
from libcreat import model
from libcreat.model import DBSession

def process(sid, params):
    podone = DBSession.query(model.podspec).filter_by(podName=params['podName']).first()
    podtwo = DBSession.query(model.podspec).filter_by(podName=params['repoName']).first()
    if podone:
        raise APIError(1,'podName: '+params['podName'] + '已存在')
    elif podtwo:
        raise APIError(1,'repoName: '+params['repoName'] + '已存在')

    newPod = model.podspec(libHttpUrl = params['libHttpUrl'],podspecName = params['podspecName'],sourceHttpUrl = params['sourceHttpUrl'],repoName = params['repoName'],podName = params['podName'],libSSHUrl = params['libSSHUrl'],sourceSSHUrl = params['sourceSSHUrl'])
    
    DBSession.add(newPod)
    DBSession.flush()

    #podspecs = DBSession.query(model.podspec).filter_by(pid=55).all()
    return (newPod, 'success.')
