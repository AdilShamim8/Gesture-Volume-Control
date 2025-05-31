import cv2
import mediapipe as mp
import math
import numpy as np
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

# solution APIs
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

# Volume Control Library Usage 
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
volRange = volume.GetVolumeRange()
minVol, maxVol, volBar, volPer = volRange[0], volRange[1], 400, 0

# Webcam Setup
wCam, hCam = 640, 480
cam = cv2.VideoCapture(0)
cam.set(3, wCam)
cam.set(4, hCam)

# UI Constants
BAR_WIDTH = 40
BAR_HEIGHT = 300
BAR_X = 50
BAR_Y = 100
BAR_COLOR = (0, 255, 0)  # Green
BAR_BG_COLOR = (50, 50, 50)  # Dark gray
TEXT_COLOR = (255, 255, 255)  # White
HAND_COLOR = (0, 255, 255)  # Yellow
LINE_COLOR = (0, 255, 0)  # Green
LINE_COLOR_CLOSE = (0, 0, 255)  # Red
OVERLAY_COLOR = (0, 0, 0)  # Black
OVERLAY_ALPHA = 0.3  # Overlay transparency

def draw_rounded_rect(img, x, y, w, h, color, radius=20):
    """Draw a rounded rectangle"""
    # Draw main rectangle
    cv2.rectangle(img, (x + radius, y), (x + w - radius, y + h), color, -1)
    cv2.rectangle(img, (x, y + radius), (x + w, y + h - radius), color, -1)
    
    # Draw circles for corners
    cv2.circle(img, (x + radius, y + radius), radius, color, -1)
    cv2.circle(img, (x + w - radius, y + radius), radius, color, -1)
    cv2.circle(img, (x + radius, y + h - radius), radius, color, -1)
    cv2.circle(img, (x + w - radius, y + h - radius), radius, color, -1)

def create_gradient_bar(img, x, y, w, h, start_color, end_color):
    """Create a gradient background for the volume bar"""
    for i in range(h):
        alpha = i / h
        color = tuple(int(start_color[j] * (1 - alpha) + end_color[j] * alpha) for j in range(3))
        cv2.line(img, (x, y + i), (x + w, y + i), color, 1)

# Mediapipe Hand Landmark Model
with mp_hands.Hands(
    model_complexity=0,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as hands:

    while cam.isOpened():
        success, image = cam.read()
        if not success:
            continue

        # Create a copy of the image for drawing
        display_image = image.copy()
        
        # Add semi-transparent overlay
        overlay = display_image.copy()
        cv2.rectangle(overlay, (0, 0), (wCam, hCam), OVERLAY_COLOR, -1)
        cv2.addWeighted(overlay, OVERLAY_ALPHA, display_image, 1 - OVERLAY_ALPHA, 0, display_image)

        # Process hand landmarks
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = hands.process(image_rgb)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(
                    display_image,
                    hand_landmarks,
                    mp_hands.HAND_CONNECTIONS,
                    mp_drawing_styles.get_default_hand_landmarks_style(),
                    mp_drawing_styles.get_default_hand_connections_style()
                )

        # Process hand landmarks for volume control
        lmList = []
        if results.multi_hand_landmarks:
            myHand = results.multi_hand_landmarks[0]
            for id, lm in enumerate(myHand.landmark):
                h, w, c = image.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                lmList.append([id, cx, cy])

        # Volume control logic
        if len(lmList) != 0:
            x1, y1 = lmList[4][1], lmList[4][2]
            x2, y2 = lmList[8][1], lmList[8][2]

            # Draw hand tracking elements with glow effect
            for radius in range(15, 0, -3):
                alpha = radius / 15
                color = tuple(int(HAND_COLOR[i] * alpha) for i in range(3))
                cv2.circle(display_image, (x1, y1), radius, color, -1)
                cv2.circle(display_image, (x2, y2), radius, color, -1)
            
            length = math.hypot(x2-x1, y2-y1)
            line_color = LINE_COLOR_CLOSE if length < 50 else LINE_COLOR
            
            # Draw line with gradient
            for i in range(3):
                cv2.line(display_image, (x1, y1), (x2, y2), line_color, 3-i)

            # Volume calculations
            vol = np.interp(length, [50, 220], [minVol, maxVol])
            volume.SetMasterVolumeLevel(vol, None)
            volBar = np.interp(length, [50, 220], [BAR_HEIGHT, 0])
            volPer = np.interp(length, [50, 220], [0, 100])

            # Create gradient background for volume bar
            create_gradient_bar(display_image, 
                              BAR_X, 
                              BAR_Y, 
                              BAR_WIDTH, 
                              BAR_HEIGHT, 
                              (30, 30, 30), 
                              (50, 50, 50))

            # Draw volume level with rounded corners
            draw_rounded_rect(display_image,
                            BAR_X,
                            int(BAR_Y + volBar),
                            BAR_WIDTH,
                            int(BAR_HEIGHT - volBar),
                            BAR_COLOR)

            # Add volume percentage text with background
            text = f'{int(volPer)}%'
            text_size = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 1, 2)[0]
            text_x = BAR_X - 10
            text_y = BAR_Y + BAR_HEIGHT + 40
            
            # Draw text background
            cv2.rectangle(display_image,
                         (text_x - 5, text_y - text_size[1] - 5),
                         (text_x + text_size[0] + 5, text_y + 5),
                         (0, 0, 0),
                         -1)
            
            # Draw text
            cv2.putText(display_image,
                       text,
                       (text_x, text_y),
                       cv2.FONT_HERSHEY_SIMPLEX,
                       1,
                       TEXT_COLOR,
                       2)

        # Add instructions with background
        instructions = [
            ("Pinch fingers to control volume", (10, 30)),
            ("Press 'q' to quit", (wCam - 150, 30))
        ]
        
        for text, pos in instructions:
            text_size = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 0.7, 2)[0]
            cv2.rectangle(display_image,
                         (pos[0] - 5, pos[1] - text_size[1] - 5),
                         (pos[0] + text_size[0] + 5, pos[1] + 5),
                         (0, 0, 0),
                         -1)
            cv2.putText(display_image,
                       text,
                       pos,
                       cv2.FONT_HERSHEY_SIMPLEX,
                       0.7,
                       TEXT_COLOR,
                       2)

        cv2.imshow('Gesture Volume Control', display_image)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cam.release()
cv2.destroyAllWindows()
