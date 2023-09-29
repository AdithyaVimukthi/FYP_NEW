from Server_gui import ServerMonitorApp
from PyQt5.QtWidgets import *
import sys


if __name__ == "__main__":
    app = QApplication(sys.argv)
    server_monitor = ServerMonitorApp()
    server_monitor.show()
    sys.exit(app.exec_())
