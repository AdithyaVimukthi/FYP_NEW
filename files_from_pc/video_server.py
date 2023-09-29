import socket
import cv2
import pickle
import struct
import imutils


def get_ip_address():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip_address = s.getsockname()[0]
        s.close()
        return ip_address
    except Exception as e:
        return "Error: " + str(e)


def gstreamer_pipeline(
        camera_id,
        capture_width=1920,
        capture_height=1080,
        display_width=640,
        display_height=480,
        framerate=30,
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


class VideoServer():
    def __init__(self, port_num):
        # Socket Create
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host_ip = get_ip_address()
        self.port = port_num
        self.socket_address = (self.host_ip, self.port)
        self.server_socket.bind(self.socket_address)
        self.server_socket.listen(5)
        print("LISTENING AT:", self.socket_address)

    def start_server(self):
        while True:
            client_socket, addr = self.server_socket.accept()
            print('GOT CONNECTION FROM:', addr)
            if client_socket:
                vid = cv2.VideoCapture(gstreamer_pipeline(camera_id=0, flip_method=2),
                                       cv2.CAP_GSTREAMER)  # for raspberry cam
                # vid = cv2.VideoCapture(0)   #for webcam

                while vid.isOpened():
                    img, frame = vid.read()
                    print(frame.shape)
                    frame = imutils.resize(frame, width=320)
                    a = pickle.dumps(frame)
                    message = struct.pack("Q", len(a)) + a
                    client_socket.sendall(message)

                    cv2.imshow('TRANSMITTING VIDEO', frame)

                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        client_socket.close()
                        vid.relase()
                        cv2.destroyAllWindows()


if __name__ == "__main__":
    server = VideoServer(8000)  # Replace with your server IP and port
    server.start_server()
