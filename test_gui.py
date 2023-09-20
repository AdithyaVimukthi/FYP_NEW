import sys
import socket
import threading
import cv2
import numpy as np
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QListWidget, QVBoxLayout, QHBoxLayout, QWidget, QSplitter
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import Qt, QTimer

class ServerMonitorApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.server_port = 8080
        self.client_messages = []
        self.server_running = False
        self.cap = None
        self.frame = None
        self.image_label = None

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("IP Address and Server Clients")
        self.setGeometry(100, 100, 800, 400)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        layout = QVBoxLayout()

        self.ip_label = QLabel("Your IP Address:")
        layout.addWidget(self.ip_label)

        self.ip_address = self.get_ip_address()
        self.ip_display = QLabel(self.ip_address)
        layout.addWidget(self.ip_display)

        self.server_port_label = QLabel(f"Server Port: {self.server_port}")
        layout.addWidget(self.server_port_label)

        # Create a QSplitter to split the client list and video feed
        splitter = QSplitter()
        layout.addWidget(splitter)

        # Create a QListWidget for client details
        self.client_details_list = QListWidget()
        splitter.addWidget(self.client_details_list)

        # Create a widget to display video feed
        video_widget = QWidget()
        video_layout = QVBoxLayout()
        self.image_label = QLabel()
        video_layout.addWidget(self.image_label)
        video_widget.setLayout(video_layout)
        splitter.addWidget(video_widget)

        # Create a QHBoxLayout for buttons
        button_layout = QHBoxLayout()

        self.start_button = QPushButton("Start Server")
        self.start_button.clicked.connect(self.start_server)
        button_layout.addWidget(self.start_button)

        self.stop_button = QPushButton("Stop Server")
        self.stop_button.clicked.connect(self.stop_server)
        self.stop_button.setEnabled(False)
        button_layout.addWidget(self.stop_button)

        layout.addLayout(button_layout)

        self.central_widget.setLayout(layout)

    def get_ip_address(self):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip_address = s.getsockname()[0]
            s.close()
            return ip_address
        except Exception as e:
            return "Error: " + str(e)

    def start_server(self):
        if not self.server_running:
            self.server_running = True
            self.server_thread = threading.Thread(target=self.run_server)
            self.server_thread.daemon = True
            self.server_thread.start()

            self.start_button.setEnabled(False)
            self.stop_button.setEnabled(True)

            # Start capturing webcam feed
            self.start_video_stream()

    def stop_server(self):
        if self.server_running:
            self.server_running = False
            self.start_button.setEnabled(True)
            self.stop_button.setEnabled(False)

            # Stop capturing webcam feed
            self.stop_video_stream()

            # Close the program
            QApplication.quit()

    def run_server(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind(('0.0.0.0', self.server_port))
        server_socket.listen(5)
        self.client_details_list.clear()

        while self.server_running:
            try:
                client_socket, client_address = server_socket.accept()
                client_info = f"Client connected: {client_address[0]}:{client_address[1]}"
                self.client_details_list.addItem(client_info)
                self.client_messages.append(client_info)

                client_thread = threading.Thread(target=self.handle_client, args=(client_socket, client_address))
                client_thread.daemon = True
                client_thread.start()
            except Exception as e:
                print("Error accepting client:", str(e))

    def handle_client(self, client_socket, client_address):
        while self.server_running:
            try:
                data = client_socket.recv(1024)
                if not data:
                    break
                # Process received data here if needed
            except Exception as e:
                print("Error receiving data from client:", str(e))
                break

        client_socket.close()
        disconnected_msg = f"Client disconnected: {client_address[0]}:{client_address[1]}"
        self.client_details_list.addItem(disconnected_msg)
        self.client_messages.append(disconnected_msg)

    def start_video_stream(self):
        self.cap = cv2.VideoCapture(0)  # Use the default camera (usually the built-in webcam)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(1000 / 30)  # 30 frames per second

    def stop_video_stream(self):
        if self.cap:
            self.cap.release()
            self.timer.stop()
            self.image_label.clear()

    def update_frame(self):
        ret, frame = self.cap.read()
        if ret:
            self.frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            self.display_frame()

    def display_frame(self):
        if self.frame is not None:
            height, width, channel = self.frame.shape
            bytes_per_line = 3 * width
            q_img = QImage(self.frame.data, width, height, bytes_per_line, QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(q_img)
            self.image_label.setPixmap(pixmap)
            self.image_label.setAlignment(Qt.AlignCenter)

def main():
    app = QApplication(sys.argv)
    server_monitor = ServerMonitorApp()
    server_monitor.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
