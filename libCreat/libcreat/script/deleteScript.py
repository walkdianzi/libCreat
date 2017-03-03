#!/usr/bin/python
#-*- coding: utf-8 -*-
#encoding=utf-8

import os
import os.path
import string,re,sys
import shutil
import json
import getopt 
import commands
import copyFramework
reload(sys)
sys.setdefaultencoding('utf8')

basepath=os.path.dirname(os.path.abspath(__file__))
orgin_dir = basepath+"/orginRepos"
lib_dir = basepath+"/libRepos"
small_dir = basepath+"/smallLibSpecs"
clone_sh_dir = basepath+"/clone.sh"
clonelib_sh_dir = basepath+"/cloneLib.sh"
creat_frame_dir = basepath+"/creatFramework.sh"
deleteSynpush_dir = basepath+"/deleteSynpush.sh"

def clonePod(podInfo,tagBranch):

    shell = clone_sh_dir + ' ' + podInfo.sourceSSHUrl + ' ' + podInfo.podName + ' ' + tagBranch + ' ' + orgin_dir
    (status, output) = commands.getstatusoutput(shell)
    # 获取shell里面的git命令输出，查看是否切换tag成功
    print output
    if output.find("Switched to branch '"+tagBranch+"'")>-1:
        print "切换成功"
    else:
        print "切换失败"
        raise Exception(4, 'tag的分支切换失败: 请查看是否存在此分支')
    return os.path.join(orgin_dir,podInfo.podName)

def cloneLibPod(podInfo):
    shell = clonelib_sh_dir + ' ' + podInfo.libSSHUrl + ' ' + podInfo.podName+"_Lib" + ' ' + lib_dir
    output = os.popen(shell)

def deleteTagDir(podName,tag):

    orginDir = os.path.join(orgin_dir,podName)
    libDir = os.path.join(lib_dir,podName+"_Lib")
    smallDir = os.path.join(small_dir,podName)

    tagDirName = podName + "-" + tag

    #删除orginRepos里的
    for parent, dirnames, filenames in os.walk(orginDir):
        for dirname in dirnames:
            if dirname == tagDirName:
                shutil.rmtree(os.path.join(orginDir,dirname))
                break
        break
    #删除libRepos里的
    for parent, dirnames, filenames in os.walk(libDir):
        for dirname in dirnames:
            if dirname == tagDirName:
                shutil.rmtree(os.path.join(libDir,dirname))
                shell = deleteSynpush_dir + ' ' + libDir + ' ' + tag
                output = os.popen(shell)
                break
        break
    #删除smallLibSpecs里的
    for parent, dirnames, filenames in os.walk(smallDir):
        for dirname in dirnames:
            if dirname == tag:
                shutil.rmtree(os.path.join(smallDir,dirname))
                break
        break

#------------------------传参处理-----------------------

def deleteFramework(podInfo,tag,tagBranch):
    # clone源码
    podDir = clonePod(podInfo,tagBranch)
    # clone Lib仓库
    cloneLibPod(podInfo)

    deleteTagDir(podInfo.podName,tag)
