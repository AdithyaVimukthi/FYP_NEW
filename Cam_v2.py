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
            return ["None"]
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
                return tuple([shoulder_L, shoulder_R, elbow, wrist, "None", "None"])
                # cv2.imshow('MediaPipe Pose', image)
            else:
                landmark_hand = results.right_hand_landmarks.landmark
                mft = [round(landmark_hand[self.mp_pose.HandLandmark.MIDDLE_FINGER_TIP.value].x * self.width),
                       round(landmark_hand[self.mp_pose.HandLandmark.MIDDLE_FINGER_TIP.value].y * self.height)]

                thumb_cmc = [round(landmark_hand[self.mp_pose.HandLandmark.THUMB_CMC.value].x * self.width),
                            round(landmark_hand[self.mp_pose.HandLandmark.THUMB_CMC.value].y * self.height)]
                pinky_cmc = [round(landmark_hand[self.mp_pose.HandLandmark.PINKY_MCP.value].x * self.width),
                             round(landmark_hand[self.mp_pose.HandLandmark.PINKY_MCP.value].y * self.height)]

                dis_cal_data = [thumb_cmc, pinky_cmc]

                return tuple([shoulder_L, shoulder_R, elbow, wrist, mft, dis_cal_data])

    def video_analyzer(self):

        # while self.cap.isOpened():
        success, image = self.cap.read()
        cpy_org_image = image
        fps = int(self.cap.get(cv2.CAP_PROP_FPS))

        if not success:
            print("Ignoring empty camera frame.")
            # If loading a video, use 'break' instead of 'continue'.
            # continue

        landmark_data = self.landmark_extractor(cpy_org_image)

        if len(landmark_data) == 1 and landmark_data[0] == "None":
            return tuple([image, "None"])
        else:
            shoulder_R = [landmark_data[1][0], landmark_data[1][1]]
            wrist = landmark_data[3]

            R_x = shoulder_R[0] - wrist[0]
            R_y = shoulder_R[1] - wrist[1]

            # Draw the arrowed line passing the arguments
            image2 = cv2.arrowedLine(image, (shoulder_R[0] + 80, shoulder_R[1]),
                                     (shoulder_R[0] - 150, shoulder_R[1]),
                                     (255, 255, 255), 2, 5, 0, 0.1)
            image2 = cv2.arrowedLine(image2, (shoulder_R[0], shoulder_R[1] + 80),
                                     (shoulder_R[0], shoulder_R[1] - 150),
                                     (255, 255, 255), 2, 5, 0, 0.1)

            # Draw a diagonal green line with thickness of 9 px
            image2 = cv2.line(image2, shoulder_R, wrist, (0, 255, 0), 2)
            image2 = cv2.putText(image2, f'({R_x},{R_y})',
                                 (wrist[0] + 20, wrist[1] + 20), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 0), 2,
                                 cv2.LINE_AA)

            return tuple([image2, landmark_data])

# if __name__ == "__main__":
#     video = Video()
#     video.landmarks_finder()
