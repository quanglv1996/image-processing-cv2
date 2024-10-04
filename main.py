import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QRadioButton
from PyQt5 import uic
from src.hsv_filter_ui import HSVFilterUI
from src.camera_calib_ui import CameraCalibrationUI
from src.sharpness_analyzer_ui import SharpnessAnalyzerUI

class MainUI(QMainWindow):
    def __init__(self):
        super(MainUI, self).__init__()

        # Load the ui file
        uic.loadUi('./ui/main.ui', self)

        # Define widgets
        self.radio_buttons = [
            self.findChild(QRadioButton, 'radioButtonHSVFilter'),
            self.findChild(QRadioButton, 'radioButtonCalibration'),
            self.findChild(QRadioButton, 'radioButtonImageProcessing'),
            self.findChild(QRadioButton, 'radioButtonSharpnessAnalyzer'),
        ]
        self.pushButtonApplyMode = self.findChild(QPushButton, 'pushButtonApplyMode')

        # Connect signals
        for radio_button in self.radio_buttons:
            radio_button.toggled.connect(self.chooseMode)

        self.pushButtonApplyMode.clicked.connect(self.open_window)

        # Show the app
        self.show()

    def open_window(self):
        # List of UI classes corresponding to each radio button
        ui_classes = [HSVFilterUI, CameraCalibrationUI, HSVFilterUI, SharpnessAnalyzerUI]

        # Get selected mode and create corresponding UI
        selected_index = self.get_selected_mode()
        if selected_index is not None:
            self.ui = ui_classes[selected_index](self)
            self.hide()

    def chooseMode(self):
        """Sets the selected mode ID based on which radio button is checked."""
        self.id_mode = self.get_selected_mode()

    def get_selected_mode(self):
        """Returns the index of the selected radio button, or None if none are selected."""
        for index, radio_button in enumerate(self.radio_buttons):
            if radio_button.isChecked():
                return index
        return None  # No radio button is checked

def main():
    app = QApplication(sys.argv)
    UIMain = MainUI()
    app.exec_()

if __name__ == '__main__':
    main()
