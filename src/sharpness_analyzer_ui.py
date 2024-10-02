import sys
sys.path.append('../.')

import cv2

import os
import time
from pathlib import Path
from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel, QPushButton, QRadioButton, QLineEdit, QButtonGroup, QFileDialog, QMessageBox, QCheckBox, QProgressBar
from PyQt5 import uic
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import Qt
from src.sharpness_analyzer  import CameraSharpnessAnalyzer

from src.webcam import Webcam
from src.image import Image
from src.video import Video

class SharpnessAnalyzerUI(QMainWindow):
    def load_ui(self, path_ui='./ui/sharpness_analyzer.ui'):
        uic.loadUi(path_ui, self)
        self.radioButtonWebcam = self.findChild(QRadioButton, 'radioButtonWebcam')
        self.radioButtonVideo = self.findChild(QRadioButton, 'radioButtonVideo')
        self.radioButtonImage = self.findChild(QRadioButton,'radioButtonImage')
        self.lineEditChooseFile = self.findChild(QLineEdit, 'lineEditChooseFile')
        self.group_type = QButtonGroup()
        self.group_type.addButton(self.radioButtonWebcam)
        self.group_type.addButton(self.radioButtonVideo)
        self.group_type.addButton(self.radioButtonImage)
        
        self.pushButtonChooseFile = self.findChild(QPushButton, 'pushButtonChooseFile')
        self.pushButtonApplyFile = self.findChild(QPushButton, 'pushButtonApplyFile')
        self.labelShow = self.findChild(QLabel, 'labelShow')
        self.labelShow.setStyleSheet("border: 2px solid gray;")
        
        self.pushButtonBack = self.findChild(QPushButton, 'pushButtonBack')
        
        self.checkBoxLaplacian = self.findChild(QCheckBox, 'checkBoxLaplacian')
        self.progressBarLaplacian =  self.findChild(QProgressBar, 'progressBarLaplacian')
        
        self.checkBoxSobel = self.findChild(QCheckBox, 'checkBoxSobel')
        self.progressBarSobel =  self.findChild(QProgressBar, 'progressBarSobel')
        
        
    def load_event(self):
        self.pushButtonBack.clicked.connect(self.evt_btBack_clicked)
        self.radioButtonWebcam.toggled.connect(self.chooseMode)
        self.radioButtonVideo.toggled.connect(self.chooseMode)
        self.radioButtonImage.toggled.connect(self.chooseMode)
        self.pushButtonApplyFile.clicked.connect(self.evt_btApplyFile_clicked)
        self.pushButtonChooseFile.clicked.connect(self.evt_btChooseFile_clicked)
      
        
    
    def __init__(self, main_window):
        super(SharpnessAnalyzerUI, self).__init__()
        self.main_window = main_window
        self.load_ui()
        self.load_event()
        
        # Object
        self.sharpness_analyzer = CameraSharpnessAnalyzer()
        self.chooseMode()
        self.video = None
        self.webcam = None
        self.img = None
        self.path_media = ''
        self.show()
        
        self.sharpness_values = None
        
    
    def chooseMode(self):
        if self.radioButtonWebcam.isChecked():
            self.id_mode = 0
            self.lineEditChooseFile.setDisabled(True)
            self.pushButtonChooseFile.setDisabled(True)
        elif self.radioButtonVideo.isChecked():
            self.id_mode = 1
            self.lineEditChooseFile.setDisabled(False)
            self.pushButtonChooseFile.setDisabled(False)
        elif self.radioButtonImage.isChecked():
            self.id_mode = 2
            self.lineEditChooseFile.setDisabled(False)
            self.pushButtonChooseFile.setDisabled(False)
            
    def show_message_box(self, tittle='Error', content='Please select path file'):
        # Tạo hộp thoại thông báo
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle(tittle)
        msg.setText(content)
        msg.setStandardButtons(QMessageBox.Ok)
        
        # Hiển thị hộp thoại
        msg.exec_()

            
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
            
    def evt_btChooseFile_clicked(self):
        self.openFileNameDialog()
        
    def evt_btApplyFile_clicked(self):
        if self.path_media == '' and self.id_mode != 0:
            self.show_message_box()
        else:
            if self.video is not None:
                self.video.is_running = False
            if self.webcam is not None:
                self.webcam.is_running = False
            if self.img is not None:
                self.img.is_running = False
                
            if self.id_mode == 0:
                self.webcam = Webcam()
                self.showWebcam()
            elif self.id_mode == 1:
                self.video = Video(self.path_media)
                self.showVideo()
            elif self.id_mode == 2:
                self.img = Image(self.path_media)
                self.showImage()
                
        
    def evt_btBack_clicked(self):
        if self.video is not None:
            self.video.is_running = False
        if self.webcam is not None:
            self.webcam.is_running = False
        if self.img is not None:
            self.img.is_running = False
        self.close()
        self.main_window.show()
        self.main_window.pushButtonApplyMode.setDisabled(False)
        
    def processing(self, img):
        self.sharpness_values = self.sharpness_analyzer.get_sharpness_values_percent(img)
        if self.checkBoxLaplacian.isChecked():
            self.progressBarLaplacian.setValue(self.sharpness_values['Laplacian'])
            self.progressBarLaplacian.setDisabled(False)
        else:
            self.progressBarLaplacian.setValue(0)
            self.progressBarLaplacian.setDisabled(True)
        
        if self.checkBoxSobel.isChecked():
            self.progressBarSobel.setValue(self.sharpness_values['Sobel'])
            self.progressBarSobel.setDisabled(False)
        else:
            self.progressBarSobel.setValue(0)
            self.progressBarSobel.setDisabled(True)
    
        
    def update_image(self, cv_img):
        """Updates the image_label with a new opencv image"""
        self.processing(cv_img)
        qt_img = self.convert_cv_qt(cv_img)
        self.labelShow.setPixmap(qt_img)
        self.labelShow.setScaledContents(True)
    
    
    def convert_cv_qt(self, cv_img):
        """Convert from an opencv image to QPixmap"""
        rgb_image =  cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        convert_to_Qt_format = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
        return QPixmap.fromImage(convert_to_Qt_format)
        
        
    def showWebcam(self):
        self.webcam.change_pixel_signal.connect(self.update_image)
        self.webcam.start()
        
    def showImage(self):
        self.img.change_pixel_signal.connect(self.update_image)
        self.img.start()
        
    def showVideo(self):
        self.video.change_pixel_signal.connect(self.update_image)
        self.video.start()

def main():
    app = QApplication(sys.argv)
    sharpness_analyzer_UI = SharpnessAnalyzerUI()
    app.exec_()
    
if __name__ == '__main__':
    main()
    