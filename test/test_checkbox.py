import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QCheckBox, QLabel

class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        
        self.initUI()

    def initUI(self):
        # Tạo layout
        layout = QVBoxLayout()
        
        # Tạo một QLabel để hiển thị trạng thái
        self.label = QLabel("Chọn hoặc bỏ chọn hộp kiểm", self)
        
        # Tạo một QCheckBox
        self.checkbox = QCheckBox("Chọn tôi", self)
        
        # Kết nối tín hiệu stateChanged với hàm xử lý
        self.checkbox.stateChanged.connect(self.on_checkbox_state_changed)
        
        # Thêm các widget vào layout
        layout.addWidget(self.label)
        layout.addWidget(self.checkbox)

        # Thiết lập layout cho widget
        self.setLayout(layout)

        # Cài đặt tiêu đề và kích thước cửa sổ
        self.setWindowTitle('QCheckBox Example')
        self.setGeometry(100, 100, 300, 200)

    def on_checkbox_state_changed(self, state):
        print(state)
        # Kiểm tra trạng thái của QCheckBox
        if state == 0:
            self.label.setText("Hộp kiểm chưa được chọn")
        elif state == 1:
            self.label.setText("Hộp kiểm đã được chọn")
        elif state == 2:  # Trạng thái 2 cho trạng thái "trộn lẫn"
            self.label.setText("Hộp kiểm ở trạng thái trộn lẫn")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    ex.show()
    sys.exit(app.exec_())
