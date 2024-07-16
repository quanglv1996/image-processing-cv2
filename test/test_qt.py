import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QVBoxLayout, QHBoxLayout

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Main Window')
        
        # Create layout
        self.layout = QVBoxLayout()

        # Create buttons
        self.ok_button = QPushButton('OK', self)
        self.cancel_button = QPushButton('Cancel', self)
        
        # Connect buttons to functions
        self.ok_button.clicked.connect(self.show_second_window)
        self.cancel_button.clicked.connect(self.close)

        # Add buttons to layout
        self.layout.addWidget(self.ok_button)
        self.layout.addWidget(self.cancel_button)

        self.setLayout(self.layout)

    def show_second_window(self):
        self.second_window = SecondWindow(self)
        self.second_window.show()
        self.hide()


class SecondWindow(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Second Window')
        
        # Create layout
        self.layout = QVBoxLayout()

        # Create label and back button
        self.label = QLabel('Xin chào', self)
        self.back_button = QPushButton('Back', self)
        
        # Connect back button to function
        self.back_button.clicked.connect(self.show_main_window)

        # Add widgets to layout
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.back_button)

        self.setLayout(self.layout)

    def show_main_window(self):
        self.main_window.show()
        self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())

def openFileNameDialog(self):
    current_path = Path(os.path.abspath(os.getcwd()))
    # parrent_path = current_path.parent.absolute()
    # print(parrent_path)
    options = QFileDialog.Options()
    options |= QFileDialog.DontUseNativeDialog
    if self.radioButtonVideo.isChecked():
        fileName, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", os.path.join(current_path, 'media'),"MP4 Files (*.mp4)", options=options)
    elif self.radioButtonImage.isChecked():
        fileName, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", os.path.join(current_path, 'media'),"Images Files (*.png *.jpeg *.jpg)", options=options)
    else:
        fileName = ''
    if fileName:
        self.textBrowserChooseFile.setText(fileName)
        self.path_media = fileName
        self.pushButtonApplyMode.setDisabled(False)