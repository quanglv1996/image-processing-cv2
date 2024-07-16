import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QFrame, QPushButton, QLabel, QMessageBox, QHBoxLayout, QScrollArea
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSize

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Dynamic QFrame Example")
        self.setGeometry(100, 100, 400, 300)

        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.main_layout.addWidget(self.scroll_area)

        self.scroll_content = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_content)
        self.scroll_area.setWidget(self.scroll_content)

        self.rows = []
        self.insert_buttons = []

        # Add initial row if there are no rows
        if not self.rows:
            self.add_row()

        # Add insert button at the bottom
        self.add_insert_button()

    def add_row(self):
        row_frame = QFrame()
        row_layout = QHBoxLayout()
        row_frame.setLayout(row_layout)

        row_label = QLabel(f"Row {len(self.rows) + 1}")
        row_layout.addWidget(row_label)

        config_button = QPushButton("Config")
        config_button.clicked.connect(lambda _, btn=config_button: self.config_action(btn))
        row_layout.addWidget(config_button)

        delete_button = QPushButton()
        delete_button.setIcon(QIcon('minus.png'))
        delete_button.setIconSize(QSize(16, 16))  # Set the size of the icon
        delete_button.setFixedSize(24, 24)  # Set the size of the button to fit the icon
        delete_button.clicked.connect(lambda _, frame=row_frame: self.delete_row(frame))
        row_layout.addWidget(delete_button)

        insert_button = QPushButton()
        insert_button.setIcon(QIcon('plus.png'))
        insert_button.setIconSize(QSize(16, 16))  # Set the size of the icon
        insert_button.setFixedSize(24, 24)  # Set the size of the button to fit the icon
        insert_button.clicked.connect(lambda _, idx=len(self.rows): self.insert_row(idx))
        row_layout.addWidget(insert_button)
        self.insert_buttons.append(insert_button)

        self.rows.append((row_frame, row_label))
        self.scroll_layout.addWidget(row_frame)

        self.update_row_labels()

    def add_insert_button(self):
        insert_button = QPushButton()
        insert_button.setIcon(QIcon('plus.png'))
        insert_button.setIconSize(QSize(16, 16))  # Set the size of the icon
        insert_button.setFixedSize(24, 24)  # Set the size of the button to fit the icon
        insert_button.clicked.connect(lambda: self.insert_row(len(self.rows)))
        self.scroll_layout.addWidget(insert_button)
        self.insert_buttons.append(insert_button)

    def insert_row(self, index):
        row_frame = QFrame()
        row_layout = QHBoxLayout()
        row_frame.setLayout(row_layout)

        row_label = QLabel(f"Row {len(self.rows) + 1}")
        row_layout.addWidget(row_label)

        config_button = QPushButton("Config")
        config_button.clicked.connect(lambda _, btn=config_button: self.config_action(btn))
        row_layout.addWidget(config_button)

        delete_button = QPushButton()
        delete_button.setIcon(QIcon('minus.png'))
        delete_button.setIconSize(QSize(16, 16))  # Set the size of the icon
        delete_button.setFixedSize(24, 24)  # Set the size of the button to fit the icon
        delete_button.clicked.connect(lambda _, frame=row_frame: self.delete_row(frame))
        row_layout.addWidget(delete_button)

        insert_button = QPushButton()
        insert_button.setIcon(QIcon('plus.png'))
        insert_button.setIconSize(QSize(16, 16))  # Set the size of the icon
        insert_button.setFixedSize(24, 24)  # Set the size of the button to fit the icon
        insert_button.clicked.connect(lambda _, idx=len(self.rows): self.insert_row(idx))
        row_layout.addWidget(insert_button)
        self.insert_buttons.insert(index, insert_button)

        self.rows.insert(index, (row_frame, row_label))
        self.scroll_layout.insertWidget(index, row_frame)

        self.update_row_labels()

    def config_action(self, button):
        reply = QMessageBox.question(self, 'Config Confirmation', 'Do you want to config this row?',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            button.setStyleSheet("background-color: green")

    def delete_row(self, frame):
        for i, (row_frame, row_label) in enumerate(self.rows):
            if row_frame == frame:
                self.rows.pop(i)
                self.insert_buttons.pop(i).deleteLater()  # Remove and delete insert button
                for widget in row_frame.findChildren(QWidget):
                    widget.deleteLater()
                row_frame.deleteLater()
                break

        if len(self.rows) == 0:
            self.add_row()  # Add a new row if all rows are deleted
        else:
            self.update_row_labels()

    def update_row_labels(self):
        for i, (row_frame, row_label) in enumerate(self.rows):
            row_label.setText(f"Row {i + 1}")

app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec_())
