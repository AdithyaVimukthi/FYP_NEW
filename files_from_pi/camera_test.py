from picamera2 import Picamera2, Preview
from time import sleep
import cv2

cam = Picamera2()
cam.preview_configuration.main.size=(1640, 1232)
cam.preview_configuration.main.format="RGB888"
cam.preview_configuration.align()
cam.configure("preview")
cam.start()
while True:
    frame=cam.capture_array()
    frame = cv2.resize(frame, (615,462),interpolation=cv2.INTER_LINEAR)
    cv2.imshow("PICAM",frame)
    if cv2.waitKey(1)==ord("q"):
        break
cv2.destroyAllWindows()










# cam.start_preview(Preview.QTGL)
# preview_config = cam.create_preview_configuration()
# cam.configure(preview_config)

# cam.start()
# sleep(10)