# import cv2
# import mediapipe as mp
# import numpy as np
# from config.settings import *

# class HandTracker:
#     def __init__(self):
#         self.mp_hands = mp.solutions.hands
#         self.hands = self.mp_hands.Hands(
#             static_image_mode=False,
#             max_num_hands=MAX_NUM_HANDS,
#             min_detection_confidence=MIN_DETECTION_CONFIDENCE,
#             min_tracking_confidence=MIN_TRACKING_CONFIDENCE
#         )
#         self.mp_draw = mp.solutions.drawing_utils
        
#         # Landmark indices
#         self.INDEX_TIP = 8
#         self.THUMB_TIP = 4
#         self.MIDDLE_TIP = 12
#         self.RING_TIP = 16
#         self.PINKY_TIP = 20
        
#     def get_fingertip_position(self, hand_landmarks, landmark_id, frame_shape):
#         """Get the pixel coordinates of a specific landmark"""
#         h, w, _ = frame_shape
#         landmark = hand_landmarks.landmark[landmark_id]
#         return int(landmark.x * w), int(landmark.y * h)
    
#     def get_all_fingertips(self, hand_landmarks, frame_shape):
#         """Get positions of all fingertips"""
#         fingertips = {}
#         fingertips['index'] = self.get_fingertip_position(hand_landmarks, self.INDEX_TIP, frame_shape)
#         fingertips['thumb'] = self.get_fingertip_position(hand_landmarks, self.THUMB_TIP, frame_shape)
#         fingertips['middle'] = self.get_fingertip_position(hand_landmarks, self.MIDDLE_TIP, frame_shape)
#         fingertips['ring'] = self.get_fingertip_position(hand_landmarks, self.RING_TIP, frame_shape)
#         fingertips['pinky'] = self.get_fingertip_position(hand_landmarks, self.PINKY_TIP, frame_shape)
#         return fingertips
    
#     def process_frame(self, frame):
#         """Process a frame and return hand landmarks"""
#         rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#         results = self.hands.process(rgb_frame)
#         return results
    
#     def draw_landmarks(self, frame, hand_landmarks):
#         """Draw hand landmarks on the frame"""
#         self.mp_draw.draw_landmarks(frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)
#         return frame
    
#     def release(self):
#         """Release resources"""
#         self.hands.close()

# import cv2
# import mediapipe as mp
# import numpy as np
# from config.settings import *

# class HandTracker:
#     def __init__(self):
#         # MediaPipe 0.10.33 uses the tasks API
#         from mediapipe.tasks import python
#         from mediapipe.tasks.python import vision
        
#         # Download the model file if not exists
#         import urllib.request
#         import os
#         model_path = 'hand_landmarker.task'
#         if not os.path.exists(model_path):
#             print("Downloading hand landmarker model...")
#             urllib.request.urlretrieve(
#                 'https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/1/hand_landmarker.task',
#                 model_path
#             )
#             print("Download complete!")
        
#         # Initialize hand landmarker with correct parameter names
#         base_options = python.BaseOptions(model_asset_path=model_path)
#         options = vision.HandLandmarkerOptions(
#             base_options=base_options,
#             num_hands=MAX_NUM_HANDS,
#             min_hand_detection_confidence=MIN_DETECTION_CONFIDENCE,  # Changed from min_detection_confidence
#             min_hand_presence_confidence=MIN_TRACKING_CONFIDENCE,     # Changed from min_tracking_confidence
#             min_tracking_confidence=MIN_TRACKING_CONFIDENCE
#         )
#         self.detector = vision.HandLandmarker.create_from_options(options)
        
#         # Landmark indices
#         self.INDEX_TIP = 8
#         self.THUMB_TIP = 4
#         self.MIDDLE_TIP = 12
#         self.RING_TIP = 16
#         self.PINKY_TIP = 20
        
