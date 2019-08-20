from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import sys
import re
import os


class CVTE_View(QWidget):
    def __init__(self):
        self.controller = None
        self.model = None
        super(CVTE_View, self).__init__()
        self.initUI()
        self.show()
        
    def initUI(self):
        # 窗口标题
        self.setWindowIcon(QIcon('./icons/cvte_window.ico'))
        self.setWindowTitle('CVTE-APK-INFO')
        # 定义窗口大小
        self.resize(700, 500)
        self.setFixedSize(700,500)
        
        self.QLabl = QLabel(self)
        self.QLabl.setText('请输入apk的路径:(支持拖拽apk)')
        self.QLabl.setFont(QFont("Timers", 12))
      #  self.QLabl.setGeometry(20, 20, 100, 150)
        #调用Drops方法
        self.setAcceptDrops(True)

        self.QLabl2 = QLabel(self)
        self.QLabl2.setText('Path:')
        self.QLabl2.move(0, 27)
        self.QLabl2.setFont(QFont("Timers", 12))
        self.editpath = QLineEdit('', self)
        self.editpath.setDragEnabled(True)
        self.editpath.setGeometry(50,25,550,25)

        self.btn1 = QPushButton('确定',self)
        self.btn1.setFont(QFont("Timers", 13))
        self.btn1.move(620, 27)
        self.btn1.clicked.connect(self.determine)
    
        self.appName = QLabel(self)
        self.appName.setText('应用名称/CPU架构')
        self.appName.setFont(QFont("Timers", 10))
        self.appName.move(0, 60)
        self.appNameIs = QLineEdit(self)
        self.appNameIs.setFont(QFont("Timers", 10))
        self.appNameIs.setGeometry(150,60,300,20)
        self.appNameIs.setReadOnly(True)
        self.CPUFamewokIs = QLineEdit(self)
        self.CPUFamewokIs.setFont(QFont("Timers", 10))
        self.CPUFamewokIs.setGeometry(470,60,130,20)
        self.CPUFamewokIs.setReadOnly(True)
        

        self.version = QLabel(self)
        self.version.setText('发布版本/架构版本')
        self.version.setFont(QFont("Timers", 10))
        self.version.move(0, 85)
        self.pubilcVersionIs = QLineEdit(self)
        self.pubilcVersionIs.setFont(QFont("Timers", 10))
        self.pubilcVersionIs.setGeometry(150,85,350,20)
        self.pubilcVersionIs.setReadOnly(True)
        self.frameworkVersionIs = QLineEdit(self)
        self.frameworkVersionIs.setFont(QFont("Timers", 10))
        self.frameworkVersionIs.setGeometry(510,85,90,20)
        self.frameworkVersionIs.setReadOnly(True)

        self.packageName = QLabel(self)
        self.packageName.setText('原始包名')
        self.packageName.setFont(QFont("Timers", 10))
        self.packageName.move(0, 110)
        self.packageNameIs = QLineEdit(self)
        self.packageNameIs.setFont(QFont("Timers", 10))
        self.packageNameIs.setGeometry(150,110,450,20)
        self.packageNameIs.setReadOnly(True)

        self.SDKName = QLabel(self)
        self.SDKName.setText('最低/目标编译 SDK')
        self.SDKName.setFont(QFont("Timers", 10))
        self.SDKName.move(0, 135)
        self.sdkVersionIs = QLineEdit(self)
        self.sdkVersionIs.setFont(QFont("Timers", 10))
        self.sdkVersionIs.setGeometry(150,135,270,20)
        self.sdkVersionIs.setReadOnly(True)
        self.targetSdkVersionIs = QLineEdit(self)
        self.targetSdkVersionIs.setFont(QFont("Timers", 10))
        self.targetSdkVersionIs.setGeometry(430,135,260,20)
        self.targetSdkVersionIs.setReadOnly(True)

        self.screenName = QLabel(self)
        self.screenName.setText('屏幕尺寸')
        self.screenName.setFont(QFont("Timers", 10))
        self.screenName.move(0, 160)
        self.screenNameIs = QLineEdit(self)
        self.screenNameIs.setFont(QFont("Timers", 10))
        self.screenNameIs.setGeometry(150,160,540,20)
        self.screenNameIs.setReadOnly(True)
        
        self.densityName = QLabel(self)
        self.densityName.setText('密度')
        self.densityName.setFont(QFont("Timers", 10))
        self.densityName.move(0, 185)
        self.densityNameIs = QLineEdit(self)
        self.densityNameIs.setFont(QFont("Timers", 10))
        self.densityNameIs.setGeometry(150,185,540,20)
        self.densityNameIs.setReadOnly(True)
        

        self.permissionsName = QLabel(self)
        self.permissionsName.setText('权限')
        self.permissionsName.setFont(QFont("Timers", 10))
        self.permissionsName.move(0, 220)
        self.permissionsNameIs = QTextEdit(self)
        self.permissionsNameIs.setFont(QFont("Timers", 10))
        self.permissionsNameIs.setGeometry(150,220,540,80)
        #self.permissionsNameIs.setContextMenuPolicy(Qt.NoContextMenu)
        self.permissionsNameIs.setReadOnly(True)


        self.attributeName = QLabel(self)
        self.attributeName.setText('属性')
        self.attributeName.setFont(QFont("Timers", 10))
        self.attributeName.move(0, 310)
        self.attributeNameIs = QTextEdit(self)
        self.attributeNameIs.setFont(QFont("Timers", 10))
        self.attributeNameIs.setGeometry(150,310,540,80)
        self.attributeNameIs.setReadOnly(True)

        self.fileSizeName = QLabel(self)
        self.fileSizeName.setText('文件大小')
        self.fileSizeName.setFont(QFont("Timers", 10))
        self.fileSizeName.move(0, 400)
        self.fileSizeNameIs = QLineEdit(self)
        self.fileSizeNameIs.setFont(QFont("Timers", 10))
        self.fileSizeNameIs.setGeometry(150,400,540,20)
        self.fileSizeNameIs.setReadOnly(True)

        self.fileMD5Name = QLabel(self)
        self.fileMD5Name.setText('文件MD5值')
        self.fileMD5Name.setFont(QFont("Timers", 10))
        self.fileMD5Name.move(0, 425)
        self.fileMD5NameIs = QLineEdit(self)
        self.fileMD5NameIs.setFont(QFont("Timers", 10))
        self.fileMD5NameIs.setGeometry(150,425,540,20)
        self.fileMD5NameIs.setReadOnly(True)

        self.currentName = QLabel(self)
        self.currentName.setText('当前名称')
        self.currentName.setFont(QFont("Timers", 10))
        self.currentName.move(0, 450)
        self.currentNameIs = QLineEdit(self)
        self.currentNameIs.setFont(QFont("Timers", 10))
        self.currentNameIs.setGeometry(150,450,540,20)
        self.currentNameIs.setReadOnly(True)

        self.newName = QLabel(self)
        self.newName.setText('新名称')
        self.newName.setFont(QFont("Timers", 10))
        self.newName.move(0, 475)
        self.newNameIs = QLineEdit(self)
        self.newNameIs.setFont(QFont("Timers", 10))
        self.newNameIs.setGeometry(150,475,540,20)
        self.newNameIs.setReadOnly(True)

        self.picture = QLabel(self)
        self.picture.setGeometry(610,60,88,70)
        self.picture.setScaledContents (True)
       # self.picture.setStyleSheet("border: 2px solid red")

    
    # 鼠标拖入事件
    def dragEnterEvent(self, evn):
     #   self.setWindowTitle('鼠标拖入窗口了')
        self.editpath.setText(evn.mimeData().text().split('///')[-1])
        #鼠标放开函数事件
        evn.accept()

    def dropEvent(self, evn):
        self.determine()

            
    def determine(self):
        print("enter determine")
        print("enter controller.cleanedit()")
        self.controller.cleanedit()
        print("exit controller.cleanedit()")
        self.controller.setDisplay()
        print("exit determine")

    def prompt(self,Infotype,information):
        
        if Infotype is 'analyzeError':
            QMessageBox.warning(self,"Error", information)
        
