import sys
import os
from pathlib import Path
import cv2
import json
import random
import string
from datetime import datetime

from PyQt5.QtWidgets import (QMainWindow, QApplication, QLabel, QPushButton, 
                             QComboBox, QSlider, QRadioButton, QLineEdit, 
                             QButtonGroup, QFileDialog, QMessageBox, QInputDialog)
from PyQt5 import uic
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import Qt
from src.hsv_filter import HSVFilter
from src.webcam import Webcam
from src.image import Image
from src.video import Video


class HSVFilterUI(QMainWindow):
    def __init__(self, main_window):
        super(HSVFilterUI, self).__init__()
        self.main_window = main_window
        self.load_ui()
        self.load_event()
        
        # Object
        self.changing_colorspace_lib = HSVFilter()
        self.dict_colors = self.changing_colorspace_lib.color_dict_HSV
        self.set_value_combo_samples()
        self.choose_mode()
        
        self.video, self.webcam, self.img = None, None, None
        self.path_media = ''
        self.show()
        

    def save_config(self):
        hl, sl, vl, hu, su, vu = self.get_value_hsv_range()

        # Hộp thoại nhập tên file
        config_file_name, ok = QInputDialog.getText(self, 'Save Config', 'Enter config file name (without extension):')
        if ok and config_file_name:
            config_file_name = f"{config_file_name}.txt"  # Thêm đuôi file .txt
            # Lưu cấu hình vào thư mục config
            config_data = {
                "HL": hl,
                "SL": sl,
                "VL": vl,
                "HU": hu,
                "SU": su,
                "VU": vu,
            }
            with open(f"assets/config/{config_file_name}", "w") as config_file:  # Thay đổi đường dẫn lưu
                json.dump(config_data, config_file)
            
            QMessageBox.information(self, "Success", f"Configuration saved successfully as {config_file_name}.")
        

    def load_ui(self, path_ui='./ui/hsv_filter.ui'):
        uic.loadUi(path_ui, self)
        self.init_ui_elements()
        
        
    def init_ui_elements(self):
        # Initialize UI components
        self.radioButtonWebcam = self.findChild(QRadioButton, 'radioButtonWebcam')
        self.radioButtonVideo = self.findChild(QRadioButton, 'radioButtonVideo')
        self.radioButtonImage = self.findChild(QRadioButton, 'radioButtonImage')
        
        self.lineEditChooseFile = self.findChild(QLineEdit, 'lineEditChooseFile')
        self.pushButtonChooseFile = self.findChild(QPushButton, 'pushButtonChooseFile')
        self.pushButtonApplyFile = self.findChild(QPushButton, 'pushButtonApplyFile')
        
        self.labelShow = self.findChild(QLabel, 'labelShow')
        self.labelShow.setStyleSheet("border: 2px solid gray;")
        
        self.radioButtonOriginal = self.findChild(QRadioButton, 'radioButtonOriginal')
        self.radioButtonMask = self.findChild(QRadioButton, 'radioButtonMask')
        
        self.horizontalSliders = {
            'HL': self.findChild(QSlider, 'horizontalSliderHL'),
            'SL': self.findChild(QSlider, 'horizontalSliderSL'),
            'VL': self.findChild(QSlider, 'horizontalSliderVL'),
            'HU': self.findChild(QSlider, 'horizontalSliderHU'),
            'SU': self.findChild(QSlider, 'horizontalSliderSU'),
            'VU': self.findChild(QSlider, 'horizontalSliderVU')
        }
        
        self.labels = {
            'HL': self.findChild(QLabel, 'labelHL'),
            'SL': self.findChild(QLabel, 'labelSL'),
            'VL': self.findChild(QLabel, 'labelVL'),
            'HU': self.findChild(QLabel, 'labelHU'),
            'SU': self.findChild(QLabel, 'labelSU'),
            'VU': self.findChild(QLabel, 'labelVU')
        }
        
        self.comboBoxSamples = self.findChild(QComboBox, 'comboBoxSamples')
        self.pushButtonSaveConfig = self.findChild(QPushButton, 'pushButtonSaveConfig')
        self.pushButtonLoadConfig = self.findChild(QPushButton, 'pushButtonLoadConfig') 
        self.pushButtonApply = self.findChild(QPushButton, 'pushButtonApply')
        self.pushButtonBack = self.findChild(QPushButton, 'pushButtonBack')

        # Initialize button groups
        self.group_type = QButtonGroup()
        self.group_view = QButtonGroup()
        self.group_type.addButton(self.radioButtonWebcam)
        self.group_type.addButton(self.radioButtonVideo)
        self.group_type.addButton(self.radioButtonImage)
        self.group_view.addButton(self.radioButtonOriginal)
        self.group_view.addButton(self.radioButtonMask)


    def load_event(self):
        # Connect signals to slots
        self.pushButtonApply.clicked.connect(self.apply_sample_color)
        self.pushButtonBack.clicked.connect(self.back_to_main)
        self.pushButtonChooseFile.clicked.connect(self.open_file_dialog)
        self.pushButtonApplyFile.clicked.connect(self.apply_file)
        
        self.pushButtonSaveConfig.clicked.connect(self.save_config)
        self.pushButtonLoadConfig.clicked.connect(self.load_config)
        
        # Connect slider value changes
        for key, slider in self.horizontalSliders.items():
            slider.valueChanged.connect(self.update_color_space)

        self.radioButtonWebcam.toggled.connect(self.choose_mode)
        self.radioButtonVideo.toggled.connect(self.choose_mode)
        self.radioButtonImage.toggled.connect(self.choose_mode)


    def set_value_combo_samples(self):
        example_colors = [f"{key_}: {self.dict_colors[key_][1]}-{self.dict_colors[key_][0]}" 
                          for key_ in self.dict_colors]
        self.comboBoxSamples.addItems(example_colors)


    def get_value_hsv_range(self):
        return [int(slider.value()) for slider in self.horizontalSliders.values()]


    def choose_mode(self):
        is_video_or_image = not self.radioButtonWebcam.isChecked()
        self.lineEditChooseFile.setDisabled(not is_video_or_image)
        self.pushButtonChooseFile.setDisabled(not is_video_or_image)
        self.id_mode = 0 if self.radioButtonWebcam.isChecked() else (1 if self.radioButtonVideo.isChecked() else 2)


    def show_message_box(self, title='Error', content='Please select a file path'):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle(title)
        msg.setText(content)
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()


    def open_file_dialog(self):
        current_path = Path(os.getcwd())
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_filters = {
            1: "MP4 Files (*.mp4)",
            2: "Image Files (*.png *.jpeg *.jpg)"
        }
        filter_type = file_filters.get(self.id_mode, "")
        file_name, _ = QFileDialog.getOpenFileName(self, "Select File", str(current_path / 'media'), filter_type, options=options)

        if file_name:
            self.lineEditChooseFile.setText(file_name)
            self.path_media = file_name
            
            
    def load_config(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_name, _ = QFileDialog.getOpenFileName(self, "Select Config File", "assets/config", "Config Files (*.txt);;All Files (*)", options=options)

        if file_name:
            try:
                with open(file_name, "r") as config_file:
                    config_data = json.load(config_file)

                # Cập nhật giá trị cho các slider
                for key in ['HL', 'SL', 'VL', 'HU', 'SU', 'VU']:
                    if key in config_data:
                        slider = self.horizontalSliders[key]
                        slider.setSliderPosition(config_data[key])
                        self.labels[key].setText(str(config_data[key]))

                # Cập nhật không gian màu
                self.update_color_space()
                QMessageBox.information(self, "Success", "Configuration loaded successfully.")

            except FileNotFoundError:
                QMessageBox.critical(self, "Error", "Config file not found.")
            except json.JSONDecodeError:
                QMessageBox.critical(self, "Error", "Error reading the config file.")


    def apply_file(self):
        if not self.path_media and self.id_mode != 0:
            self.show_message_box()
            return

        if self.video is not None: self.video.is_running = False
        if self.webcam is not None: self.webcam.is_running = False
        if self.img is not None: self.img.is_running = False

        if self.id_mode == 0:
            self.webcam = Webcam()
            self.show_webcam()
        elif self.id_mode == 1:
            self.video = Video(self.path_media)
            self.show_video()
        elif self.id_mode == 2:
            self.img = Image(self.path_media)
            self.show_image()


    def apply_sample_color(self):
        value = self.comboBoxSamples.currentText()
        key_ = value.split(':')[0]
        hl, sl, vl = self.dict_colors[key_][1]
        hu, su, vu = self.dict_colors[key_][0]

        # Set slider positions and labels
        for key, slider in self.horizontalSliders.items():
            if key in ['HL', 'SL', 'VL', 'HU', 'SU', 'VU']:
                slider.setSliderPosition(eval(key.lower()))
            self.labels[key].setText(str(eval(key.lower())))

        self.update_color_space()


    def back_to_main(self):
        if self.video is not None: self.video.is_running = False
        if self.webcam is not None: self.webcam.is_running = False
        if self.img is not None: self.img.is_running = False
        
        self.close()
        self.main_window.show()
        self.main_window.pushButtonApplyMode.setDisabled(False)


    def update_color_space(self):
        hl, sl, vl, hu, su, vu = self.get_value_hsv_range()

        # Ensure lower values do not exceed upper values
        if hl > hu: hl, hu = hu, hl
        if sl > su: sl, su = su, sl
        if vl > vu: vl, vu = vu, vl
        
        # Set slider positions and labels
        for key, slider in self.horizontalSliders.items():
            if key in ['HL', 'SL', 'VL', 'HU', 'SU', 'VU']:
                slider.setSliderPosition(eval(key.lower()))
            self.labels[key].setText(str(eval(key.lower())))

        self.changing_colorspace_lib.update_colorspaces(hl, sl, vl, hu, su, vu)


    def update_image(self, cv_img):
        """Updates the labelShow with a new OpenCV image"""
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
            rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        convert_to_Qt_format = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
        return QPixmap.fromImage(convert_to_Qt_format)


    def show_webcam(self):
        self.webcam.change_pixel_signal.connect(self.update_image)
        self.webcam.start()


    def show_video(self):
        self.img.change_pixel_signal.connect(self.update_image)
        self.img.start()
        
        
    def show_image(self):
        self.video.change_pixel_signal.connect(self.update_image)
        self.video.start()


def main():
    app = QApplication(sys.argv)
    UIChaningColorspaces = HSVFilterUI()
    app.exec_()
    
if __name__ == '__main__':
    main()
