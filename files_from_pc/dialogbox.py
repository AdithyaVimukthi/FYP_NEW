from PyQt5.QtWidgets import *

class LoginDialog(QDialog):
    def __init__(self, parent=None):
        # app = QApplication([])
        super(LoginDialog, self).__init__(parent)

        self.setWindowTitle("Login")

        self.server_ip_label = QLabel("Server IP:")
        self.server_ip = QLineEdit(self)
        self.server_port_label = QLabel("Server Port:")
        self.server_port = QLineEdit(self)

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
