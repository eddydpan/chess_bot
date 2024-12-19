import mediapipe as mp
import cv2

# Initialize Mediapipe Hand module
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False,
                       max_num_hands=1,
                       min_detection_confidence=0.5,
                       min_tracking_confidence=0.5)
mp_drawing = mp.solutions.drawing_utils

def interpret_gesture(landmarks):
    """
    Interpret Basic Gestures (Thumbs Up, Thumbs Down, Fist)

    ::landmarks:: detected hand points
    """
    # Convert normalized landmarks to a more usable form
    points = [(landmark.x, landmark.y, landmark.z) for landmark in landmarks.landmark]

    # # Example 1: "Thumbs Up"
    # if points[mp_hands.HandLandmark.THUMB_TIP][1] < points[mp_hands.HandLandmark.THUMB_IP][1] < points[mp_hands.HandLandmark.THUMB_MCP][1]:
    #     if points[mp_hands.HandLandmark.INDEX_FINGER_MCP][1] < points[mp_hands.HandLandmark.INDEX_FINGER_PIP][1]:
    #         return "Thumbs Up"

    # # Example 2: "Fist" (All fingers folded)
    # if all(points[i][1] > points[i + 1][1] for i in [mp_hands.HandLandmark.INDEX_FINGER_MCP, 
    #                                                 mp_hands.HandLandmark.MIDDLE_FINGER_MCP,
    #                                                 mp_hands.HandLandmark.RING_FINGER_MCP,
    #                                                 mp_hands.HandLandmark.PINKY_MCP]):
    #     return "Fist"
    
    # # Example 3: "Thumbs Down"
    # if points[mp_hands.HandLandmark.THUMB_TIP][1] > points[mp_hands.HandLandmark.THUMB_IP][1] > points[mp_hands.HandLandmark.THUMB_MCP][1]:
    #     if points[mp_hands.HandLandmark.INDEX_FINGER_MCP][1] < points[mp_hands.HandLandmark.INDEX_FINGER_PIP][1]:
    #         return "Thumbs Down"

    if points[mp_hands.HandLandmark.WRIST][1] > points[mp_hands.HandLandmark.THUMB_CMC][1]:
            return "Shake"

    # If no gesture recognized
    return None

def run_gesture_recognition():
    """Open Camera and Identify Handmarks"""
    cap = cv2.VideoCapture(0)  # Open webcam

    if not cap.isOpened():
        print("Error: Could not open webcam.")
        return

    while cap.isOpened():
        success, frame = cap.read()
        if not success:
            print("Ignoring empty camera frame.")
            break

        # Flip and process the frame
        frame = cv2.flip(frame, 1)  # Flip camera for intuitive view
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Convert to RGB
        results = hands.process(rgb_frame)

        # Process and draw hand landmarks
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                gesture = interpret_gesture(hand_landmarks)
                
                # Display the gesture on the frame
                if gesture:
                    cv2.putText(frame, f"Gesture: {gesture}", (10, 50), 
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)

        # Display the frame with landmarks and gesture text
        cv2.imshow("Hand Gesture Recognition", frame)

        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the webcam and close windows
    cap.release()
    cv2.destroyAllWindows()

# Run the gesture recognition
run_gesture_recognition()
