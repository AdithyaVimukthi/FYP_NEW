import cv2
import mediapipe as mp
import math

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()


# Function to calculate distance between two points
def calculate_distance(point1, point2):
    return math.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)


# Webcam setup
cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        continue

    # Convert the frame to RGB for MediaPipe
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Process the frame with MediaPipe Hands
    results = hands.process(frame_rgb)

    if results.multi_hand_landmarks:
        for landmarks in results.multi_hand_landmarks:
            # Get the landmarks for the hand
            landmarks_list = []
            for landmark in landmarks.landmark:
                x, y, _ = frame.shape[1] * landmark.x, frame.shape[0] * landmark.y, landmark.z
                landmarks_list.append((x, y))

            # Calculate the distance between two specific landmarks (e.g., thumb and index finger)
            thumb_tip = landmarks_list[1]
            index_tip = landmarks_list[17]
            distance = calculate_distance(thumb_tip, index_tip)

            # Display the distance on the frame
            cv2.putText(frame, f"Distance: {round(distance)} pixels", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0),
                        2)

            # Draw the landmarks on the frame
            for landmark in landmarks_list:
                cv2.circle(frame, (int(landmark[0]), int(landmark[1])), 5, (0, 0, 255), -1)

    # Display the frame
    cv2.imshow("Hand Distance Estimation", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and close OpenCV windows
cap.release()
cv2.destroyAllWindows()
