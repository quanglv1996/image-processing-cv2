import sys
sys.path.append('../.')

import os
from pathlib import Path

from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QLabel, QRadioButton
from PyQt5 import uic

from src.changing_colorspace_ui import ChangingColorspacesUI

class MainUI(QMainWindow):
    def __init__(self):
        super(MainUI, self).__init__()
        
        # Load the ui file
        uic.loadUi('./ui/main.ui', self)
        
        # Define widgets
        self.radioButtonHSVFilter = self.findChild(QRadioButton, 'radioButtonHSVFilter')
        self.radioButtonCalibration = self.findChild(QRadioButton, 'radioButtonCalibration')
        self.radioButtonImageProcessing = self.findChild(QRadioButton, 'radioButtonImageProcessing')
        self.pushButtonApplyMode = self.findChild(QPushButton, 'pushButtonApplyMode')
        
        # Object
        self.radioButtonHSVFilter.toggled.connect(self.chooseMode)
        self.radioButtonCalibration.toggled.connect(self.chooseMode)
        self.radioButtonImageProcessing.toggled.connect(self.chooseMode)
        
        self.pushButtonApplyMode.clicked.connect(self.open_window)
        
        # Action
        self.id_mode = 0
        
        # Show the app
        self.show()
        
    def open_window(self):
        if self.id_mode == 0:
            self.ui = ChangingColorspacesUI()
        elif self.id_mode == 1:
            self.ui = ChangingColorspacesUI()
        elif self.id_mode == 2:
            self.ui = ChangingColorspacesUI()
        self.hide()
        
    def chooseMode(self):
        if self.radioButtonHSVFilter.isChecked():
            self.id_mode = 0
        elif self.radioButtonCalibration.isChecked():
            self.id_mode = 1
        elif self.radioButtonImageProcessing.isChecked():
            self.id_mode = 2
        
def main():
    app = QApplication(sys.argv)
    UIMain = MainUI()
    app.exec_()
    
if __name__ == '__main__':
    main()