import cv2
from Cam_v2 import Video
from sending_data_cal import Data_process

if __name__ == '__main__':
    video = Video()
    data_process = Data_process()
    while True:
        data = video.video_analyzer()
        if len(data[1]) == 1:
            cv2.imshow('Video view', data[0])
        else:
            landmark_data = data[1]
            frame_size_data = data[2]
            processed_data = data_process.Proces(landmark_data, frame_size_data)
            message = processed_data[0]
            print(message)
            res_img = video.draw_result(processed_data[1])
            cv2.imshow('Video view', res_img)

            if cv2.waitKey(5) & 0xFF == ord('q'):
                break