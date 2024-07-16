import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QHBoxLayout, QVBoxLayout, QFileDialog, QListWidget, QRadioButton
from PyQt5.QtWidgets import QApplication, QComboBox, QProgressBar, QTextEdit, QSlider,  QMessageBox
from PyQt5.QtCore import Qt

class SMTUI(QWidget):
    def __init__(self):
        super().__init__()
        
        self.init_ui()
        
    def init_ui(self):
        # Tạo các thành phần giao diện
        self.label_1 = QLabel('ROBOT SMT FRING LED v2.0', self)
        self.label_2 = QLabel('Select type pannel', self)
        self.comboBoxTypePannelAll = QComboBox(self)
        self.list_pannel = ['RGB', 'FRING', 'UDISC']
        self.comboBoxTypePannelAll.addItems(self.list_pannel)
        self.comboBoxTypePannelAll.setCurrentIndex(0)
        self.pushButtonApplyTypePannel = QPushButton('Apply')
        self.labelMachineConnection = QLabel('Machine connection', self)
        self.labelFeederConnection  =  QLabel('Feeder connection', self)
        self.labelCameraConnection = QLabel('Camera connection', self)
        self.pushButtonMachineConnection =  QPushButton('Connect')
        self.label_3 = QLabel('Type pannel', self)
        self.comboBoxTypePannel = QComboBox(self)
        self.list_type = (['FULL', 'HALF'])
        self.comboBoxTypePannel.addItems(self.list_type)
        self.comboBoxTypePannel.setCurrentIndex(0)
        self.radioButtonDefault =  QRadioButton('Default')
        self.radioButtonCustomizeRC =  QRadioButton('Customize')
        self.radioButtonDebug =  QRadioButton('Debug')
        self.label_4 = QLabel('Pannel', self)
        self.label_5 = QLabel('Col', self)
        self.label_6 = QLabel('Row', self)
        self.textEditPannel = QTextEdit(self)
        self.textEditCol = QTextEdit(self)
        self.textEditRow = QTextEdit(self)
        self.label_7 = QLabel('Offset X', self)
        self.label_8 = QLabel('Offset Y', self)
        self.horizontalSliderX = QSlider(self)
        self.horizontalSliderX.setOrientation(Qt.Horizontal)
        self.horizontalSliderY = QSlider(self)
        self.horizontalSliderY.setOrientation(Qt.Horizontal)
        self.labelOffsetX  = QLabel('0.0', self)
        self.labelOffsetY  = QLabel('0.0', self)

        
        # Label layout
        label_layout = QHBoxLayout()
        label_layout.addWidget(self.label_1)
        
        # Select type layout
        select_type_layout = QHBoxLayout()
        select_type_layout.addWidget(self.label_2)
        select_type_layout.addWidget(self.comboBoxTypePannelAll)
        select_type_layout.addWidget(self.pushButtonApplyTypePannel)
        select_type_layout.setStretch(0, 2)
        select_type_layout.setStretch(1, 6)
        select_type_layout.setStretch(2, 2)
        
        # Connection layout
        connection_layout1 = QVBoxLayout()
        connection_layout1.addWidget(self.labelMachineConnection)
        connection_layout1.addWidget(self.labelFeederConnection)
        connection_layout1.addWidget(self.labelCameraConnection)
        
        connection_layout2 = QVBoxLayout()
        connection_layout2.addWidget(self.pushButtonMachineConnection)
        
        connection_layout = QHBoxLayout()
        connection_layout.addLayout(connection_layout1)
        connection_layout.addLayout(connection_layout2)
        connection_layout.setStretch(0, 5)
        connection_layout.setStretch(1, 5)
        
        # Customize option
        cus_layout1 = QHBoxLayout()
        cus_layout1.addWidget(self.label_3)
        cus_layout1.addWidget(self.comboBoxTypePannel)
        cus_layout1.setStretch(0, 2)
        cus_layout1.setStretch(1, 8)
        
        cus_layout2 = QHBoxLayout()
        cus_layout2.addWidget(self.radioButtonDefault)
        
        cus_layout30 = QHBoxLayout()
        cus_layout30.addWidget(self.radioButtonCustomizeRC)
        
        cus_layout31 = QHBoxLayout()
        cus_layout31.addWidget(self.label_4)
        cus_layout31.addWidget(self.textEditPannel)
        cus_layout31.addWidget(self.label_5)
        cus_layout31.addWidget(self.textEditCol)
        cus_layout31.addWidget(self.label_6)
        cus_layout31.addWidget(self.textEditRow)
        
        
        cus_layout42 = QHBoxLayout()
        cus_layout42.addWidget(self.label_7)
        cus_layout42.addWidget(self.horizontalSliderX)
        cus_layout42.addWidget(self.labelOffsetX)
        
        cus_layout43 = QHBoxLayout()
        cus_layout43.addWidget(self.label_8)
        cus_layout43.addWidget(self.horizontalSliderY)
        cus_layout43.addWidget(self.labelOffsetY)
        
        cus_layout5 = QHBoxLayout()
        cus_layout5.addWidget(self.radioButtonDebug)
        
        custom_option_layout = QVBoxLayout()
        # custom_option_layout.
        
        # Main layout
        main_layout = QVBoxLayout()
        main_layout.addLayout(label_layout)
        main_layout.addLayout(select_type_layout)
        main_layout.addLayout(connection_layout)
        # main_layout.addLayout(connection_layout)
        
        connection_layout.setStretch(0, 2)
        connection_layout.setStretch(1, 5)
        connection_layout.setStretch(2, 3)
        
        self.setLayout(main_layout)
        self.setWindowTitle('SMT')
        self.setGeometry(300, 300, 800, 400)
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    folder_selection = SMTUI()
    folder_selection.show()
    sys.exit(app.exec_())
