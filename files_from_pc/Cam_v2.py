import cv2
import mediapipe as mp
import numpy as np
from typing import Tuple


def calculate_dis(a, b):
    a = np.array(a)  # First point
    b = np.array(b)  # second point

    sqrs = (a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2
    dist = np.sqrt(sqrs)

    return dist


class Video:
    def __init__(self):
        self.image = None
        self.landmark_data = None
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_drawing_styles = mp.solutions.drawing_styles
        self.mp_pose = mp.solutions.holistic

        # For webcam input:
        self.cap = cv2.VideoCapture(0)
        self.width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.frame_size = (self.width, self.height)

        self.holistic = self.mp_pose.Holistic(
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5)

    def landmark_extractor(self, image_cap):
        image_cap.flags.writeable = False
        image_cap = cv2.cvtColor(image_cap, cv2.COLOR_BGR2RGB)
        results = self.holistic.process(image_cap)

        if results.pose_landmarks is None:
            return [0]
            # cv2.imshow('MediaPipe Pose', image)
        else:
            landmark_pose = results.pose_landmarks.landmark
            shoulder_L = [round(landmark_pose[self.mp_pose.PoseLandmark.LEFT_SHOULDER.value].x * self.width),
                          round(landmark_pose[self.mp_pose.PoseLandmark.LEFT_SHOULDER.value].y * self.height),
                          round(landmark_pose[self.mp_pose.PoseLandmark.LEFT_SHOULDER.value].visibility, 5)]
            shoulder_R = [round(landmark_pose[self.mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x * self.width),
                          round(landmark_pose[self.mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y * self.height),
                          round(landmark_pose[self.mp_pose.PoseLandmark.RIGHT_SHOULDER.value].visibility, 5)]
            elbow = [round(landmark_pose[self.mp_pose.PoseLandmark.RIGHT_ELBOW.value].x * self.width),
                     round(landmark_pose[self.mp_pose.PoseLandmark.RIGHT_ELBOW.value].y * self.height)]
            wrist = [round(landmark_pose[self.mp_pose.PoseLandmark.RIGHT_WRIST.value].x * self.width),
                     round(landmark_pose[self.mp_pose.PoseLandmark.RIGHT_WRIST.value].y * self.height)]

            if results.right_hand_landmarks is None:
                return tuple([shoulder_L, shoulder_R, elbow, wrist, -999, -999])
            else:
                landmark_hand = results.right_hand_landmarks.landmark
                mft = [round(landmark_hand[self.mp_pose.HandLandmark.MIDDLE_FINGER_TIP.value].x * self.width),
                       round(landmark_hand[self.mp_pose.HandLandmark.MIDDLE_FINGER_TIP.value].y * self.height)]

                thumb_tip = [round(landmark_hand[self.mp_pose.HandLandmark.THUMB_TIP.value].x * self.width),
                             round(landmark_hand[self.mp_pose.HandLandmark.THUMB_TIP.value].y * self.height)]
                pinky_tip = [round(landmark_hand[self.mp_pose.HandLandmark.PINKY_TIP.value].x * self.width),
                             round(landmark_hand[self.mp_pose.HandLandmark.PINKY_TIP.value].y * self.height)]

                dis_cal_data = [thumb_tip, pinky_tip]

                return tuple([shoulder_L, shoulder_R, elbow, wrist, mft, dis_cal_data])

    def video_analyzer(self):
        success, self.image = self.cap.read()

        cpy_org_image = self.image
        fps = int(self.cap.get(cv2.CAP_PROP_FPS))

        if not success:
            print("Ignoring empty camera frame.")

        self.landmark_data = self.landmark_extractor(cpy_org_image)

        return tuple([self.image, self.landmark_data, [self.width, self.height]])

    def draw_result(self, drawing_data, receiving_frame=None):
        rec_data = drawing_data[0]
        shoulder_R = drawing_data[1]
        wrist = drawing_data[2]

        x1 = int(rec_data[0])
        y1 = int(rec_data[1])
        x2 = int(rec_data[2])
        y2 = int(rec_data[3])

        start_point = (x1, y1)
        end_point = (x2, y2)
        color = (255, 0, 0)
        thickness = 2

        image2 = cv2.rectangle(self.image, start_point, end_point, color, thickness)

        image2 = cv2.circle(image2, start_point, 5, (0, 0, 255), -1)
        image2 = cv2.circle(image2, end_point, 5, (255, 255, 255), -1)

        image2 = cv2.line(image2, shoulder_R, wrist, (0, 255, 0), 2)

        image2 = cv2.flip(image2, 1)

        return image2


if __name__ == "__main__":
    video = Video()
    while True:
        data = video.video_analyzer()
        cv2.imshow('MediaPipe Pose', data[0])
        if cv2.waitKey(5) & 0xFF == ord('q'):
            break
    cv2.destroyAllWindows()
