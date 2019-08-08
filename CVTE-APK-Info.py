import sys
import re
import os
import hashlib
import subprocess
import zipfile
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from CVTE_View import CVTE_View
from CVTE_Controller import CVTE_Controller
from CVTE_Model import CVTE_Model

def Main():
    app = QApplication(sys.argv)

    Model = CVTE_Model()
    Controller = CVTE_Controller()
    View = CVTE_View()

    Model.controller = Controller
    Model.view = View

    Controller.model = Model
    Controller.view = View

    View.controller = Controller
    View.model = Model

    sys.exit(app.exec_())
                
if __name__ == "__main__":
    Main()

