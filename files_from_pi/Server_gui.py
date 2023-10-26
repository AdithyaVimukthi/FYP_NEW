import sys
import cv2
import socket
import threading
import pickle
import struct
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import random
from servo import servo_controller
from camera import camera


def get_ip_address():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip_address = s.getsockname()[0]
        s.close()
        return ip_address
    except Exception as e:
        return "Error: " + str(e)


class ServerMonitorApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.servo = servo_controller()
        self.cam = camera()

        self.frame = None
        self.clients_label = None
        self.save_list = None
        self.server_thread = None
        self.received_messages_list = None
        self.clear_list = None
        self.start_button = None
        self.client_listbox = None
        self.server_socket = None
        self.ClientCount = 0

        self.server_port_list = []
        for i in range(100):
            self.server_port_list.append(8000+i) 
        self.server_port = random.choice(self.server_port_list)

        self.client_messages = []
        self.server_running = False
        self.disconnect_msg = 'disconnect'

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Robot Controller")
        self.setGeometry(50, 50, 1150, 600)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()

        ipdata_and_cam = QHBoxLayout()
        layout.addLayout(ipdata_and_cam)

        data_main = QVBoxLayout()
        ipdata_and_cam.addLayout(data_main)

        ip_address = get_ip_address()
        ip_label = QLabel(f"Your IP Address:          {ip_address}")
        ip_label.setFont(QFont('Arial', 30))
        data_main.addWidget(ip_label)

        server_port_label = QLabel(f"Server Port:                   {self.server_port}")
        server_port_label.setFont(QFont('Arial', 30))
        data_main.addWidget(server_port_label)

        self.clients_label = QLabel(f"Connected Clients:         {self.ClientCount}")
        self.clients_label.setFont(QFont('Arial', 30))
        data_main.addWidget(self.clients_label)

        self.cam_label = QLabel()
        self.cam_label.setAlignment(Qt.AlignRight)
        ipdata_and_cam.addWidget(self.cam_label)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_webcam_feed)
        self.timer.start(1)  # Update every 10 milliseconds

        list_leable_splitter = QSplitter()
        layout.addWidget(list_leable_splitter)

        self.cd_label = QLabel("Clients details") 
        self.cd_label.setFont(QFont('Arial', 15))
        self.cd_label.setMaximumHeight(20)
        self.cd_label.setMinimumWidth(100)
        self.cd_label.setAlignment(Qt.AlignCenter)
        list_leable_splitter.addWidget(self.cd_label)

        self.res_m_label = QLabel("Resiving massage") 
        self.res_m_label.setFont(QFont('Arial', 15))
        self.res_m_label.setMaximumHeight(20)
        self.res_m_label.setMinimumWidth(50)
        self.res_m_label.setAlignment(Qt.AlignCenter)
        list_leable_splitter.addWidget(self.res_m_label)

        self.R_M_label = QLabel("R_M") 
        self.R_M_label.setFont(QFont('Arial', 15))
        self.res_m_label.setMaximumHeight(20)
        list_leable_splitter.addWidget(self.R_M_label)

        self.L_M_label = QLabel("L_M") 
        self.L_M_label.setFont(QFont('Arial', 15))
        self.L_M_label.setMaximumHeight(20)
        list_leable_splitter.addWidget(self.L_M_label)

        self.Grip_label = QLabel("Grip") 
        self.Grip_label.setFont(QFont('Arial', 15))
        self.Grip_label.setMaximumHeight(20)
        list_leable_splitter.addWidget(self.Grip_label)

        # Create a QSplitter to split the client list
        splitter = QSplitter()
        layout.addWidget(splitter)

        self.client_listbox = QListWidget()
        self.client_listbox.setMinimumWidth(400)
        splitter.addWidget(self.client_listbox)

        # Create a QListWidget for received messages
        self.received_messages_list = QListWidget()
        self.received_messages_list.setMinimumWidth(400)
        splitter.addWidget(self.received_messages_list)

        motor_data_splitter = QSplitter()
        splitter.addWidget(motor_data_splitter)
        
        # Create a QListWidget for display motor angles
        self.mr_angle_list = QListWidget()
        motor_data_splitter.addWidget(self.mr_angle_list)

        self.ml_angle_list = QListWidget()
        motor_data_splitter.addWidget(self.ml_angle_list)

        self.gripper_state_list = QListWidget()
        motor_data_splitter.addWidget(self.gripper_state_list)

        buttons_main = QHBoxLayout()
        layout.addLayout(buttons_main)

        server_action_buttons = QHBoxLayout()
        buttons_main.addLayout(server_action_buttons)

        self.start_button = QPushButton("Start Server")

        self.start_button.clicked.connect(self.start_server)
        server_action_buttons.addWidget(self.start_button)

        self.stop_button = QPushButton("Stop Server")
        self.stop_button.clicked.connect(self.stop_server)
        server_action_buttons.addWidget(self.stop_button)

        list_action_buttons = QHBoxLayout()
        buttons_main.addLayout(list_action_buttons)

        self.clear_list = QPushButton("Clear")
        self.clear_list.clicked.connect(self.ClearList)
        list_action_buttons.addWidget(self.clear_list)

        self.save_list = QPushButton("Save")
        self.save_list.clicked.connect(self.SaveList)
        # self.save_list.setEnabled(False)  # Initially disabled
        list_action_buttons.addWidget(self.save_list)

        central_widget.setLayout(layout)
        # self.showMaximized()
        self.showFullScreen()

    def update_webcam_feed(self):
        self.frame = self.cam.capture()
        self.frame  = cv2.flip(self.frame , 0)
        
        # Convert the frame to a QImage
        height, width, channel = self.frame.shape
        bytes_per_line = 3 * width
        q_img = QImage(self.frame.data, width, height, bytes_per_line, QImage.Format_RGB888)

        # Display the webcam feed in the QLabel
        self.cam_label.setPixmap(QPixmap.fromImage(q_img))
    
    def start_server(self):
        self.server_running = True
        self.server_thread = threading.Thread(target=self.run_server)
        self.server_thread.daemon = True
        self.server_thread.start()

    def show_stop_message_box(self):
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Information)
        msg_box.setWindowTitle("Server Stopped")
        msg_box.setText("Server stopped! Thank You")
        msg_box.exec_()

    def stop_server(self):
        self.show_stop_message_box()
        # time.sleep(2)
        QApplication.quit()

    def ClearList(self):
        self.received_messages_list.clear()
        self.mr_angle_list.clear()
        self.ml_angle_list.clear()
        self.gripper_state_list.clear()

    def SaveList(self):
        # Open a file dialog to choose the save location
        file_dialog = QFileDialog(self)
        file_dialog.setAcceptMode(QFileDialog.AcceptSave)
        file_dialog.setNameFilter("Text files (*.txt)")

        if file_dialog.exec_():
            file_path = file_dialog.selectedFiles()[0]
            try:
                with open(file_path, 'w') as file:
                    # Iterate over the items in the list and write them to the file
                    for index in range(self.received_messages_list.count()):
                        item = self.received_messages_list.item(index)
                        file.write(item.text() + '\n')

                QMessageBox.information(self, "Success", "List data saved successfully!")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"An error occurred while saving: {str(e)}")

    def run_server(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((get_ip_address(), self.server_port))
        self.server_socket.listen(5)
        self.client_listbox.clear()

        self.start_button.setEnabled(False)

        Running_msg = "Server Running ..............~ "
        self.client_listbox.addItem(Running_msg)
        self.client_messages.append(Running_msg)

        while True:
            if self.server_running:
                try:
                    client_socket, client_address = self.server_socket.accept()
                    client_info = f"Client connected: {client_address[0]}:{client_address[1]}"
                    self.ClientCount += 1
                    self.clients_label.setText(f"Connected Clients:         {self.ClientCount}")
                    self.client_listbox.addItem(client_info)
                    self.client_messages.append(client_info)
                    self.servo.to_init_pos()

                    self.clear_list.setEnabled(False)
                    self.save_list.setEnabled(False)

                    # Handle client disconnect
                    client_thread = threading.Thread(target=self.handle_client, args=(client_socket, client_address))
                    client_thread.daemon = True
                    client_thread.start()
                except Exception as e:
                    print("Error accepting client:", str(e))

    def handle_client(self, client_socket, client_address):
        while True:
            try:
                self.video_send(client_socket)
                data = client_socket.recv(1024)
                if not data:
                    break
                data_dec = data.decode('utf-8')
                if data_dec == self.disconnect_msg:
                    break
                
                self.received_messages_list.addItem(f"{data_dec}")
                self.received_messages_list.scrollToBottom()

                mot_ang_msg = self.servo.controll(data_dec)

                self.mr_angle_list.addItem(mot_ang_msg[1])
                self.mr_angle_list.scrollToBottom()
                self.ml_angle_list.addItem(mot_ang_msg[2])
                self.ml_angle_list.scrollToBottom()
                self.gripper_state_list.addItem(mot_ang_msg[0])
                self.gripper_state_list.scrollToBottom()

                # Process received data here if needed
            except Exception as e:
                print("Error receiving data from client:", str(e))
                break

        # Handle client disconnect
        client_socket.close()
        disconnected_msg = f"Client disconnected: {client_address[0]}:{client_address[1]}"
        self.ClientCount -= 1
        self.clients_label.setText(f"Connected Clients:         {self.ClientCount}")
        self.client_listbox.addItem(disconnected_msg)
        self.client_messages.append(disconnected_msg)
        self.servo.to_init_pos()

        self.clear_list.setEnabled(True)
        self.save_list.setEnabled(True)

        list_count = self.received_messages_list.count()
        print(f"list_count = {list_count - 1}")

    def video_send(self, conn):
        data = pickle.dumps(self.frame)
        message_size = struct.pack("Q", len(data))
        conn.sendall(message_size + data)


# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     server_monitor = ServerMonitorApp()
#     server_monitor.show()
#     sys.exit(app.exec_())
