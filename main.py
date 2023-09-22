import cv2
from Cam_v2 import Video
from TCP_CLIENT import Client
from sending_data_cal import Data_process

if __name__ == '__main__':
    client = Client("192.168.1.3", 8000)  # Replace with the server's IP and port
    video = Video()
    data_process = Data_process()

    client.connect()

    while True:
        data = video.video_analyzer()
        cv2.imshow('MediaPipe Pose', data[0])

        # print(data)

        if len(data) == 1:
            pass
        else:
            landmark_data = data[1]     
            sending_data = data_process.Proces(landmark_data)

            message = str(sending_data)

            client.send_message(message)

            if cv2.waitKey(5) & 0xFF == ord('q'):
                message = "quit"
                cv2.destroyAllWindows()

            if message.lower() == "quit":
                client.disconnect()
                break




