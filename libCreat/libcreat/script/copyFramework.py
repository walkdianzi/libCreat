#!/usr/bin/python
#-*- coding: utf-8 -*-
#encoding=utf-8

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
des_dir = basepath+"/libRepos"
smallLibSpecs_dir = basepath+"/smallLibSpecs"
synpush_dir = basepath+"/synpush.sh"
synpushSmallLibSpec_dir = basepath+"/synpushSmallLibSpec.sh"

#找出需要的文件并复制
def copyNeedFile(filepath,repoModel):
    podspecName = repoModel.podspecName

    #复制全部到新的git仓库,其中原仓库的podspec如果跟tag不符,在复制过来之前已经从master中找出正确tag的.json替换掉了。
    #所以复制过来podspec的tag一定是对的
    real_des_Dir = copyDir(filepath,repoModel)
    desPodspecDir = os.path.join(real_des_Dir,podspecName)

    if podspecName.find(".podspec.json")>-1:
        rewritePodspecJson(desPodspecDir,repoModel)
        podspecName = podspecName.replace(".json","")
        desPodspecDir = os.path.join(real_des_Dir,podspecName)
    else:
        rewritePodspec(desPodspecDir,repoModel,real_des_Dir)

    #提交
    shell = synpush_dir + ' ' + real_des_Dir + ' ' + repoModel.tagBranch
    output = os.popen(shell)
    pushSmallLibSpecs(real_des_Dir,podspecName,repoModel.tag,repoModel.podName)

def pushSmallLibSpecs(parent,filename,version,podName):
    print "#####"+version + filename
    finalDir = os.path.join(smallLibSpecs_dir,podName + '/' + version)
    if os.path.exists(finalDir) == True:
        shutil.rmtree(finalDir)
    os.makedirs(finalDir)
    shutil.copy(os.path.join(parent, filename),os.path.join(finalDir,filename))

    # push SmallLibSpecs
    shell = synpushSmallLibSpec_dir + ' ' + smallLibSpecs_dir 
    output = os.popen(shell)

def copyDir(copyDirPath,repoModel):
    print copyDirPath
    real_des_Dir = des_dir + '/' + repoModel.podName + '_Lib' + '/'
    #删除 除.git配置文件和原有版本的Framework外的所有文件
    for parent, dirnames, filenames in os.walk(real_des_Dir):
        for dirname in dirnames:
            if dirname[0].find(".")==-1 and dirname.find(repoModel.podName+"-")==-1:
                shutil.rmtree(os.path.join(real_des_Dir,dirname))
        for filename in filenames:
            if filename[0].find(".")==-1:
                os.remove(os.path.join(real_des_Dir,filename))
        break

    #复制 除.git配置文件外的所有文件，特殊情况：le.podspec.json 不用复制
    for parent, dirnames, filenames in os.walk(copyDirPath):
        for dirname in dirnames:
            if dirname[0].find(".") > -1:
                continue
            if os.path.exists(os.path.join(real_des_Dir,dirname)):
                shutil.rmtree(os.path.join(real_des_Dir,dirname))
            try:
                shutil.copytree(os.path.join(parent, dirname),os.path.join(real_des_Dir,dirname))
                if dirname == repoModel.podName+"-"+repoModel.tag:
                    removeFile(os.path.join(real_des_Dir,dirname))
            except:
                print dirname + "复制失败"
        for filename in filenames:
            if filename[0].find(".") > -1 or filename.find("le.podspec.json")>-1 or filename.find("_Pods.xcodeproj")>-1:
                continue
            if os.path.isfile(os.path.join(real_des_Dir,filename)):
                os.remove(os.path.join(real_des_Dir,filename))
            try:
                shutil.copy(os.path.join(parent, filename),os.path.join(real_des_Dir,filename))
            except:
                print filename + "复制失败"
        break
    return real_des_Dir

#Framework里删除不必要的文件
def removeFile(frameworkDir):
    for parent, dirnames, filenames in os.walk(frameworkDir):
        for dirname in dirnames:
            if dirname == "build" or dirname == "Versions":
                shutil.rmtree(os.path.join(parent,dirname))

