import sys
sys.path.append('../.')

import cv2

import os
from pathlib import Path
from PyQt5.QtWidgets import  QRadioButton, QLineEdit, QButtonGroup, QFileDialog, QMessageBox, QFrame
from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel, QPushButton, QComboBox, QSlider
from PyQt5 import uic
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import Qt
from src.camera_calib import CameraCalib

from src.webcam import Webcam
from src.image import Image
from src.video import Video
import time

class CameraCalibrationUI(QMainWindow):
    def load_ui(self, path_ui='./ui/calibration_camera.ui'):
        uic.loadUi(path_ui, self)
        self.pushButtonBack =  self.findChild(QPushButton, 'pushButtonBack')
        
        self.frameSetting = self.findChild(QFrame, 'frameSetting')
        self.radioButtonCamera = self.frameSetting.findChild(QRadioButton, 'radioButtonCamera')
        self.radioButtonFolderImage = self.frameSetting.findChild(QRadioButton, 'radioButtonFolderImage')
        self.lineEditCW = self.frameSetting.findChild(QLineEdit, 'lineEditCW')
        self.lineEditCH = self.frameSetting.findChild(QLineEdit, 'lineEditCH')
        self.lineEditCBW = self.frameSetting.findChild(QLineEdit, 'lineEditCBW')
        self.lineEditCBH = self.frameSetting.findChild(QLineEdit, 'lineEditCBH')
        self.lineEditCBSS = self.frameSetting.findChild(QLineEdit, 'lineEditCBSS')
        self.pushButtonApply = self.frameSetting.findChild(QPushButton, 'pushButtonApply')
        
        self.labelView =  self.findChild(QLabel, 'labelView')
        self.frameShow = self.findChild(QFrame, 'frameShow')
        self.pushButtonExportConfig = self.findChild(QPushButton, 'pushButtonExportConfig')
        self.pushButtonLoadConfig =  self.findChild(QPushButton, 'pushButtonLoadConfig')
        
        
    def load_event(self):
        self.pushButtonBack.clicked.connect(self.evt_btBack_clicked)
        self.radioButtonCamera.toggled.connect(self.chooseMode)
        self.radioButtonFolderImage.toggled.connect(self.chooseMode)
        self.pushButtonApply.clicked.connect(self.evt_btApply_clicked)
        self.pushButtonExportConfig.clicked.connect(self.evt_btExportConfig_clicked)
        self.pushButtonLoadConfig.clicked.connect(self.evt_btLoadConfig_clicked)
    
    def __init__(self, main_window):
        super(CameraCalibrationUI, self).__init__()
        self.main_window = main_window
        self.load_ui()
        self.load_event()
        
        # Object
        self.camear_calib = CameraCalib()
        self.chooseMode()
        self.camera_calib = None
        self.image_calib = None
        self.path_media = ''
        self.show()
        
    def chooseMode(self):
        if self.radioButtonCamera.isChecked():
            self.id_mode = 0
        elif self.radioButtonFolderImage.isChecked():
            self.id_mode = 1


    def show_message_box(self, tittle='Error', content='Please select path file'):
        # Tạo hộp thoại thông báo
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle(tittle)
        msg.setText(content)
        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        
        # Hiển thị hộp thoại và xử lý nút bấm
        result = msg.exec_()
        if result == QMessageBox.Ok:
            self.camear_calib.is_continue = False
        elif result == QMessageBox.Cancel:
            self.camear_calib.is_continue = False

            
    def openFileNameDialog(self):
        current_path = Path(os.path.abspath(os.getcwd()))
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        if self.radioButtonVideo.isChecked():
            fileName, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", os.path.join(current_path, 'media'),"MP4 Files (*.mp4)", options=options)
        elif self.radioButtonImage.isChecked():
            fileName, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", os.path.join(current_path, 'media'),"Images Files (*.png *.jpeg *.jpg)", options=options)
        else:
            fileName = ''
        if fileName:
            self.lineEditChooseFile.setText(fileName)
            self.path_media = fileName
            
    def check_input(self):
        try:
            self.cw = int(self.lineEditCW.text())
            self.ch = int(self.lineEditCH.text())
            self.cbw = int(self.lineEditCBW.text())
            self.cbh = int(self.lineEditCBH.text())
            self.cbss = float(self.lineEditCBSS.text())
            return True
        except Exception as e:
            return False
            
    def evt_btChooseFile_clicked(self):
        self.openFileNameDialog()
        
    def evt_btApply_clicked(self):
        if not self.check_input():
            self.show_message_box(content='Input error. Re-check')
        else:
            if self.id_mode == 0:
                self.camear_calib = CameraCalib(w=self.cw, h=self.ch)
                self.camear_calib.change_pixel_signal.connect(self.update_image)
                self.camear_calib.info_update.connect(self.update_info)
                self.camear_calib.start()
            elif self.id_mode == 1:
                self.video = Video(self.path_media)
                pass
       
    def evt_btBack_clicked(self):
        self.close()
        self.main_window.show()
        self.main_window.pushButtonApplyMode.setDisabled(False)
        
    def evt_btExportConfig_clicked(self):
        pass
    
    def evt_btLoadConfig_clicked(self):
        pass
    
        
    def update_image(self, cv_img):
        """Updates the image_label with a new opencv image"""
        qt_img = self.convert_cv_qt(cv_img)
        self.labelView.setPixmap(qt_img)
        self.labelView.setScaledContents(True)
        
    def update_info(self, info):
        epoch, max_epoch = info
        self.show_message_box('Complete','{}/{}'.format(epoch, max_epoch))
    
    def convert_cv_qt(self, cv_img):
        """Convert from an opencv image to QPixmap"""
        rgb_image =  cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        convert_to_Qt_format = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
        return QPixmap.fromImage(convert_to_Qt_format)
        

def main():
    app = QApplication(sys.argv)
    CameraCalibrationUI = CameraCalibrationUI()
    app.exec_()
    
if __name__ == '__main__':
    main()
    