import cv2
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys
import socket
import numpy as np

class VideoWindow(QWidget):
    def __init__(self):
        super().__init__()

        # Set up socket connection
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect(("192.168.1.4", 8003))  # replace with your server address and port

        self.timer_camera = QTimer()
        self.timer_camera.timeout.connect(self.show_camera)
        self.timer_camera.start(10)

        self.layout = QVBoxLayout()
        self.label_camera = QLabel()
        self.layout.addWidget(self.label_camera)
        self.setLayout(self.layout)

    def show_camera(self):
        # Receive data from the socket
        data = b''
        while True:
            packet = self.sock.recv(4096)
            if not packet: break
            data += packet

        # Convert the data to an image
        nparr = np.frombuffer(data, np.uint8)
        frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        if frame is not None:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image = QImage(frame.data, frame.shape[1], frame.shape[0], QImage.Format_RGB888)
            self.label_camera.setPixmap(QPixmap.fromImage(image))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = VideoWindow()
    window.show()
    sys.exit(app.exec_())