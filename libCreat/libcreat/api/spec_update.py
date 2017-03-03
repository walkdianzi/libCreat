# -*- coding: utf-8 -*-

__all__ = [ 'op_name', 'process' ]

op_name = 'spec_update'


from api_exception import APIError
from libcreat import model
from libcreat.model import DBSession

def process(sid, params):
    print params['pid']
    pod = DBSession.query(model.podspec).get(params['pid'])
    if not pod:
        raise APIError(1,'pod is not existed')

    if params.has_key('libHttpUrl'):
        pod.libHttpUrl = params['libHttpUrl']

    if params.has_key('podspecName'):
        pod.podspecName = params['podspecName']

    if params.has_key('sourceHttpUrl'):
        pod.sourceHttpUrl = params['sourceHttpUrl']

    if params.has_key('tagBranch'):
        pod.tagBranch = params['tagBranch']

    if params.has_key('tag'):
        pod.tag = params['tag']

    if params.has_key('repoName'):
        pod.repoName = params['repoName']

    if params.has_key('podName'):
        pod.podName = params['podName']

    if params.has_key('libSSHUrl'):
        pod.libSSHUrl = params['libSSHUrl']

    if params.has_key('sourceSSHUrl'):
        pod.sourceSSHUrl = params['sourceSSHUrl']

    #podspecs = DBSession.query(model.podspec).filter_by(pid=55).all()
    return (pod, 'success.')
