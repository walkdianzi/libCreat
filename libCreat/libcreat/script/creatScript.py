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
clone_sh_dir = basepath+"/clone.sh"
clonelib_sh_dir = basepath+"/cloneLib.sh"
creat_frame_dir = basepath+"/creatFramework.sh"
master_dir = "/Users/dasheng/.cocoapods/repos/master/Specs"


def checkPodWithDir(podDir,repoModel):
    list = os.listdir(podDir)
    isCopyJson = True
    podspecDir = ""
    podspecJsonDir = ""
    for line in list:
        if line.find(".podspec")>-1 and line.find(".json") == -1:
            podspecDir = os.path.join(podDir,line)
            f = open(podspecDir,'r')
            for lineStr in f.readlines():
                if (lineStr.find("s.version")>-1 or lineStr.find("@version")>-1) and lineStr.find(repoModel.tag)>-1:
                    isCopyJson = False
                    break
            if isCopyJson == False:
                break
        if line.find(".podspec.json")>-1:
            podspecJsonDir = os.path.join(podDir,line)

    # 如果isCopyJson为True，则原有的.podspec不可用，需要去仓库中找去对应tag的.podspec
    if isCopyJson == True:
        if len(podspecDir)>0:
            os.remove(podspecDir)
        if len(podspecJsonDir)>0:
            os.remove(podspecJsonDir)
        podSearch(podDir,repoModel.tag)
        print "copy true"
    else:
        print "copy false"
        shell = creat_frame_dir + ' ' + podDir + ' ' + podspecDir.replace(podDir+"/","")
        print shell
        output = os.system(shell)

#到master分支搜索对应pod的.podspec.json并复制
def podSearch(podDir,tag):
    print podDir
    for parent, dirnames, filenames in os.walk(master_dir):
        for dirname in dirnames:
            if podDir.find(dirname)>-1 or (podDir.find("FDCollapsibleConstraints")>-1 and dirname.find("UIView+FDCollapsibleConstraints")>-1):
                list = os.listdir(os.path.join(parent,dirname))
                for line in list:
                    if line.find(tag)>-1:
                        tagDir = os.path.join(os.path.join(parent,dirname),line)
                        tagList = os.listdir(tagDir)
                        for tagLine in tagList:
                            shutil.copy(os.path.join(tagDir, tagLine),os.path.join(podDir,tagLine))
                            shell = creat_frame_dir + ' ' + podDir + ' ' + tagLine
                            print shell
                            output = os.system(shell)

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

#------------------------传参处理-----------------------

def creatFramework(podInfo,tag,tagBranch):
    # clone源码
    podDir = clonePod(podInfo,tagBranch)
    # 创建对应tag的二进制库
    podInfo.tag = tag
    podInfo.tagBranch = tagBranch
    checkPodWithDir(podDir,podInfo)
    # clone Lib仓库
    cloneLibPod(podInfo)
    # 复制源码中创建好的二进制库到Lib仓库中，并修改podspec和上传podspec
    copyFramework.copyNeedFile(podDir,podInfo)