#     def get_fingertip_position(self, hand_landmarks, landmark_id, frame_shape):
#         """Get the pixel coordinates of a specific landmark"""
#         h, w, _ = frame_shape
#         landmark = hand_landmarks[landmark_id]
#         return int(landmark.x * w), int(landmark.y * h)
    
#     def get_all_fingertips(self, hand_landmarks, frame_shape):
#         """Get positions of all fingertips"""
#         fingertips = {}
#         fingertips['index'] = self.get_fingertip_position(hand_landmarks, self.INDEX_TIP, frame_shape)
#         fingertips['thumb'] = self.get_fingertip_position(hand_landmarks, self.THUMB_TIP, frame_shape)
#         fingertips['middle'] = self.get_fingertip_position(hand_landmarks, self.MIDDLE_TIP, frame_shape)
#         fingertips['ring'] = self.get_fingertip_position(hand_landmarks, self.RING_TIP, frame_shape)
#         fingertips['pinky'] = self.get_fingertip_position(hand_landmarks, self.PINKY_TIP, frame_shape)
#         return fingertips
    
#     def process_frame(self, frame):
#         """Process a frame and return hand landmarks"""
#         # Convert to RGB
#         rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#         mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)
        
#         # Detect hands
#         detection_result = self.detector.detect(mp_image)
        
#         # Create a mock results object for compatibility
#         class Results:
#             def __init__(self, detection_result):
#                 self.multi_hand_landmarks = []
#                 if detection_result.hand_landmarks:
#                     for hand_landmarks in detection_result.hand_landmarks:
#                         self.multi_hand_landmarks.append(hand_landmarks)
        
#         return Results(detection_result)
    
#     def draw_landmarks(self, frame, hand_landmarks):
#         """Draw hand landmarks on the frame"""
#         h, w, _ = frame.shape
        
#         # Define connections between landmarks
#         connections = [
#             (0,1), (1,2), (2,3), (3,4),  # Thumb
#             (0,5), (5,6), (6,7), (7,8),  # Index finger
#             (0,9), (9,10), (10,11), (11,12),  # Middle finger
#             (0,13), (13,14), (14,15), (15,16),  # Ring finger
#             (0,17), (17,18), (18,19), (19,20),  # Pinky
#             (5,9), (9,13), (13,17)  # Palm connections
#         ]
        
#         # Draw connections
#         for connection in connections:
#             start = hand_landmarks[connection[0]]
#             end = hand_landmarks[connection[1]]
#             start_point = (int(start.x * w), int(start.y * h))
#             end_point = (int(end.x * w), int(end.y * h))
#             cv2.line(frame, start_point, end_point, (0, 255, 0), 2)
        
#         # Draw landmarks
#         for i, landmark in enumerate(hand_landmarks):
#             x = int(landmark.x * w)
#             y = int(landmark.y * h)
#             # Color code different fingertips
#             if i in [4, 8, 12, 16, 20]:  # Fingertips
#                 cv2.circle(frame, (x, y), 6, (0, 0, 255), -1)
#             else:
#                 cv2.circle(frame, (x, y), 3, (0, 255, 0), -1)
        
#         return frame
    
#     def release(self):
#         """Release resources"""
#         self.detector.close()


import cv2
import mediapipe as mp
import numpy as np
import urllib.request
import os
from config.settings import *

