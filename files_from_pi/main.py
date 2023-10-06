from Server_gui import ServerMonitorApp
from PyQt5.QtWidgets import *
import sys
import os

os.environ.pop("QT_QPA_PLATFORM_PLUGIN_PATH")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    server_monitor = ServerMonitorApp()
    server_monitor.show()
    sys.exit(app.exec_())
