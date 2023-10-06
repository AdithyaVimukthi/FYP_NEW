from picamera2 import Picamera2, Preview
from time import sleep
import cv2


class camera:
    def __init__(self) :
        self.cam = Picamera2()
        self.cam.preview_configuration.main.size=(1640, 1232)
        self.cam.preview_configuration.main.format="RGB888"
        self.cam.preview_configuration.align()
        self.cam.configure("preview")
        self.cam.start()

    def capture(self):
        frame=self.cam.capture_array()
        frame = cv2.resize(frame, (410,308),interpolation=cv2.INTER_LINEAR)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        # cv2.imshow("PICAM",frame)
        return frame



if __name__ == "__main__":
    cam = camera()
    while True:
        frame=cam.capture()
        cv2.imshow("PICAM",frame)
        if cv2.waitKey(1)==ord("q"):
            break
    cv2.destroyAllWindows()










# cam.start_preview(Preview.QTGL)
# preview_config = cam.create_preview_configuration()
# cam.configure(preview_config)

# cam.start()
# sleep(10)