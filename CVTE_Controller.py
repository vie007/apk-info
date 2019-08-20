import sys
import re
import os
import hashlib
import zipfile
import subprocess
from CVTE_View import CVTE_View


class CVTE_Controller:
    def __init__(self):
        self.view = None
        self.model = None

    def cleanedit(self):
        self.view.appNameIs.clear()
        self.view.pubilcVersionIs.clear()
        self.view.frameworkVersionIs.clear()
        self.view.packageNameIs.clear()
        self.view.sdkVersionIs.clear()
        self.view.targetSdkVersionIs.clear()
        self.view.screenNameIs.clear()
        self.view.densityNameIs.clear()
        self.view.permissionsNameIs.clear()
        self.view.attributeNameIs.clear()
        self.view.fileSizeNameIs.clear()
        self.view.fileMD5NameIs.clear()
        self.view.currentNameIs.clear()
        self.view.newNameIs.clear()
        self.view.picture.clear()
        self.view.CPUFamewokIs.clear()

    def setDisplay(self):
        st = subprocess.STARTUPINFO()
        st.dwFlags = subprocess.CREATE_NEW_CONSOLE | subprocess.STARTF_USESHOWWINDOW
        st.wShowWindow = subprocess.SW_HIDE
        
        path = self.view.editpath.text()#'C:/Users/user/Desktop/cvte-TvService-2.6.0.apk'
        path = "\"%s\""%path 
        commond1 = './tool/aapt dump badging %s' % path
        res1=''
        try:
            adb1 = subprocess.Popen(commond1, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,startupinfo=st)
            res1 = adb1.communicate()[0].decode().split("\r\n")
        except Exception as err:
            1+1 #空操作
        
        commond2 = './tool/aapt dump strings %s' % path
        res2=''
        try:
            adb2 = subprocess.Popen(commond2, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,startupinfo=st)
            res2 = adb2.communicate()[0].decode().split("\r\n")
        except Exception as err:
            1+1 #空操作
           # print(commond2+',Command parsing results are too long!')
           # QMessageBox.warning(self,"Warning", commond2+',Command parsing results are too long!')

        
        b, information, packageName, versionCode, versionName = self.model.getPackage(res1,path)
        print("Analytical conditions is %s"%b)
        if b is "true":
            self.view.appNameIs.setText(self.model.getAppName(res1,res2))
            print('111')
            self.view.CPUFamewokIs.setText(self.model.getCPUFamewok(res1))
            print('222')
            self.view.pubilcVersionIs.setText(versionName)
            print('333')
            self.view.frameworkVersionIs.setText(versionCode)
            print('4')
            self.view.packageNameIs.setText(packageName)
            print('5')
            self.view.sdkVersionIs.setText(self.model.getSdkVersion(res1))
            print('6')
            self.view.targetSdkVersionIs.setText(self.model.getTargetSdkVersion(res1))
            print('7')
            self.view.screenNameIs.setText(self.model.getSupportsScreens(res1))
            print('8')
            self.view.densityNameIs.setText(self.model.getDensities(res1))
            print('9')
            self.view.permissionsNameIs.setPlainText(self.model.getPermission(res1))
            print('10')
            self.view.attributeNameIs.setPlainText(self.model.getApplication(res1))
            print('11')
            self.view.fileSizeNameIs.setText(self.model.getFileSize(path.replace('\"','')))
            print('12')
            self.view.fileMD5NameIs.setText(self.model.getBigFileMD5(path.replace('\"','')))
            print('13')
            self.view.currentNameIs.setText(path.replace('\"','').split('/')[-1])
            print('14')
            self.view.newNameIs.setText(self.model.getAppName(res1,res2)+' '+versionName+'.'+versionCode+'.apk')
            print('15')
            self.view.picture.setPixmap(self.model.getIconPix(path.replace('\"',''),res1))
            print('16')
        else:
            self.view.prompt("analyzeError", information)
