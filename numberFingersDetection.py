import cv2
import mediapipe as mp
from utils import calculateAngle

def detectFingers(lmrks, angle_threshold=150):
    number_of_fingers = 0

    # Check if the tip is below the next landmark (it means the finger is closed)
    four_fingers = [8,12,16,20]
    for id in four_fingers:
        if (lmrks[id][2]<=lmrks[id-1][2]):
            number_of_fingers+=1

    # Check if the Thumb is straight (angle between landmarks 2,3,4)
    angle = calculateAngle(lmrks[2], lmrks[3], lmrks[4])
    if (angle >= angle_threshold):
        number_of_fingers+=1
    
    return number_of_fingers

# Capture the webcam video
cap = cv2.VideoCapture(0)

# Initilise Mediapipe Hands Module for landmarks
mp_hands= mp.solutions.hands # Initialise mp hands solutions
hand_detector = mp_hands.Hands() # Only uses RGB
mp_draw = mp.solutions.drawing_utils # Draws the lines between the landmarks

while True:
    suc, img = cap.read()

    # Convert color for Hands (only RGB)
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) # BGR -> RGB
    results = hand_detector.process(imgRGB)

    number_of_fingers = 0

    TEXT_POSITION = (10, 50)
    TEXT_COLOR = (0,0,225)

    if results.multi_hand_landmarks:
        for handLM in results.multi_hand_landmarks:
            lmrks = [] # Landmarks for each id
            for id, lm in enumerate(handLM.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                lmrks.append([id, cx, cy]) # Add landmarks
            
            number_of_fingers+=detectFingers(lmrks) # Detect for a single hand (2 times - for both)
            mp_draw.draw_landmarks(img, handLM, mp_hands.HAND_CONNECTIONS)
    
        cv2.putText(img, str(number_of_fingers), TEXT_POSITION, cv2.FONT_HERSHEY_PLAIN, 3, TEXT_COLOR, thickness=3)
        
    else:
        cv2.putText(img, "No hand detected", TEXT_POSITION, cv2.FONT_HERSHEY_PLAIN, 3, TEXT_COLOR, thickness=3)

    cv2.imshow("Image", img)

    # Break the loop when 'Q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera and close the window
cap.release()
cv2.destroyAllWindows()