class HandTracker:
    def __init__(self):
        # Download model if not exists
        self.model_path = 'hand_landmarker.task'
        self.download_model_if_needed()
        
        # Initialize MediaPipe Hands using Tasks API
        from mediapipe.tasks import python
        from mediapipe.tasks.python import vision
        
        base_options = python.BaseOptions(model_asset_path=self.model_path)
        options = vision.HandLandmarkerOptions(
            base_options=base_options,
            num_hands=MAX_NUM_HANDS,
            min_hand_detection_confidence=MIN_DETECTION_CONFIDENCE,
            min_hand_presence_confidence=MIN_TRACKING_CONFIDENCE,
            min_tracking_confidence=MIN_TRACKING_CONFIDENCE
        )
        self.detector = vision.HandLandmarker.create_from_options(options)
        
        # Landmark indices for fingertips
        self.INDEX_TIP = 8
        self.THUMB_TIP = 4
        self.MIDDLE_TIP = 12
        self.RING_TIP = 16
        self.PINKY_TIP = 20
        
    def download_model_if_needed(self):
        """Download the hand landmarker model if not present"""
        if not os.path.exists(self.model_path):
            print("Downloading hand landmarker model (this may take a moment)...")
            url = "https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/1/hand_landmarker.task"
            try:
                urllib.request.urlretrieve(url, self.model_path)
                print("Model downloaded successfully!")
            except Exception as e:
                print(f"Error downloading model: {e}")
                print("Please download manually from:")
                print(url)
                raise
    
    def get_fingertip_position(self, hand_landmarks, landmark_id, frame_shape):
        """Get pixel coordinates of a specific landmark"""
        h, w, _ = frame_shape
        landmark = hand_landmarks[landmark_id]
        return int(landmark.x * w), int(landmark.y * h)
    
    def get_all_fingertips(self, hand_landmarks, frame_shape):
        """Get positions of all fingertips"""
        fingertips = {}
        fingertips['index'] = self.get_fingertip_position(hand_landmarks, self.INDEX_TIP, frame_shape)
        fingertips['thumb'] = self.get_fingertip_position(hand_landmarks, self.THUMB_TIP, frame_shape)
        fingertips['middle'] = self.get_fingertip_position(hand_landmarks, self.MIDDLE_TIP, frame_shape)
        fingertips['ring'] = self.get_fingertip_position(hand_landmarks, self.RING_TIP, frame_shape)
        fingertips['pinky'] = self.get_fingertip_position(hand_landmarks, self.PINKY_TIP, frame_shape)
        return fingertips
    
    def process_frame(self, frame):
        """Process frame and return hand landmarks"""
        # Convert BGR to RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)
        
        # Detect hands
        detection_result = self.detector.detect(mp_image)
        
        # Create a compatible results object
        class Results:
            def __init__(self, detection_result):
                self.multi_hand_landmarks = []
                if detection_result.hand_landmarks:
                    for hand_landmarks in detection_result.hand_landmarks:
                        self.multi_hand_landmarks.append(hand_landmarks)
        
        return Results(detection_result)
    
    def draw_landmarks(self, frame, hand_landmarks):
        """Draw hand landmarks on frame"""
        h, w, _ = frame.shape
        
        # Hand connections
        connections = [
            (0,1), (1,2), (2,3), (3,4),  # Thumb
            (0,5), (5,6), (6,7), (7,8),  # Index
            (0,9), (9,10), (10,11), (11,12),  # Middle
            (0,13), (13,14), (14,15), (15,16),  # Ring
            (0,17), (17,18), (18,19), (19,20),  # Pinky
            (5,9), (9,13), (13,17)  # Palm
        ]
        
        # Draw connections
        for connection in connections:
            start = hand_landmarks[connection[0]]
            end = hand_landmarks[connection[1]]
            start_point = (int(start.x * w), int(start.y * h))
            end_point = (int(end.x * w), int(end.y * h))
            cv2.line(frame, start_point, end_point, (0, 255, 0), 2)
        
        # Draw landmarks (fingertips in red, others in green)
        for i, landmark in enumerate(hand_landmarks):
            x = int(landmark.x * w)
            y = int(landmark.y * h)
            if i in [4, 8, 12, 16, 20]:  # Fingertips
                cv2.circle(frame, (x, y), 8, (0, 0, 255), -1)
            else:
                cv2.circle(frame, (x, y), 4, (0, 255, 0), -1)
        
        return frame
    
    def release(self):
        """Release resources"""
        self.detector.close()

    def __del__(self):
        """Destructor - cleanup resources"""
        try:
            self.release()
        except:
            pass  # Ignore cleanup errors