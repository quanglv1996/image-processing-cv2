import sys
import cv2
import numpy as np
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout
from PyQt5.QtGui import QPixmap, QImage, QPainter, QPen
from PyQt5.QtCore import Qt, QPoint

class CameraApp(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setWindowTitle('Camera App')
        
        self.label = QLabel(self)
        self.label.setFixedSize(640, 480)
        
        self.connect_btn = QPushButton('Connect', self)
        self.connect_btn.clicked.connect(self.connect_camera)
        
        self.apply_btn = QPushButton('Apply', self)
        self.apply_btn.clicked.connect(self.apply)

        self.circle_center = QPoint(320, 240)
        self.circle_radius = 20
        self.dragging = False

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.connect_btn)
        layout.addWidget(self.apply_btn)

        self.setLayout(layout)
        self.cap = None

    def connect_camera(self):
        self.cap = cv2.VideoCapture(0)
        self.timer_id = self.startTimer(30)

    def timerEvent(self, event):
        ret, frame = self.cap.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, ch = frame.shape
            bytes_per_line = ch * w
            q_img = QImage(frame.data, w, h, bytes_per_line, QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(q_img)

            painter = QPainter(pixmap)
            pen = QPen(Qt.red)
            painter.setPen(pen)
            painter.drawEllipse(self.circle_center, self.circle_radius, self.circle_radius)
            
            # Draw crosshair
            painter.drawLine(self.circle_center.x() - self.circle_radius, self.circle_center.y(), 
                             self.circle_center.x() + self.circle_radius, self.circle_center.y())
            painter.drawLine(self.circle_center.x(), self.circle_center.y() - self.circle_radius, 
                             self.circle_center.x(), self.circle_center.y() + self.circle_radius)
            painter.end()

            self.label.setPixmap(pixmap)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            distance = (event.pos() - self.circle_center).manhattanLength()
            if distance <= self.circle_radius:
                self.dragging = True

    def mouseMoveEvent(self, event):
        if self.dragging:
            new_x = event.pos().x()
            new_y = event.pos().y()
            # Ensure the circle center stays within the image boundaries
            new_x = max(0, min(new_x, self.label.width()))
            new_y = max(0, min(new_y, self.label.height()))
            self.circle_center = QPoint(new_x, new_y)
            self.update()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragging = False

    def apply(self):
        print(f"Circle Center: ({self.circle_center.x()}, {self.circle_center.y()})")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = CameraApp()
    ex.show()
    sys.exit(app.exec_())
