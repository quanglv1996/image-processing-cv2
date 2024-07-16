import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QHBoxLayout, QVBoxLayout, QFileDialog, QListWidget, QRadioButton


class FolderSelection(QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        # Tạo các thành phần giao diện
        self.label = QLabel('Select folder', self)
        self.edit_text = QLineEdit(self)
        self.button = QPushButton('Choose', self)
        self.file_list = QListWidget(self)
        self.radio1 = QRadioButton("Option 1")
        self.radio2 = QRadioButton("Option 2")
        self.start_button = QPushButton('Start')
        self.stop_button = QPushButton('Stop')
        self.resume_button = QPushButton('Resume')

        # Sắp xếp các thành phần giao diện trên cùng một hàng
        top_layout = QHBoxLayout()
        top_layout.addWidget(self.label)
        top_layout.addWidget(self.edit_text)
        top_layout.addWidget(self.button)

        # Sắp xếp các nút radio bên dưới file_list
        radio_layout = QHBoxLayout()
        radio_layout.addWidget(self.radio1)
        radio_layout.addWidget(self.radio2)

        # Sắp xếp các thành phần giao diện tổng thể
        main_layout = QVBoxLayout()
        main_layout.addLayout(top_layout)
        main_layout.addWidget(self.file_list)
        main_layout.addLayout(radio_layout)

        # Sắp xếp các nút bấm Start, Stop, Resume theo chiều dọc
        button_layout = QVBoxLayout()
        button_layout.addWidget(self.start_button)
        button_layout.addWidget(self.stop_button)
        button_layout.addWidget(self.resume_button)
        button_layout.addStretch(1)  # Thêm khoảng trống để các nút không chiếm toàn bộ chiều cao

        # Tạo layout chính chứa main_layout và button_layout
        main_h_layout = QHBoxLayout()
        main_h_layout.addLayout(main_layout)
        main_h_layout.addLayout(button_layout)

        # Đặt tỉ lệ không gian: 2 phần cho main_layout, 1 phần cho button_layout
        main_h_layout.setStretch(0, 2)
        main_h_layout.setStretch(1, 1)

        self.setLayout(main_h_layout)

        # Kết nối nút chọn folder với hàm
        self.button.clicked.connect(self.choose_folder)

        # Cài đặt cửa sổ chính
        self.setWindowTitle('Folder Selection')
        self.setGeometry(300, 300, 800, 400)

    def choose_folder(self):
        # Hiển thị hộp thoại chọn folder và lấy đường dẫn folder đã chọn
        folder_path = QFileDialog.getExistingDirectory(self, 'Select Folder')

        # Hiển thị đường dẫn folder trong EditText
        if folder_path:
            self.edit_text.setText(folder_path)
            self.display_files(folder_path)

    def display_files(self, folder_path):
        import os
        # Xóa nội dung cũ của QListWidget
        self.file_list.clear()
        # Lấy danh sách các file trong folder đã chọn
        files = os.listdir(folder_path)
        # Hiển thị các file trong QListWidget
        for file in files:
            self.file_list.addItem(file)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    folder_selection = FolderSelection()
    folder_selection.show()
    sys.exit(app.exec_())
