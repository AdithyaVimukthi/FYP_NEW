import sys
import socket
import threading
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from servo import servo_controller
from camera import camera
from server_sep import Server
from cus_threading import ThreadWithReturnValue

class ServerMonitorApp(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.servo = servo_controller()
        self.cam = camera()

        self.clients_label = None
        self.save_list = None
        self.server_thread = None
        self.received_messages_list = None
        self.clear_list = None
        self.start_button = None
        self.client_listbox = None
        self.ClientCount = 0

        self.client_messages = []
        self.server_running = False

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

        ip_address = "get_ip_address()"
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
        self.timer.start(10)  # Update every 10 milliseconds

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
        frame = self.cam.capture()
        
        # Convert the frame to a QImage
        height, width, channel = frame.shape
        bytes_per_line = 3 * width
        q_img = QImage(frame.data, width, height, bytes_per_line, QImage.Format_RGB888)

        # Display the webcam feed in the QLabel
        self.cam_label.setPixmap(QPixmap.fromImage(q_img))
    
    def start_server(self):
        self.server = Server()
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
