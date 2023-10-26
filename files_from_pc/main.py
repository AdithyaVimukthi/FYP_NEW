import cv2
from PyQt5.QtWidgets import *

from Cam_v2 import Video
from TCP_CLIENT import Client
from sending_data_cal import Data_process
from dialogbox import LoginDialog
from operator_gui import camViewer

if __name__ == '__main__':
    app = QApplication([])

    login = LoginDialog()
    if login.exec_():
        SERVER_IP, SERVER_PORT = login.getInputs()

        client = Client(SERVER_IP, SERVER_PORT)  # Replace with the server's IP and port
        video = Video()
        data_process = Data_process()

        client.connect()

        while True:
            data = video.video_analyzer()

            if len(data[1]) == 1:
                pass
            else:
                landmark_data = data[1]
                frame_size_data = data[2]
                processed_data = data_process.Proces(landmark_data, frame_size_data)
                message = processed_data[0]

                Receiving_frame = client.video_receive()

                Receiving_frame = cv2.cvtColor(Receiving_frame, cv2.COLOR_RGB2BGR)
                Receiving_frame = cv2.resize(Receiving_frame, (820, 616), interpolation=cv2.INTER_LINEAR)

                res_img = video.draw_result(processed_data[1], Receiving_frame)
                res_img = cv2.resize(res_img, (820, 616), interpolation=cv2.INTER_LINEAR)
                show_frame = cv2.hconcat([Receiving_frame, res_img])
                cv2.imshow('Receiving  Video and operator view', show_frame)

                if cv2.waitKey(5) & 0xFF == ord('q'):
                    message = "quit"
                    cv2.destroyAllWindows()

                if message.lower() == "quit":
                    client.disconnect()
                    break

                client.send_message(message)