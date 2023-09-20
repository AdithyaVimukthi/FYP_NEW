import sys
import socket
import threading
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QListWidget, QVBoxLayout, QWidget, QSplitter


class ServerMonitorApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.server_socket = None
        self.server_port = 8080
        self.client_messages = []
        self.server_running = False

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("IP Address and Server Clients")
        self.setGeometry(100, 100, 600, 300)

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

        # Create a QSplitter to split the client list
        splitter = QSplitter()
        layout.addWidget(splitter)

        # Create a QListWidget for client details
        self.client_details_list = QListWidget()
        splitter.addWidget(self.client_details_list)

        # Create a QListWidget for received messages
        self.received_messages_list = QListWidget()
        splitter.addWidget(self.received_messages_list)

        self.start_button = QPushButton("Start Server")
        self.start_button.clicked.connect(self.start_server)
        layout.addWidget(self.start_button)

        self.stop_button = QPushButton("Stop Server")
        self.stop_button.clicked.connect(self.stop_server)
        self.stop_button.setEnabled(False)
        layout.addWidget(self.stop_button)

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

    def stop_server(self):
        if self.server_running:
            self.server_running = False
            self.server_socket.shutdown(self.server_socket.SHUT_RDWR)
            self.server_socket.close()
            print("closed")

            self.start_button.setEnabled(True)
            self.stop_button.setEnabled(False)

    def run_server(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind(('0.0.0.0', self.server_port))
        self.server_socket.listen(5)
        self.client_details_list.clear()
        self.received_messages_list.clear()

        while self.server_running:
            try:
                client_socket, client_address = self.server_socket.accept()
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
                self.received_messages_list.addItem(f"Received from {client_address[0]}:{client_address[1]}: {data.decode('utf-8')}")
            except Exception as e:
                print("Error receiving data from client:", str(e))
                break

        client_socket.close()
        disconnected_msg = f"Client disconnected: {client_address[0]}:{client_address[1]}"
        self.client_details_list.addItem(disconnected_msg)
        self.client_messages.append(disconnected_msg)

def main():
    app = QApplication(sys.argv)
    server_monitor = ServerMonitorApp()
    server_monitor.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
