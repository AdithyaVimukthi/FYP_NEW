from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


class LoginDialog(QDialog):
    def __init__(self, parent=None):

        super(LoginDialog, self).__init__(parent)

        self.setWindowTitle("Login to Robot Arm")
        self.setGeometry(50, 50, 250, 150)

        self.server_ip_label = QLabel("Server IP:")
        self.server_ip_label.setFont(QFont('Arial', 15))

        self.server_ip = QLineEdit(self)
        self.server_ip.setFont(QFont('Arial', 15))

        self.server_port_label = QLabel("Server Port:")
        self.server_port_label.setFont(QFont('Arial', 15))

        self.server_port = QLineEdit(self)
        self.server_port.setFont(QFont('Arial', 15))

        self.button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)

        layout = QVBoxLayout()
        layout.addWidget(self.server_ip_label)
        layout.addWidget(self.server_ip)
        layout.addWidget(self.server_port_label)
        layout.addWidget(self.server_port)
        layout.addWidget(self.button_box)
        self.setLayout(layout)

    def getInputs(self):
        return self.server_ip.text(), int(self.server_port.text())


if __name__ == "__main__":
    app = QApplication([])

    login = LoginDialog()
    if login.exec_():
        SERVER_IP, SERVER_PORT = login.getInputs()

        print(f"IP --> {SERVER_IP} && PORT --> {SERVER_PORT}")
