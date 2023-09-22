import numpy as np
import cv2

print(cv2.__version__)

def gstreamer_pipeline(
        camera_id,
        capture_width=1280,
        capture_height=720,
        display_width=640,
        display_height=480,
        framerate=120,
        flip_method=0,
    ):
    return (
            "nvarguscamerasrc sensor-id=%d ! "
            "video/x-raw(memory:NVMM), "
            "width=(int)%d, height=(int)%d, "
            "format=(string)NV12, framerate=(fraction)%d/1 ! "
            "nvvidconv flip-method=%d ! "
            "video/x-raw, width=(int)%d, height=(int)%d, format=(string)BGRx ! "
            "videoconvert ! "
            "video/x-raw, format=(string)BGR ! appsink max-buffers=1 drop=True"
            % (
                    camera_id,
                    capture_width,
                    capture_height,
                    framerate,
                    flip_method,
                    display_width,
                    display_height,
            )
    )

class get_video():
	def __init__(self):
		self.cap = cv2.VideoCapture(gstreamer_pipeline(camera_id=0, flip_method=2), cv2.CAP_GSTREAMER)


	def video (self):

		while(self.cap.isOpened()):
			
			while True:
				
				ret, img = self.cap.read()
				cv2.imshow('img', img)
				if cv2.waitKey(30) & 0xff == ord('q'):
					break
					
			self.cap.release()
			cv2.destroyAllWindows()
		else:
			print("Alert ! Camera disconnected")


if __name__ == "__main__":
	cam = get_video()
	cam.video()
