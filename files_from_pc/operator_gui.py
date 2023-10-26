from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import QTimer
import cv2
import sys


class camViewer(QWidget):
    def __init__(self, frame):
        super().__init__()

        # Store the frame.
        self.pix = None
        self.frame = frame

        # Create a timer.
        self.timer = QTimer()
        self.timer.timeout.connect(self.nextFrameSlot)

        # Create a layout.
        layout = QVBoxLayout()

        # Create a label.
        self.label = QLabel()
        layout.addWidget(self.label)

        # Set the layout.
        self.setLayout(layout)

    def nextFrameSlot(self):
        # Convert the image from OpenCV BGR format to PyQt format.
        convertToQtFormat = QImage(self.frame.data, self.frame.shape[1], self.frame.shape[0],
                                   QImage.Format_RGB888).rgbSwapped()

        # Convert QImage to QPixmap and show it on QLabel.
        self.pix = QPixmap.fromImage(convertToQtFormat)
        self.label.setPixmap(self.pix)

    def start(self):
        self.timer.start(1)

    def stop(self):
        self.timer.stop()


if __name__ == "__main__":
    app2 = QApplication(sys.argv)

    # Get a frame.
    frame = cv2.imread("D:/photos/batch trip/DJI_0788.jpg")  # Replace with your frame

    viewer = WebcamViewer(frame)
    viewer.start()
    viewer.show()
    sys.exit(app2.exec_())
