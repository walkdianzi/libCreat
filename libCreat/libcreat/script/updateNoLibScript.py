#!/usr/bin/python
#-*- coding: utf-8 -*-
#encoding=utf-8

from libcreat import model
from libcreat.model import DBSession
import os
import os.path
import string,re,sys
import shutil
import json
import getopt 
import sys
reload(sys)
sys.setdefaultencoding('utf8')

basepath=os.path.dirname(os.path.abspath(__file__))
lib_des_dir = basepath+"/smallLibSpecs"
updateSpec_dir = basepath+"/updateSpec.sh"
synpushSmallLibSpec_dir = basepath+"/synpushSmallLibSpec.sh"

# 修改为自己的spec仓库
smallSpec_dir = basepath+"/spec/smallSpecs"

# 判断是否是可以生成二进制库的Pod
def getJsonModel(podName):
    pod = DBSession.query(model.podspec).filter_by(podName=unicode(podName)).first()
    if pod is None:
        return 0
    else:
        return pod.pid

def copyNoLibTag(podDir,pid,podName):
    podtags = DBSession.query(model.podtag).filter_by(pid=pid).all()
    podtagMap = {}
    for podtag in podtags:
        podtagMap[podtag.tag] = 1

    for parent, dirnames, filenames in os.walk(podDir):
        for dirname in dirnames:
            # 如果tag不存在数据库中则复制过来这个tag的文件夹
            if podtagMap.has_key(dirname) == False:
                if os.path.exists(os.path.join(lib_des_dir+"/"+podName,dirname)):
                    shutil.rmtree(os.path.join(lib_des_dir+"/"+podName,dirname))
                shutil.copytree(os.path.join(parent, dirname),os.path.join(lib_des_dir+"/"+podName,dirname))
        break

#------------------------执行代码-----------------------

def podSearch(specDir):
    shell = updateSpec_dir + ' ' + specDir
    output = os.popen(shell)
    for parent, dirnames, filenames in os.walk(specDir):
        for dirname in dirnames:
            callback = getJsonModel(dirname)
            if callback == 0 and dirname != ".git":
                if os.path.exists(os.path.join(lib_des_dir,dirname)):
                    shutil.rmtree(os.path.join(lib_des_dir,dirname))
                shutil.copytree(os.path.join(parent, dirname),os.path.join(lib_des_dir,dirname))
            elif callback != 0 and dirname != ".git":
                copyNoLibTag(os.path.join(parent, dirname),callback,dirname)
        break

def update():
    podSearch(smallSpec_dir)

    # push SmallLibSpecs
    shell = synpushSmallLibSpec_dir + ' ' + lib_des_dir 
    output = os.popen(shell)
