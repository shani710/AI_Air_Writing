import cv2
import os
import numpy as np
from src.hand_tracker import HandTracker
from src.gesture_recognizer import GestureRecognizer
from src.canvas import VirtualCanvas
from config.settings import *

class DataCollector:
    def __init__(self):
        self.hand_tracker = HandTracker()
        self.gesture_recognizer = GestureRecognizer()
        self.canvas = VirtualCanvas()
        self.current_letter = None
        self.sample_count = 0
        
    def collect_data(self, letter, num_samples=100):
        """Collect data for a specific letter"""
        self.current_letter = letter
        self.sample_count = 0
        
        # Create directory for the letter
        save_dir = os.path.join(DATA_COLLECTION_DIR, letter)
        os.makedirs(save_dir, exist_ok=True)
        
        cap = cv2.VideoCapture(CAMERA_INDEX)
        
        print(f"Collecting data for letter '{letter}'")
        print(f"Pinch your fingers to write, open palm or make fist to stop")
        print(f"Press 'c' to clear canvas, 's' to save, 'q' to quit")
        
        while self.sample_count < num_samples:
            ret, frame = cap.read()
            if not ret:
                break
            
            frame = cv2.flip(frame, 1)
            frame = cv2.resize(frame, (CAMERA_WIDTH, CAMERA_HEIGHT))
            
            # Process hand tracking
            results = self.hand_tracker.process_frame(frame)
            
            if results.multi_hand_landmarks:
                hand_landmarks = results.multi_hand_landmarks[0]
                
                # Get fingertip positions
                index_tip = self.hand_tracker.get_fingertip_position(
                    hand_landmarks, self.hand_tracker.INDEX_TIP, frame.shape
                )
                thumb_tip = self.hand_tracker.get_fingertip_position(
                    hand_landmarks, self.hand_tracker.THUMB_TIP, frame.shape
                )
                fingertips = self.hand_tracker.get_all_fingertips(hand_landmarks, frame.shape)
                
                # Update gesture state
                gesture_state = self.gesture_recognizer.update_gesture_state(
                    index_tip, thumb_tip, fingertips
                )
                
                if gesture_state == "WRITING":
                    self.canvas.draw_point(index_tip)
                elif gesture_state == "STOP_WRITING":
                    self.canvas.end_stroke()
                    self.canvas.clear_canvas()
                    self.sample_count += 1
                    print(f"Collected {self.sample_count}/{num_samples} samples for '{letter}'")
                
                # Draw hand landmarks
                self.hand_tracker.draw_landmarks(frame, hand_landmarks)
                cv2.circle(frame, index_tip, 10, (0, 255, 0), -1)
            
            # Overlay canvas on frame
            frame = self.canvas.overlay_on_frame(frame, 0.3)
            
            # Display information
            cv2.putText(frame, f"Letter: {letter}", (10, 30), FONT, FONT_SCALE, FONT_COLOR, FONT_THICKNESS)
            cv2.putText(frame, f"Samples: {self.sample_count}/{num_samples}", (10, 60), FONT, FONT_SCALE, FONT_COLOR, FONT_THICKNESS)
            cv2.putText(frame, "Writing: " + ("YES" if self.gesture_recognizer.is_writing else "NO"), 
                       (10, 90), FONT, FONT_SCALE, FONT_COLOR, FONT_THICKNESS)
            
            cv2.imshow(WINDOW_NAME, frame)
            
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break
            elif key == ord('c'):
                self.canvas.clear_canvas()
            elif key == ord('s') and self.canvas.trajectory:
                # Manual save
                img = self.canvas.get_trajectory_image()
                save_path = os.path.join(save_dir, f"{letter}_{self.sample_count}.png")
                cv2.imwrite(save_path, img)
                self.sample_count += 1
                self.canvas.clear_canvas()
                print(f"Manually saved sample {self.sample_count}")
        
        cap.release()
        cv2.destroyAllWindows()
        self.hand_tracker.release()
        print(f"Data collection for '{letter}' complete!")