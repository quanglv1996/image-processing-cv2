import sys
sys.path.append('../.')

import cv2

import os
from pathlib import Path
from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel, QPushButton, QComboBox, QSlider, QRadioButton, QLineEdit, QButtonGroup, QFileDialog, QMessageBox
from PyQt5 import uic
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import Qt
from src.hsv_filter import HSVFilter

from src.webcam import Webcam
from src.image import Image
from src.video import Video

class HSVFilterUI(QMainWindow):
    def load_ui(self, path_ui='./ui/changing_colorspace.ui'):
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
        
        self.radioButtonOriginal = self.findChild(QRadioButton, 'radioButtonOriginal')
        self.radioButtonMask = self.findChild(QRadioButton, 'radioButtonMask')
        self.group_view = QButtonGroup()
        self.group_view.addButton(self.radioButtonOriginal)
        self.group_view.addButton(self.radioButtonMask)
        
        self.horizontalSliderHL = self.findChild(QSlider, 'horizontalSliderHL')
        self.horizontalSliderSL = self.findChild(QSlider, 'horizontalSliderSL')
        self.horizontalSliderVL = self.findChild(QSlider, 'horizontalSliderVL')
        
        self.horizontalSliderHU = self.findChild(QSlider, 'horizontalSliderHU')
        self.horizontalSliderSU = self.findChild(QSlider, 'horizontalSliderSU')
        self.horizontalSliderVU = self.findChild(QSlider, 'horizontalSliderVU')
        
        self.labelHL = self.findChild(QLabel, 'labelHL')
        self.labelSL = self.findChild(QLabel, 'labelSL')
        self.labelVL = self.findChild(QLabel, 'labelVL')
        
        self.labelHU = self.findChild(QLabel, 'labelHU')
        self.labelSU = self.findChild(QLabel, 'labelSU')
        self.labelVU = self.findChild(QLabel, 'labelVU')
        
        self.comboBoxSamples = self.findChild(QComboBox, 'comboBoxSamples')
        self.pushButtonApply = self.findChild(QPushButton, 'pushButtonApply')
        self.pushButtonBack = self.findChild(QPushButton, 'pushButtonBack')
        
    def load_event(self):
        self.pushButtonApply.clicked.connect(self.evt_btApply_clicked)
        self.pushButtonBack.clicked.connect(self.evt_btBack_clicked)
        self.horizontalSliderHL.valueChanged.connect(self.valueChangeHueLow)
        self.horizontalSliderSL.valueChanged.connect(self.valueChangeSaturationLow)
        self.horizontalSliderVL.valueChanged.connect(self.valueChangeValueLow)
        self.horizontalSliderHU.valueChanged.connect(self.valueChangeHueUpper)
        self.horizontalSliderSU.valueChanged.connect(self.valueChangeSaturationUpper)
        self.horizontalSliderVU.valueChanged.connect(self.valueChangeValueUpper)
        self.radioButtonWebcam.toggled.connect(self.chooseMode)
        self.radioButtonVideo.toggled.connect(self.chooseMode)
        self.radioButtonImage.toggled.connect(self.chooseMode)
        self.pushButtonApplyFile.clicked.connect(self.evt_btApplyFile_clicked)
        self.pushButtonChooseFile.clicked.connect(self.evt_btChooseFile_clicked)
    
    def set_value_combox_samples(self):
        example_colors = []
        for key_ in self.dict_colors:
            example_colors.append('{}: {}-{}'.format(key_, self.dict_colors[key_][1], self.dict_colors[key_][0]))
        self.comboBoxSamples.addItems(example_colors)
    
    def __init__(self, main_window):
        super(HSVFilterUI, self).__init__()
        self.main_window = main_window
        self.load_ui()
        self.load_event()
        
        # Object
        self.changing_colorspace_lib = HSVFilter()
        self.dict_colors = self.changing_colorspace_lib.color_dict_HSV
        self.set_value_combox_samples()
        self.chooseMode()
        self.video = None
        self.webcam = None
        self.img = None
        self.path_media = ''
        self.show()
        
    def getValueHSVRange(self):
        h_low = self.horizontalSliderHL.value()
        s_low = self.horizontalSliderSL.value()
        v_low = self.horizontalSliderVL.value()
        h_upper = self.horizontalSliderHU.value()
        s_upper = self.horizontalSliderSU.value()
        v_upper = self.horizontalSliderVU.value()
        return [h_low, s_low, v_low, h_upper, s_upper, v_upper]
    
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

    def evt_btApply_clicked(self):
        value = self.comboBoxSamples.currentText()
        key_ = value.split(':')[0]
        
        hl, sl, vl = self.dict_colors[key_][1]
        hu, su, vu = self.dict_colors[key_][0]
        
        self.horizontalSliderHL.setSliderPosition(hl)
        self.horizontalSliderSL.setSliderPosition(sl)
        self.horizontalSliderVL.setSliderPosition(vl)
        self.horizontalSliderHU.setSliderPosition(hu)
        self.horizontalSliderSU.setSliderPosition(su)
        self.horizontalSliderVU.setSliderPosition(vu)
        
        self.labelHL.setText(str(hl))
        self.labelSL.setText(str(sl))
        self.labelVL.setText(str(vl))
        self.labelHU.setText(str(hu))
        self.labelSU.setText(str(su))
        self.labelVU.setText(str(vu))
        
        hl, sl, vl, hu, su, vu = self.get_spacecolor_from_slider()
        self.changing_colorspace_lib.update_colorspaces(hl, sl, vl, hu, su, vu)
        
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
        
    
    def get_spacecolor_from_slider(self):
        hl = int(self.horizontalSliderHL.value())
        sl = int(self.horizontalSliderSL.value())
        vl = int(self.horizontalSliderVL.value())
        hu = int(self.horizontalSliderHU.value())
        su = int(self.horizontalSliderSU.value())
        vu = int(self.horizontalSliderVU.value())
        return hl, sl, vl, hu, su, vu
    
    def valueChangeHueLow(self):
        text = str(self.horizontalSliderHL.value())
        self.labelHL.setText(text)
        hl, sl, vl, hu, su, vu = self.get_spacecolor_from_slider()
        self.changing_colorspace_lib.update_colorspaces(hl, sl, vl, hu, su, vu)
        
    def valueChangeHueUpper(self):
        text = str(self.horizontalSliderHU.value())
        self.labelHU.setText(text)
        hl, sl, vl, hu, su, vu = self.get_spacecolor_from_slider()
        self.changing_colorspace_lib.update_colorspaces(hl, sl, vl, hu, su, vu)
        
    def valueChangeSaturationLow(self):
        text =  str(self.horizontalSliderSL.value())
        self.labelSL.setText(text)
        hl, sl, vl, hu, su, vu = self.get_spacecolor_from_slider()
        self.changing_colorspace_lib.update_colorspaces(hl, sl, vl, hu, su, vu)
    
    def valueChangeSaturationUpper(self):
        text = str(self.horizontalSliderSU.value())
        self.labelSU.setText(text)
        hl, sl, vl, hu, su, vu = self.get_spacecolor_from_slider()
        self.changing_colorspace_lib.update_colorspaces(hl, sl, vl, hu, su, vu)
    
    def valueChangeValueLow(self):
        text = str(self.horizontalSliderVL.value())
        self.labelVL.setText(text)
        hl, sl, vl, hu, su, vu = self.get_spacecolor_from_slider()
        self.changing_colorspace_lib.update_colorspaces(hl, sl, vl, hu, su, vu)
    
    def valueChangeValueUpper(self):
        text = str(self.horizontalSliderVU.value())
        self.labelVU.setText(text)
        hl, sl, vl, hu, su, vu = self.get_spacecolor_from_slider()
        self.changing_colorspace_lib.update_colorspaces(hl, sl, vl, hu, su, vu)
        
    def update_image(self, cv_img):
        """Updates the image_label with a new opencv image"""
        if not self.radioButtonOriginal.isChecked():
            cv_img = self.changing_colorspace_lib.run(cv_img)
        qt_img = self.convert_cv_qt(cv_img)
        self.labelShow.setPixmap(qt_img)
        self.labelShow.setScaledContents(True)
    
    def convert_cv_qt(self, cv_img):
        """Convert from an opencv image to QPixmap"""
        if not self.radioButtonOriginal.isChecked():
            rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_GRAY2RGB)
        else:
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
    UIChaningColorspaces = HSVFilterUI()
    app.exec_()
    
if __name__ == '__main__':
    main()
    