def rewritePodspec(desPodspecDir,repoModel,realDesDir):
    podName = repoModel.podName
    versionStr = repoModel.tag

    #读取podspec内容
    f = open(desPodspecDir,'r+')
    content = f.read()
    f.close()

    #修改podspec
    f = open(desPodspecDir,'r+')
    subSourceFileStr = ""
    sourceFileStr = ""
    resourcesStr = ""
    headerFileStr = ""
    lastString = ""
    preservePaths = "  s.preserve_paths = "
    for lineStr in f.readlines():

        #如果为空白行或注释则删除
        commentStr = lineStr.strip()
        if commentStr.startswith('#'):  #判断是否是注释行
            content = content.replace(lineStr,"")
            continue 

        #获取sourceFile
        if lineStr.find("s.source_files")>-1:
            sourceFileStr = lineStr

        if lineStr.find("s.public_header_files")>-1:
            headerFileStr = lineStr

        if lineStr.find(".source_files")>-1 or lineStr.find(".resources")>-1:
            preservePaths = preservePaths + findPath(lineStr) + ","

        #获取default_subspec
        if lineStr.find("default_subspec") > -1:
            subSourceFileStr = subSourceFileStr + "  " +lineStr
            content = content.replace(lineStr,"")

        #获取最后一行
        lastString = lineStr


    #获取s.subspec
    pat = re.compile(r'\s+\bs\.subspec\b[\s\S]*?\bend\b')
    match = pat.findall(content)
    for subStr in match:
        content = content.replace(subStr,"")
        subSourceFileStr = subSourceFileStr + subStr + "\n"
    if len(subSourceFileStr)>0:
        #缩进两个空格
        subSourceFileStr = subSourceFileStr.replace("\n","\n  ")
        subSourceFileStr = subSourceFileStr + "\n"

    #获取s.resource_bundles
    patTwo = re.compile(r'\bs\.resource_bundles\b[\s\S]*?[}]\n')
    matchTwo = patTwo.search(content)
    if matchTwo:
        resourcesStr = matchTwo.group()
        content = content.replace(resourcesStr,"")
        resourcesStr = resourcesStr.replace("\n","\n  ").strip()
        resourcesStr = "    " + resourcesStr + "\n"

    dirFirst = ""
    framework = "\"" + podName + "-" + versionStr + "/" + "ios/" + podName + ".embeddedframework/" + podName + ".framework\"\n"
    preservePaths = preservePaths + framework
    frameworkDir = "    s.ios.vendored_framework = " + framework

    resourcesDir = hasBundle(realDesDir,framework,podName,0)
    if len(subSourceFileStr)>0:
        subFramework = getSubFramework(realDesDir,subSourceFileStr,framework)
        dirFirst = "  $source = ENV['use_source']\n" + "  $source_name = ENV[\"#{s.name}_source\"]\n" + "  if $source || $source_name\n" + subSourceFileStr
        dirFirst = dirFirst + "  else\n" + subFramework + resourcesDir + "  end\n" + preservePaths +"end"
        content = content.replace(lastString,dirFirst)
    else:
        if len(headerFileStr)>0:
            content = content.replace(headerFileStr,"")
            headerFileStr = "  " + headerFileStr
        dirFirst = "  $source = ENV['use_source']\n" + "  $source_name = ENV[\"#{s.name}_source\"]\n" + "  if $source || $source_name\n" + "  " + sourceFileStr + headerFileStr + resourcesStr
        dirFirst = dirFirst + "  else\n" + frameworkDir + resourcesDir + "  end\n" + preservePaths
        content = content.replace(sourceFileStr,dirFirst)

    content = content.replace(repoModel.sourceHttpUrl,repoModel.libHttpUrl)
    content = content.replace(repoModel.sourceSSHUrl,repoModel.libHttpUrl)

    #特殊处理
    if content.find("'PSTCollectionView/'"):
        content = content.replace("'PSTCollectionView/'","'PSTCollectionView/**'")

    fw = open(desPodspecDir,'w')
    fw.write(content)
    fw.close()

def rewritePodspecJson(desPodspecDir,repoModel):

    podName = repoModel.podName
    versionStr = repoModel.tag

    frameworkDir = desPodspecDir.replace(".podspec.json","-"+versionStr)
    print "-------"+frameworkDir
    list = os.listdir(frameworkDir)
    for line in list:
        filepath = os.path.join(frameworkDir,line)
        if os.path.isfile(filepath) and line.find(".podspec")>-1 and line.find(".json") == -1:
            f = open(filepath,'r+')
            content = f.read()
            f.close()
            realUrl = "s.source = { :git => \"" + repoModel.libHttpUrl + "\", :tag => s.version.to_s}"
            content = content.replace("s.source = { :path => '.' }",realUrl)
            content = content.replace("ios/"+podName+".embeddedframework",podName+"-"+versionStr+"/ios/"+podName+".embeddedframework")
            fw = open(filepath,'w')
            fw.write(content)
            fw.close()
            os.remove(desPodspecDir)
            shutil.copy(filepath,desPodspecDir.replace(".json",""))

#返回路径
def findPath(lineStr):
    strArray = lineStr.split('=')
    return strArray[1].replace("\n","").replace(";","")

def hasBundle(realDesDir,framework,podName,isSS):
    framework = framework.replace("\n","")
    framework = framework.replace("\"","")
    bundleDir = framework+"/Resources/"+podName+".bundle"
    if os.path.exists(os.path.join(realDesDir,bundleDir)):
        if isSS:
            return "    ss.resources = " + "\"" + bundleDir + "\"\n"
        else:
            return "    s.resources = " + "\"" + bundleDir + "\"\n"
    else:
        return ""

def getSubFramework(realDesDir,subSourceFileStr,framework):

    frameworkDir = "    s.ios.vendored_framework = " + framework

    pat = re.compile(r'\s+\bs\.subspec\b[\s\S]*?\bend\b')
    match = pat.findall(subSourceFileStr)
    subFrameworkDir = ""
    for subStr in match:
        #获取s.subspec
        p = re.compile(r'\bs\.subspec\b.*?\|ss\|')
        m = p.search(subStr)
        if m:
            subFrameworkDir += "    " + m.group()+"\n"+"    "+frameworkDir
            strArr = m.group().split("'")
            if strArr[1]:
                subFrameworkDir += "    " + hasBundle(realDesDir,framework,strArr[1],1)
        subFrameworkDir += "\n"+ "    " + "end\n"

    return subFrameworkDir