import sys
import re
import os
import hashlib
import zipfile
import subprocess
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *


from CVTE_Controller import CVTE_Controller
from CVTE_View import CVTE_View


class CVTE_Model:
    def __init__(self):
        self.controller = None
        self.view = None

    def str(self):
        return '111'
    
    def ToDealWithVersionNameString(self,string):
        str = ''
        for word in string:
            if word >= '0' and word <= '9':
                str += word
            elif word is '.':
                str += word
            else :
                break
        return  str;
            

    def getIconPath(self,res):
        show = ''
        for line in res:
            if line.find('application:') == 0:
                show += line
                break;
        reg = re.compile(
            "application: label='(?P<label>.*)' icon='(?P<icon>.*)'")
        regMatch = reg.match(show)
        if regMatch:
            linebits = regMatch.groupdict()
            if linebits['icon'] is '':
                return None
            else:
                return linebits['icon']
        else:
            return None

    def parse_icon(self,filePath, iconPath):
        if iconPath == None:
            return
        zip = zipfile.ZipFile(filePath)
        iconData = zip.read(iconPath)
        saveIconName = "icon.png"
        with open(saveIconName,'w+b') as saveIconFile:
            saveIconFile.write(iconData)


    def getAppName(self,res1, res2):
        show1 = ''
        for line1 in res1:
            if line1.find('application:') == 0:
                show1 += line1
                break;
        reg1 = re.compile(
            "application: label='(?P<label>.*)' ")
        regMatch1 = reg1.match(show1) 
        if regMatch1:
            linebits1 = regMatch1.groupdict()
            if linebits1['label'] is '':
                show2 = ''
                for line2 in res2:
                    if line2.find('String #0:') == 0:
                        show2 += line2
                        break;
                if show2 is '':
                    return None
                else:
                    return show2.split(': ')[-1]
            else:
                return linebits1['label']
        else:
            return None

    def getCPUFamewok(self, res):
        string = ''
        for line in res:
            if line.find('native-code:') == 0:
                string += re.search("\'.*\'", line).group() +'\r\n'
        return string.replace('\'', '')
        
    def getIconPix(self,path, res):
    #    os.popen('ERASE /Q icon.png')
        for root, dirs, files in os.walk('./'):
            for name in files:
                if(name.endswith(".png")):
                    os.remove(os.path.join(root, name))
        self.parse_icon(path,self.getIconPath(res))
        print("parse_icon succeed")
        pix = QPixmap('icon.png')
        print(pix)
        return pix  

    def getPackage(self, res, path):
        print("getPackage the res is %s"%res)
        print("getPackage the path is %s"%path)
        show = ''
        for line in res:
            if line.find('package') == 0:
                show += line
                print(show)
                break;
        reg = re.compile(
            ".*name='(?P<packageName>.*)' versionCode='(?P<versionCode>.*)' versionName='(?P<versionName>.*)'")
        print(reg)
        regMatch = reg.match(show)
        print("regMatch is %s"%regMatch)
        if regMatch:
            linebits = regMatch.groupdict()
            print('true')
            print(linebits['packageName'])
            print(linebits['versionCode'])
            print(self.ToDealWithVersionNameString(linebits['versionName']))
                  
            return "true", "apk文件分析成功", linebits['packageName'], linebits['versionCode'], self.ToDealWithVersionNameString(linebits['versionName'])
        else:
            print('false')
            return "false", "apk文件aapt分析操作失败，请确保文件路径({})是否书写正确".format(path), None, None, None


    def getSdkVersion(self, res):
        show = ''
        for line in res:
            if line.find('sdkVersion') == 0:
                show += line
                break;
        reg = re.compile(
            "sdkVersion:'(?P<sdkVersion>.*)'")
        regMatch = reg.match(show)
        if regMatch:
            linebits = regMatch.groupdict()
            return linebits['sdkVersion']
        else:
            return None

    def getTargetSdkVersion(self, res):
        show = ''
        for line in res:
            if line.find('targetSdkVersion') == 0:
                show += line
                break;
        reg = re.compile(
            "targetSdkVersion:'(?P<targetSdkVersion>.*)'")
        regMatch = reg.match(show)
        if regMatch:
            linebits = regMatch.groupdict()
            return linebits['targetSdkVersion']
        else:
            return None
        

    def getPermission(self, res):
        string = ''
        for line in res:
            if line.find('uses-permission') == 0:
                string += re.search("\'.*\'", line).group() +'\r\n'
        return string.replace('\'', '')

    def getDensities(self, res):
        string = ''
        for line in res:
            if line.find('densities') == 0:
                string += re.search("\'.*\'", line).group() +'\r\n'
        return string.replace('\'', '')

    def getSupportsScreens(self, res):
        string = ''
        for line in res:
            if line.find('supports-screens') == 0:
                string += re.search("\'.*\'", line).group() +'\r\n'
        return string.replace('\'', '')

    def getApplication(self, res):
        string = ''
        for line in res:
            if line.find('application:') == 0:
                string += line +'\r\n'
        return string


    # 获取文件的md5
    def getBigFileMD5(self, filepath):
        md5obj = hashlib.md5()
        maxbuf = 8192
        try:
            f = open(filepath, 'rb')
        except Exception as err:
            return "获取文件的md5失败,找不到文件，请确保文件路径（{}）是否书写正确".format(filepath)
        while True:
            buf = f.read(maxbuf)
            if not buf:
                break
            md5obj.update(buf)
        f.close()
        hash = md5obj.hexdigest()
        return str(hash).upper()


    # 字节bytes转化kb\m\g
    def formatSize(self,bytes):
        try:
            bytes = float(bytes)
            kb = bytes / 1024
        except:
            return "Error,传入的字节格式不对"

        if kb >= 1024:
            M = kb / 1024
            if M >= 1024:
                G = M / 1024
                return "%fG" % G
            else:
                return "%fM" % M
        else:
            return "%fkb" % kb


    # 获取文件大小
    def getFileSize(self, path):
        print(path)
        size = os.path.getsize(path)
        return self.formatSize(size)


    # 获取文件夹大小
    def getFileDirSize(self, path):
        sumsize = 0
        try:
            filename = os.walk(path)
            for root, dirs, files in filename:
                for fle in files:
                    size = os.path.getsize(path + fle)
                    sumsize += size
            return True, "成功得到文件夹大小", formatSize(sumsize)
        except Exception as err:
            return False, "获取文件夹大小失败,失败原因：{}".format(str(err)), None

