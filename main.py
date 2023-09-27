import cv2
from Cam_v2 import Video
from TCP_CLIENT import Client
from sending_data_cal import Data_process

if __name__ == '__main__':
    client = Client("192.168.1.4", 8000)  # Replace with the server's IP and port
    video = Video()
    data_process = Data_process()

    client.connect()

    while True:
        data = video.video_analyzer()

        if len(data) == 1:
            pass
        else:
            landmark_data = data[1]
            frame_size_data = data[2]
            processed_data = data_process.Proces(landmark_data, frame_size_data)

            res_img = video.draw_result(processed_data[1])
            cv2.imshow('MediaPipe Pose', res_img)

            # message = str(sending_data)
            message = processed_data[0]

            client.send_message(message)

            if cv2.waitKey(5) & 0xFF == ord('q'):
                message = "quit"
                cv2.destroyAllWindows()

            if message.lower() == "quit":
                client.disconnect()
                break




