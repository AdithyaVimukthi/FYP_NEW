import cv2
import mediapipe as mp
import numpy as np

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_pose = mp.solutions.pose

# For webcam input:
cap = cv2.VideoCapture(0)
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
frame_size = (width, height)


def calculate_dis(a, b):
    a = np.array(a)  # First point
    b = np.array(b)  # second point

    sqrs = (a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2
    dist = np.sqrt(sqrs)

    return dist


# pose = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)
with mp_pose.Pose(
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5) as pose:
    while cap.isOpened():
        success, image = cap.read()

        fps = int(cap.get(cv2.CAP_PROP_FPS))
        print(f'FPS = {fps}')
        print(f'frame_size = {frame_size}')

        if not success:
            print("Ignoring empty camera frame.")
            # If loading a video, use 'break' instead of 'continue'.
            continue

        # To improve performance, optionally mark the image as not writeable to
        # pass by reference.
        image.flags.writeable = False
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = pose.process(image)

        # Draw the pose annotation on the image.
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        # mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
        #                           landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style())

        landmark_c = results.pose_landmarks.landmark
        Wrist = [round(landmark_c[mp_pose.PoseLandmark.RIGHT_WRIST.value].x * width),
                 round(landmark_c[mp_pose.PoseLandmark.RIGHT_WRIST.value].y * height)]
        Shoulder_R = [round(landmark_c[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x * width),
                      round(landmark_c[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y * height)]
        elbow = [round(landmark_c[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x * width),
                 round(landmark_c[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y * height)]
        Shoulder_L = [round(landmark_c[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x * width),
                      round(landmark_c[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y * height)]

        R_x = Shoulder_R[0] - Wrist[0]
        R_y = Shoulder_R[1] - Wrist[1]
        print(f"X and Y Coordinates relative to shoulder point = {R_x, R_y}")

        # print(f'Wrist {Wrist}')
        # print(f'Shoulder {Shoulder}')
        # print(f'Elbow {elbow}')
        dist = round(calculate_dis(Shoulder_L, Shoulder_R))
        print(f"Distance = {dist}")
        # image2 = cv2.circle(image, Shoulder, radius=5, color=(0, 0, 255), thickness=-1)
        # image2 = cv2.circle(image2, Wrist, radius=5, color=(0, 0, 255), thickness=-1)

        # Draw the arrowed line passing the arguments
        image2 = cv2.arrowedLine(image, (Shoulder_R[0] + 80, Shoulder_R[1]), (Shoulder_R[0] - 150, Shoulder_R[1]),
                                 (255, 255, 255), 2, 5, 0, 0.1)
        image2 = cv2.arrowedLine(image2, (Shoulder_R[0], Shoulder_R[1] + 80), (Shoulder_R[0], Shoulder_R[1] - 150),
                                 (255, 255, 255), 2, 5, 0, 0.1)

        # Draw a diagonal green line with thickness of 9 px
        image2 = cv2.line(image2, Shoulder_R, Wrist, (0, 255, 0), 2)
        image2 = cv2.putText(image2, f'({R_x},{R_y})',
                             (Wrist[0] + 20, Wrist[1] + 20), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 0), 2, cv2.LINE_AA)
        # Flip the image horizontally for a selfie-view display.
        cv2.imshow('MediaPipe Pose', image2)
        if cv2.waitKey(5) & 0xFF == ord('q'):
            break
cap.release()
