

# import cv2
# import numpy as np
# import os
# import sys
# from .hand_tracker import HandTracker
# from .gesture_recognizer import GestureRecognizer
# from .canvas import VirtualCanvas
# from .model_trainer import ModelTrainer
# from .data_collector import DataCollector
# from config.settings import *

# class AirWritingSystem:
#     def __init__(self):
#         self.hand_tracker = HandTracker()
#         self.gesture_recognizer = GestureRecognizer()
#         self.canvas = VirtualCanvas()
#         self.model_trainer = ModelTrainer()
#         self.data_collector = DataCollector()
        
#         # Try to load pre-trained model, but don't fail if it doesn't exist
#         try:
#             self.model_loaded = self.model_trainer.load_model()
#         except Exception as e:
#             print(f"Note: {e}")
#             self.model_loaded = False
        
#         # UI state
#         self.mode = "WRITE"  # WRITE, COLLECT, TRAIN
#         self.recognized_text = ""
#         self.current_letter = "A"
    
#     def run(self):
#         """Main application loop"""
#         # Initialize camera with better error handling
#         cap = None
        
#         # Try different camera indices and backends
#         for backend in [cv2.CAP_DSHOW, cv2.CAP_ANY]:
#             for idx in range(3):
#                 try:
#                     test_cap = cv2.VideoCapture(idx, backend)
#                     if test_cap.isOpened():
#                         ret, test_frame = test_cap.read()
#                         if ret and test_frame is not None:
#                             cap = test_cap
#                             print(f"✓ Camera opened: index {idx} with backend {backend}")
#                             break
#                     else:
#                         test_cap.release()
#                 except:
#                     continue
#             if cap is not None:
#                 break
        
#         if cap is None or not cap.isOpened():
#             print("=" * 50)
#             print("ERROR: Could not open any camera!")
#             print("Please check:")
#             print("1. Your webcam is connected")
#             print("2. Camera is not being used by another app")
#             print("3. You have granted camera permissions")
#             print("4. Try restarting your computer")
#             print("=" * 50)
#             return
        
#         # Set camera properties
#         cap.set(cv2.CAP_PROP_FRAME_WIDTH, CAMERA_WIDTH)
#         cap.set(cv2.CAP_PROP_FRAME_HEIGHT, CAMERA_HEIGHT)
#         cap.set(cv2.CAP_PROP_FPS, CAMERA_FPS)
        
#         print("=" * 50)
#         print("AIR WRITING SYSTEM - READY!")
#         print("=" * 50)
#         print("Controls:")
#         print("  'w' - Write mode (draw with pinch gesture)")
#         print("  'c' - Collect data mode (collect samples for training)")
#         print("  't' - Train model on collected data")
#         print("  'r' - Recognize current drawing")
#         print("  'x' - Clear canvas")
#         print("  'q' - Quit")
#         print("-" * 50)
#         print("Writing gestures:")
#         print("  Pinch fingers (index + thumb) - Draw")
#         print("  Open palm or make fist - Stop drawing & recognize")
#         print("=" * 50)
        
#         frame_count = 0
#         while True:
#             ret, frame = cap.read()
#             if not ret or frame is None:
#                 frame_count += 1
#                 if frame_count > 30:  # Try for 1 second
#                     print("Warning: Lost camera feed. Attempting to reconnect...")
#                     break
#                 continue
            
#             frame_count = 0
            
#             # Flip frame horizontally for mirror effect
#             frame = cv2.flip(frame, 1)
#             frame = cv2.resize(frame, (CAMERA_WIDTH, CAMERA_HEIGHT))
            
#             # Process hand tracking
#             results = self.hand_tracker.process_frame(frame)
            
#             if results.multi_hand_landmarks:
#                 hand_landmarks = results.multi_hand_landmarks[0]
                
#                 # Get fingertip positions
#                 index_tip = self.hand_tracker.get_fingertip_position(
#                     hand_landmarks, self.hand_tracker.INDEX_TIP, frame.shape
#                 )
#                 thumb_tip = self.hand_tracker.get_fingertip_position(
#                     hand_landmarks, self.hand_tracker.THUMB_TIP, frame.shape
#                 )
#                 fingertips = self.hand_tracker.get_all_fingertips(hand_landmarks, frame.shape)
                
#                 # Update gesture state based on mode
#                 if self.mode == "WRITE":
#                     gesture_state = self.gesture_recognizer.update_gesture_state(
#                         index_tip, thumb_tip, fingertips
#                     )
                    
#                     if gesture_state == "WRITING":
#                         self.canvas.draw_point(index_tip)
#                     elif gesture_state == "STOP_WRITING":
#                         self.canvas.end_stroke()
#                         # Auto-recognize when writing stops
#                         if self.model_loaded and len(self.canvas.trajectory) > 10:
#                             self.recognize_drawing()
#                         self.canvas.clear_canvas()
                
#                 elif self.mode == "COLLECT":
#                     # Data collection mode
#                     gesture_state = self.gesture_recognizer.update_gesture_state(
#                         index_tip, thumb_tip, fingertips
#                     )
                    
#                     if gesture_state == "WRITING":
#                         self.canvas.draw_point(index_tip)
#                     elif gesture_state == "STOP_WRITING":
#                         self.canvas.end_stroke()
#                         # Save the drawing
#                         if len(self.canvas.trajectory) > 10:
#                             self.save_collected_data()
#                         self.canvas.clear_canvas()
                
#                 # Draw hand landmarks and fingertip
#                 self.hand_tracker.draw_landmarks(frame, hand_landmarks)
#                 cv2.circle(frame, index_tip, 10, (0, 255, 0), -1)
            
#             # Overlay canvas on frame
#             frame = self.canvas.overlay_on_frame(frame, 0.3)
            
#             # Display UI information
#             self.draw_ui(frame)
            
#             cv2.imshow(WINDOW_NAME, frame)
            
#             # Handle keyboard input
#             key = cv2.waitKey(1) & 0xFF
#             if key == ord('q'):
#                 break
#             elif key == ord('w'):
#                 self.mode = "WRITE"
#                 self.canvas.clear_canvas()
#                 print("Switched to WRITE mode")
#             elif key == ord('c'):
#                 self.mode = "COLLECT"
#                 self.canvas.clear_canvas()
#                 print("Switched to COLLECT mode")
#                 print(f"Current letter: {self.current_letter}")
#                 print("Press 'a' to 'z' to change letter")
#             elif key == ord('t'):
#                 self.train_model()
#             elif key == ord('r'):
#                 self.recognize_drawing()
#             elif key == ord('x'):
#                 self.canvas.clear_canvas()
#                 print("Canvas cleared")
#             elif self.mode == "COLLECT" and ord('a') <= key <= ord('z'):
#                 self.current_letter = chr(key).upper()
#                 print(f"Now collecting data for letter: {self.current_letter}")
        
#         cap.release()
#         cv2.destroyAllWindows()
#         self.hand_tracker.release()
#     def draw_ui(self, frame):
#         """Draw UI elements on the frame"""
#         # Mode indicator
#         mode_color = (0, 255, 0) if self.mode == "WRITE" else (255, 255, 0) if self.mode == "COLLECT" else (0, 255, 255)
#         cv2.putText(frame, f"Mode: {self.mode}", (10, 30), FONT, FONT_SCALE, mode_color, FONT_THICKNESS)
        
#         # Writing status
#         status = "WRITING" if self.gesture_recognizer.is_writing else "IDLE"
#         status_color = (0, 255, 0) if self.gesture_recognizer.is_writing else (0, 0, 255)
#         cv2.putText(frame, f"Status: {status}", (10, 60), FONT, FONT_SCALE, status_color, FONT_THICKNESS)
        
#         # Recognized text
#         if self.recognized_text:
#             cv2.putText(frame, f"Recognized: {self.recognized_text}", (10, 90), 
#                     FONT, FONT_SCALE, (255, 255, 0), FONT_THICKNESS)
        
#         # Collection mode info
#         if self.mode == "COLLECT":
#             cv2.putText(frame, f"Collecting: {self.current_letter}", (10, 120), 
#                     FONT, FONT_SCALE, (255, 255, 0), FONT_THICKNESS)
        
#         # Instructions
#         cv2.putText(frame, "Press 'q' to quit | 'x' clear | 'r' recognize", 
#                 (10, frame.shape[0] - 10), FONT, 0.5, (200, 200, 200), 1)

#     def recognize_drawing(self):
#         """Recognize the current drawing using the trained model"""
#         if not self.model_loaded:
#             print("No model loaded! Please train a model first (press 't').")
#             return
        
#         if len(self.canvas.trajectory) < 10:
#             print("Not enough points to recognize. Draw more!")
#             return
        
#         # Get trajectory image
#         img = self.canvas.get_trajectory_image()
        
#         # Prepare for prediction
#         img_array = img.reshape(1, IMAGE_SIZE[0], IMAGE_SIZE[1], 1) / 255.0
        
#         # Make prediction
#         try:
#             predictions = self.model_trainer.model.predict(img_array, verbose=0)
#             predicted_class = np.argmax(predictions[0])
#             confidence = np.max(predictions[0])
            
#             if confidence > RECOGNITION_CONFIDENCE_THRESHOLD:
#                 self.recognized_text = self.model_trainer.class_names[predicted_class]
#                 print(f"✓ Recognized: {self.recognized_text} (confidence: {confidence:.2f})")
#             else:
#                 print(f"Low confidence: {confidence:.2f}. Please try drawing more clearly.")
#                 self.recognized_text = "?"
#         except Exception as e:
#             print(f"Error during recognition: {e}")

#     def save_collected_data(self):
#         """Save the current drawing as training data"""
#         if self.mode != "COLLECT":
#             print("Not in collection mode! Press 'c' to enter collection mode.")
#             return
        
#         if len(self.canvas.trajectory) < 10:
#             print("Not enough points to save. Draw more!")
#             return
        
#         # Get trajectory image
#         img = self.canvas.get_trajectory_image()
        
#         # Save to appropriate directory
#         save_dir = os.path.join(DATA_COLLECTION_DIR, self.current_letter)
#         os.makedirs(save_dir, exist_ok=True)
        
#         # Find next available filename
#         existing_files = [f for f in os.listdir(save_dir) if f.endswith('.png')]
#         next_num = len(existing_files)
        
#         save_path = os.path.join(save_dir, f"{self.current_letter}_{next_num}.png")
#         cv2.imwrite(save_path, img)
        
#         print(f"✓ Saved sample {next_num + 1} for letter '{self.current_letter}'")
#         print(f"  Total samples for '{self.current_letter}': {next_num + 1}")


 
#     def train_model(self):
#         """Train the model on collected data"""
#         print("=" * 50)
#         print("Starting model training...")
#         print("=" * 50)
        
#         # Check if data directory exists
#         if not os.path.exists(DATA_COLLECTION_DIR):
#             print("No data directory found! Please collect data first (press 'c').")
#             return
        
#         # Count samples
#         total_samples = 0
#         letters_found = []
#         for letter_dir in os.listdir(DATA_COLLECTION_DIR):
#             letter_path = os.path.join(DATA_COLLECTION_DIR, letter_dir)
#             if os.path.isdir(letter_path):
#                 samples = len([f for f in os.listdir(letter_path) if f.endswith('.png')])
#                 if samples > 0:
#                     total_samples += samples
#                     letters_found.append(f"{letter_dir}: {samples} samples")
#                     print(f"  Letter '{letter_dir}': {samples} samples")
        
#         if total_samples == 0:
#             print("No training data found! Please collect data first (press 'c').")
#             return
        
#         if len(letters_found) < 2:
#             print(f"WARNING: Only found {len(letters_found)} letter(s). Need at least 2 letters to train.")
#             print("Please collect data for at least 2 different letters.")
#             return
        
#         print(f"\nTotal samples: {total_samples}")
#         print("Loading and preprocessing data...")
        
#         # Load data from the model_trainer
#         X, y = self.model_trainer.load_data()
        
#         if X is None or len(X) == 0:
#             print("Error loading data. Please check your data files.")
#             return
        
#         print(f"Loaded {len(X)} samples from {len(self.model_trainer.class_names)} classes")
#         print("Starting training (this may take a few minutes)...")
        
#         # Train the model
#         history = self.model_trainer.train_model(X, y)
        
#         if history:
#             self.model_loaded = True
#             print("\n✓✓✓ MODEL TRAINING SUCCESSFUL! ✓✓✓")
#             print("Model saved to: models/trained_model.h5")
#             print("\nNow you can:")
#             print("  1. Press 'w' to switch to WRITE mode")
#             print("  2. Draw letters in the air")
#             print("  3. Open your palm to see recognition results")
#         else:
#             print("\n✗ Model training failed.")

# if __name__ == "__main__":
#     # Create necessary directories
#     os.makedirs(DATA_COLLECTION_DIR, exist_ok=True)
#     os.makedirs('models', exist_ok=True)
    
#     # Run the application
#     system = AirWritingSystem()
#     system.run()

import cv2
import numpy as np
import os
import sys
import time
from .hand_tracker import HandTracker
from .gesture_recognizer import GestureRecognizer
from .canvas import VirtualCanvas
from .model_trainer import ModelTrainer
from .data_collector import DataCollector
from config.settings import *

class AirWritingSystem:
    def __init__(self):
        self.hand_tracker = HandTracker()
        self.gesture_recognizer = GestureRecognizer()
        self.canvas = VirtualCanvas()
        self.model_trainer = ModelTrainer()
        self.data_collector = DataCollector()
        
        # Try to load pre-trained model, but don't fail if it doesn't exist
        try:
            self.model_loaded = self.model_trainer.load_model()
        except Exception as e:
            print(f"Note: {e}")
            self.model_loaded = False
        
        # UI state
        self.mode = "WRITE"  # WRITE, COLLECT, TRAIN
        self.recognized_text = ""
        self.current_letter = "A"
        
        # Word mode state
        self.word_mode = False
        self.current_word = ""
        self.letter_buffer = []
        self.pen_was_up = False
        self.stroke_count = 0
        self.last_recognition_time = 0
        self.word_submitted = False
        
    # def run(self):
    #     """Main application loop"""
    #     # Initialize camera with better error handling
    #     cap = None
        
    #     # Try different camera indices and backends
    #     for backend in [cv2.CAP_DSHOW, cv2.CAP_ANY]:
    #         for idx in range(3):
    #             try:
    #                 test_cap = cv2.VideoCapture(idx, backend)
    #                 if test_cap.isOpened():
    #                     ret, test_frame = test_cap.read()
    #                     if ret and test_frame is not None:
    #                         cap = test_cap
    #                         print(f"✓ Camera opened: index {idx} with backend {backend}")
    #                         break
    #                 else:
    #                     test_cap.release()
    #             except:
    #                 continue
    #         if cap is not None:
    #             break
        
    #     if cap is None or not cap.isOpened():
    #         print("=" * 50)
    #         print("ERROR: Could not open any camera!")
    #         print("Please check:")
    #         print("1. Your webcam is connected")
    #         print("2. Camera is not being used by another app")
    #         print("3. You have granted camera permissions")
    #         print("4. Try restarting your computer")
    #         print("=" * 50)
    #         return
        
    #     # Set camera properties
    #     cap.set(cv2.CAP_PROP_FRAME_WIDTH, CAMERA_WIDTH)
    #     cap.set(cv2.CAP_PROP_FRAME_HEIGHT, CAMERA_HEIGHT)
    #     cap.set(cv2.CAP_PROP_FPS, CAMERA_FPS)
        
    #     print("=" * 50)
    #     print("AIR WRITING SYSTEM - READY!")
    #     print("=" * 50)
    #     print("Controls:")
    #     print("  'w' - Write mode (draw with pinch gesture)")
    #     print("  'c' - Collect data mode (collect samples for training)")
    #     print("  't' - Train model on collected data")
    #     print("  'b' - Toggle WORD MODE (continuous writing)")
    #     print("  's' - Submit current word")
    #     print("  'd' - Delete last letter")
    #     print("  'x' - Clear canvas/word")
    #     print("  'q' - Quit")
    #     print("-" * 50)
    #     print("Writing gestures:")
    #     print("  Pinch fingers (index + thumb) - Draw")
    #     print("  Open palm or make fist - Stop drawing")
    #     print("  In WORD MODE: Just lift fingers between letters!")
    #     print("=" * 50)
        
    #     frame_count = 0
    #     while True:
    #         ret, frame = cap.read()
    #         if not ret or frame is None:
    #             frame_count += 1
    #             if frame_count > 30:  # Try for 1 second
    #                 print("Warning: Lost camera feed. Attempting to reconnect...")
    #                 break
    #             continue
            
    #         frame_count = 0
            
    #         # Flip frame horizontally for mirror effect
    #         frame = cv2.flip(frame, 1)
    #         frame = cv2.resize(frame, (CAMERA_WIDTH, CAMERA_HEIGHT))
            
    #         # Process hand tracking
    #         results = self.hand_tracker.process_frame(frame)
            
    #         if results.multi_hand_landmarks:
    #             hand_landmarks = results.multi_hand_landmarks[0]
                
    #             # Get fingertip positions
    #             index_tip = self.hand_tracker.get_fingertip_position(
    #                 hand_landmarks, self.hand_tracker.INDEX_TIP, frame.shape
    #             )
    #             thumb_tip = self.hand_tracker.get_fingertip_position(
    #                 hand_landmarks, self.hand_tracker.THUMB_TIP, frame.shape
    #             )
    #             fingertips = self.hand_tracker.get_all_fingertips(hand_landmarks, frame.shape)
                
    #             # Update gesture state based on mode
    #             if self.mode == "WRITE":
    #                 gesture_state = self.gesture_recognizer.update_gesture_state(
    #                     index_tip, thumb_tip, fingertips
    #                 )
                    
    #                 # --- WORD MODE: Continuous Stroke Detection ---
    #                 if self.word_mode:
    #                     # Detect pen lift (letter boundary)
    #                     if self.detect_pen_lift(gesture_state):
    #                         # Pen was lifted - recognize the stroke
    #                         if len(self.canvas.trajectory) > 10:
    #                             print("🔄 Letter boundary detected - recognizing stroke...")
    #                             letter = self.recognize_and_add_letter()
    #                             if letter:
    #                                 print(f"✅ Added '{letter}' to word")
    #                             # Clear canvas for next letter
    #                             self.canvas.clear_canvas()
    #                         else:
    #                             # Too small to recognize, just clear
    #                             self.canvas.clear_canvas()
                        
    #                     # Handle writing
    #                     if gesture_state == "WRITING":
    #                         self.canvas.draw_point(index_tip)
                        
    #                     elif gesture_state == "STOP_WRITING":
    #                         self.canvas.end_stroke()
    #                         # Don't clear canvas in word mode - let user see what they drew
                    
    #                 # --- SINGLE LETTER MODE ---
    #                 else:
    #                     if gesture_state == "WRITING":
    #                         self.canvas.draw_point(index_tip)
    #                     elif gesture_state == "STOP_WRITING":
    #                         self.canvas.end_stroke()
    #                         # Auto-recognize when writing stops
    #                         if self.model_loaded and len(self.canvas.trajectory) > 10:
    #                             self.recognize_drawing()
    #                         self.canvas.clear_canvas()
                
    #             elif self.mode == "COLLECT":
    #                 # Data collection mode
    #                 gesture_state = self.gesture_recognizer.update_gesture_state(
    #                     index_tip, thumb_tip, fingertips
    #                 )
                    
    #                 if gesture_state == "WRITING":
    #                     self.canvas.draw_point(index_tip)
    #                 elif gesture_state == "STOP_WRITING":
    #                     self.canvas.end_stroke()
    #                     # Save the drawing
    #                     if len(self.canvas.trajectory) > 10:
    #                         self.save_collected_data()
    #                     self.canvas.clear_canvas()
                
    #             # Draw hand landmarks and fingertip
    #             self.hand_tracker.draw_landmarks(frame, hand_landmarks)
    #             cv2.circle(frame, index_tip, 10, (0, 255, 0), -1)
            
    #         # Overlay canvas on frame
    #         frame = self.canvas.overlay_on_frame(frame, 0.3)
            
    #         # Display UI information
    #         self.draw_ui(frame)
            
    #         cv2.imshow(WINDOW_NAME, frame)
            
    #         # Handle keyboard input
    #         key = cv2.waitKey(1) & 0xFF
    #         if key == ord('q'):
    #             break
    #         elif key == ord('w'):
    #             self.mode = "WRITE"
    #             self.canvas.clear_canvas()
    #             print("Switched to WRITE mode")
    #             if self.word_mode:
    #                 print("🔤 Word mode is still ON. Press 'b' to disable.")
    #         elif key == ord('c'):
    #             self.mode = "COLLECT"
    #             self.canvas.clear_canvas()
    #             print("Switched to COLLECT mode")
    #             print(f"Current letter: {self.current_letter}")
    #             print("Press 'a' to 'z' to change letter")
    #         elif key == ord('t'):
    #             self.train_model()
    #         elif key == ord('r'):
    #             if not self.word_mode:
    #                 self.recognize_drawing()
    #             else:
    #                 print("In word mode, letters are recognized automatically on pen lift!")
    #         elif key == ord('x'):
    #             self.canvas.clear_canvas()
    #             if self.word_mode:
    #                 self.clear_word()
    #             print("Canvas cleared")
    #         elif key == ord('b'):  # Toggle word mode
    #             self.toggle_word_mode()
    #         elif key == ord('s'):  # Submit word
    #             self.submit_word()
    #         elif key == ord('d'):  # Delete last letter
    #             self.delete_last_letter()
    #         elif self.mode == "COLLECT" and ord('a') <= key <= ord('z'):
    #             self.current_letter = chr(key).upper()
    #             print(f"Now collecting data for letter: {self.current_letter}")
        
    #     cap.release()
    #     cv2.destroyAllWindows()
    #     self.hand_tracker.release()
    
    def run(self):
        """Main application loop"""
        # Initialize camera with better error handling
        cap = None
        
        # Try different camera indices and backends
        for backend in [cv2.CAP_DSHOW, cv2.CAP_ANY]:
            for idx in range(3):
                try:
                    test_cap = cv2.VideoCapture(idx, backend)
                    if test_cap.isOpened():
                        ret, test_frame = test_cap.read()
                        if ret and test_frame is not None:
                            cap = test_cap
                            print(f"✓ Camera opened: index {idx} with backend {backend}")
                            break
                    else:
                        test_cap.release()
                except:
                    continue
            if cap is not None:
                break
        
        if cap is None or not cap.isOpened():
            print("=" * 50)
            print("ERROR: Could not open any camera!")
            print("Please check:")
            print("1. Your webcam is connected")
            print("2. Camera is not being used by another app")
            print("3. You have granted camera permissions")
            print("4. Try restarting your computer")
            print("=" * 50)
            return
        
        # Set camera properties
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, CAMERA_WIDTH)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, CAMERA_HEIGHT)
        cap.set(cv2.CAP_PROP_FPS, CAMERA_FPS)
        
        print("=" * 50)
        print("AIR WRITING SYSTEM - READY!")
        print("=" * 50)
        print("Controls:")
        print("  'w' - Write mode (draw with pinch gesture)")
        print("  'c' - Collect data mode (collect samples for training)")
        print("  't' - Train model on collected data")
        print("  'b' - Toggle WORD MODE (continuous writing)")
        print("  's' - Submit current word")
        print("  'd' - Delete last letter")
        print("  'x' - Clear canvas/word")
        print("  'q' - Quit")
        print("-" * 50)
        print("Writing gestures:")
        print("  Pinch fingers (index + thumb) - Draw")
        print("  Open palm or make fist - Stop drawing")
        print("  In WORD MODE: Just lift fingers between letters!")
        print("=" * 50)
        
        frame_count = 0
        # For word mode tracking
        letter_recognized_this_stroke = False
        
        while True:
            ret, frame = cap.read()
            if not ret or frame is None:
                frame_count += 1
                if frame_count > 30:
                    print("Warning: Lost camera feed. Attempting to reconnect...")
                    break
                continue
            
            frame_count = 0
            
            # Flip frame horizontally for mirror effect
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
                
                # --- WRITE MODE ---
                if self.mode == "WRITE":
                    
                    # --- WORD MODE: Continuous Stroke Detection ---
                    if self.word_mode:
                        
                        # If we're writing, draw
                        if gesture_state == "WRITING":
                            self.canvas.draw_point(index_tip)
                            letter_recognized_this_stroke = False
                        
                        # If we just stopped writing (pen lift detected)
                        elif gesture_state == "STOP_WRITING":
                            self.canvas.end_stroke()
                            
                            # Only recognize if we have enough points and haven't recognized this stroke yet
                            if len(self.canvas.trajectory) > 10 and not letter_recognized_this_stroke:
                                print("🔄 Pen lifted - recognizing stroke...")
                                letter = self.recognize_and_add_letter()
                                if letter:
                                    letter_recognized_this_stroke = True
                                    print(f"✅ Added '{letter}' to word")
                                else:
                                    print("⚠️ Could not recognize letter. Try again.")
                            
                            # Don't clear canvas immediately - let user see what they drew
                            # It will be cleared on next pen-down
                        
                        # If we're idle (hand detected but not writing)
                        elif gesture_state == "IDLE":
                            pass  # Keep the drawing visible
                    
                    # --- SINGLE LETTER MODE ---
                    else:
                        if gesture_state == "WRITING":
                            self.canvas.draw_point(index_tip)
                        elif gesture_state == "STOP_WRITING":
                            self.canvas.end_stroke()
                            if self.model_loaded and len(self.canvas.trajectory) > 10:
                                self.recognize_drawing()
                            # Clear after a moment in single mode
                            self.canvas.clear_canvas()
                
                # --- COLLECT MODE ---
                elif self.mode == "COLLECT":
                    if gesture_state == "WRITING":
                        self.canvas.draw_point(index_tip)
                    elif gesture_state == "STOP_WRITING":
                        self.canvas.end_stroke()
                        if len(self.canvas.trajectory) > 10:
                            self.save_collected_data()
                        self.canvas.clear_canvas()
                
                # Draw hand landmarks and fingertip
                self.hand_tracker.draw_landmarks(frame, hand_landmarks)
                cv2.circle(frame, index_tip, 10, (0, 255, 0), -1)
            
            # Overlay canvas on frame
            frame = self.canvas.overlay_on_frame(frame, 0.3)
            
            # Display UI information
            self.draw_ui(frame)
            
            cv2.imshow(WINDOW_NAME, frame)
            
            # Handle keyboard input
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break
            elif key == ord('w'):
                self.mode = "WRITE"
                self.canvas.clear_canvas()
                print("Switched to WRITE mode")
                if self.word_mode:
                    print("🔤 Word mode is still ON. Press 'b' to disable.")
            elif key == ord('c'):
                self.mode = "COLLECT"
                self.canvas.clear_canvas()
                print("Switched to COLLECT mode")
                print(f"Current letter: {self.current_letter}")
                print("Press 'a' to 'z' to change letter")
            elif key == ord('t'):
                self.train_model()
            elif key == ord('r'):
                if not self.word_mode:
                    self.recognize_drawing()
                else:
                    print("In word mode, letters are recognized automatically on pen lift!")
            elif key == ord('x'):
                self.canvas.clear_canvas()
                if self.word_mode:
                    self.clear_word()
                print("Canvas cleared")
            elif key == ord('b'):
                self.toggle_word_mode()
                if self.word_mode:
                    # Reset the recognition flag when entering word mode
                    letter_recognized_this_stroke = False
            elif key == ord('s'):
                self.submit_word()
                if self.word_mode:
                    # Reset the recognition flag after submitting
                    letter_recognized_this_stroke = False
            elif key == ord('d'):
                self.delete_last_letter()
            elif self.mode == "COLLECT" and ord('a') <= key <= ord('z'):
                self.current_letter = chr(key).upper()
                print(f"Now collecting data for letter: {self.current_letter}")
        
        cap.release()
        cv2.destroyAllWindows()
        self.hand_tracker.release() 
    
    def detect_pen_lift(self, gesture_state):
        """
        Detect pen lift (finger un-pinch) to separate letters
        Returns True if pen was lifted (boundary between letters)
        """
        if gesture_state == "STOP_WRITING" or gesture_state == "IDLE":
            if not self.pen_was_up:
                self.pen_was_up = True
                # Only count as letter boundary if we actually drew something
                if len(self.canvas.trajectory) > 10:
                    return True
        else:
            self.pen_was_up = False
        return False
    
    # def recognize_and_add_letter(self):
    #     """Recognize current drawing and add to word"""
    #     if len(self.canvas.trajectory) < 10:
    #         return None
        
    #     # Get trajectory image
    #     img = self.canvas.get_trajectory_image()
    #     img_array = img.reshape(1, IMAGE_SIZE[0], IMAGE_SIZE[1], 1) / 255.0
        
    #     try:
    #         predictions = self.model_trainer.model.predict(img_array, verbose=0)
    #         predicted_class = np.argmax(predictions[0])
    #         confidence = np.max(predictions[0])
            
    #         if confidence > RECOGNITION_CONFIDENCE_THRESHOLD:
    #             letter = self.model_trainer.class_names[predicted_class]
    #             print(f"✓ Recognized: {letter} (confidence: {confidence:.2f})")
                
    #             # Add to word
    #             self.current_word += letter
    #             self.letter_buffer.append(letter)
    #             print(f"📝 Current word: {self.current_word}")
    #             self.recognized_text = self.current_word
                
    #             return letter
    #         else:
    #             print(f"Low confidence: {confidence:.2f}")
    #             return None
                
    #     except Exception as e:
    #         print(f"Recognition error: {e}")
    #         return None
    
    def recognize_and_add_letter(self):
        """Recognize current drawing and add to word"""
        if len(self.canvas.trajectory) < 10:
            print(f"⚠️ Only {len(self.canvas.trajectory)} points - need at least 10")
            return None
        
        # Get trajectory image
        img = self.canvas.get_trajectory_image()
        img_array = img.reshape(1, IMAGE_SIZE[0], IMAGE_SIZE[1], 1) / 255.0
        
        try:
            predictions = self.model_trainer.model.predict(img_array, verbose=0)
            predicted_class = np.argmax(predictions[0])
            confidence = np.max(predictions[0])
            
            print(f"Confidence: {confidence:.2f}")
            
            if confidence > RECOGNITION_CONFIDENCE_THRESHOLD:
                letter = self.model_trainer.class_names[predicted_class]
                
                # Add to word
                self.current_word += letter
                self.letter_buffer.append(letter)
                print(f"📝 Current word: {self.current_word}")
                self.recognized_text = self.current_word
                
                # Clear canvas AFTER successful recognition for next letter
                self.canvas.clear_canvas()
                
                return letter
            else:
                print(f"Low confidence: {confidence:.2f}. Please try again.")
                # Don't clear canvas - let user see what they drew
                return None
                    
        except Exception as e:
            print(f"Recognition error: {e}")
            return None

    def submit_word(self):
        """Submit the complete word"""
        if self.current_word:
            print("=" * 50)
            print(f"✅ COMPLETE WORD: {self.current_word}")
            if self.letter_buffer:
                print(f"📊 Letters: {' → '.join(self.letter_buffer)}")
            print("=" * 50)
            
            # Save to a file
            try:
                with open("recognized_words.txt", "a") as f:
                    f.write(f"{self.current_word}\n")
                print("💾 Word saved to recognized_words.txt")
            except:
                pass
            
            # Clear the word
            self.current_word = ""
            self.letter_buffer = []
            self.recognized_text = ""
            self.canvas.clear_canvas()
            self.word_submitted = True
        else:
            print("No word to submit. Write some letters first!")
    
    def delete_last_letter(self):
        """Delete the last letter from the word"""
        if self.current_word:
            self.current_word = self.current_word[:-1]
            if self.letter_buffer:
                self.letter_buffer.pop()
            self.recognized_text = self.current_word if self.current_word else ""
            print(f"🗑️  Deleted last letter. Current word: {self.current_word}")
            if not self.current_word:
                print("Word is now empty")
        else:
            print("No letters to delete")
    
    def clear_canvas_for_next_letter(self):
        """Clear the canvas when starting a new letter in word mode"""
        self.canvas.clear_canvas()
        print("🔄 Ready for next letter...")

    def clear_word(self):
        """Clear the current word"""
        if self.current_word:
            self.current_word = ""
            self.letter_buffer = []
            self.recognized_text = ""
            print("🗑️  Word cleared")
    
    def draw_ui(self, frame):
        """Draw UI elements on the frame"""
        h, w = frame.shape[:2]
        
        # Mode indicator
        mode_color = (0, 255, 0) if self.mode == "WRITE" else (255, 255, 0) if self.mode == "COLLECT" else (0, 255, 255)
        cv2.putText(frame, f"Mode: {self.mode}", (10, 30), FONT, FONT_SCALE, mode_color, FONT_THICKNESS)
        
        # Word mode indicator
        if self.word_mode:
            # Highlight word mode
            cv2.putText(frame, "🔤 WORD MODE", (10, 60), FONT, 0.7, (0, 255, 255), FONT_THICKNESS)
            
            # Show current word (large, centered)
            if self.current_word:
                text_size = cv2.getTextSize(self.current_word, FONT, 1.5, 3)[0]
                x_pos = max(10, (w - text_size[0]) // 2)
                cv2.putText(frame, self.current_word, (x_pos, 100), FONT, 1.5, (0, 255, 0), 3)
                
                # Show letter count
                cv2.putText(frame, f"Letters: {len(self.letter_buffer)}", (10, 130), 
                           FONT, 0.6, (200, 200, 200), 1)
            
            # Show letter buffer
            if self.letter_buffer:
                letters_str = " → ".join(self.letter_buffer)
                max_len = 30
                if len(letters_str) > max_len:
                    letters_str = letters_str[:max_len] + "..."
                cv2.putText(frame, f"Sequence: {letters_str}", (10, h - 40), 
                           FONT, 0.5, (200, 200, 200), 1)
        else:
            # Single character mode
            status = "WRITING" if self.gesture_recognizer.is_writing else "IDLE"
            status_color = (0, 255, 0) if self.gesture_recognizer.is_writing else (0, 0, 255)
            cv2.putText(frame, f"Status: {status}", (10, 60), FONT, FONT_SCALE, status_color, FONT_THICKNESS)
            
            if self.recognized_text:
                cv2.putText(frame, f"Recognized: {self.recognized_text}", (10, 90), 
                           FONT, FONT_SCALE, (255, 255, 0), FONT_THICKNESS)
        
        # Collection mode info
        if self.mode == "COLLECT":
            cv2.putText(frame, f"Collecting: {self.current_letter}", (10, 120), 
                       FONT, FONT_SCALE, (255, 255, 0), FONT_THICKNESS)
            # Show sample count
            save_dir = os.path.join(DATA_COLLECTION_DIR, self.current_letter)
            if os.path.exists(save_dir):
                samples = len([f for f in os.listdir(save_dir) if f.endswith('.png')])
                cv2.putText(frame, f"Samples: {samples}", (10, 150), 
                           FONT, 0.7, (255, 255, 0), 1)
        
        # Instructions
        if self.word_mode:
            cv2.putText(frame, "'q' quit | 's' submit | 'd' delete | 'x' clear | 'b' exit word mode", 
                       (10, h - 10), FONT, 0.5, (200, 200, 200), 1)
        else:
            cv2.putText(frame, "'q' quit | 'x' clear | 'r' recognize | 'b' word mode", 
                       (10, h - 10), FONT, 0.5, (200, 200, 200), 1)

    def recognize_drawing(self):
        """Recognize the current drawing using the trained model"""
        if not self.model_loaded:
            print("No model loaded! Please train a model first (press 't').")
            return
        
        if len(self.canvas.trajectory) < 10:
            print("Not enough points to recognize. Draw more!")
            return
        
        # Get trajectory image
        img = self.canvas.get_trajectory_image()
        
        # Prepare for prediction
        img_array = img.reshape(1, IMAGE_SIZE[0], IMAGE_SIZE[1], 1) / 255.0
        
        # Make prediction
        try:
            predictions = self.model_trainer.model.predict(img_array, verbose=0)
            predicted_class = np.argmax(predictions[0])
            confidence = np.max(predictions[0])
            
            if confidence > RECOGNITION_CONFIDENCE_THRESHOLD:
                self.recognized_text = self.model_trainer.class_names[predicted_class]
                print(f"✓ Recognized: {self.recognized_text} (confidence: {confidence:.2f})")
            else:
                print(f"Low confidence: {confidence:.2f}. Please try drawing more clearly.")
                self.recognized_text = "?"
        except Exception as e:
            print(f"Error during recognition: {e}")

    def save_collected_data(self):
        """Save the current drawing as training data"""
        if self.mode != "COLLECT":
            print("Not in collection mode! Press 'c' to enter collection mode.")
            return
        
        if len(self.canvas.trajectory) < 10:
            print("Not enough points to save. Draw more!")
            return
        
        # Get trajectory image
        img = self.canvas.get_trajectory_image()
        
        # Save to appropriate directory
        save_dir = os.path.join(DATA_COLLECTION_DIR, self.current_letter)
        os.makedirs(save_dir, exist_ok=True)
        
        # Find next available filename
        existing_files = [f for f in os.listdir(save_dir) if f.endswith('.png')]
        next_num = len(existing_files)
        
        save_path = os.path.join(save_dir, f"{self.current_letter}_{next_num}.png")
        cv2.imwrite(save_path, img)
        
        print(f"✓ Saved sample {next_num + 1} for letter '{self.current_letter}'")
        print(f"  Total samples for '{self.current_letter}': {next_num + 1}")

    def train_model(self):
        """Train the model on collected data"""
        print("=" * 50)
        print("Starting model training...")
        print("=" * 50)
        
        # Check if data directory exists
        if not os.path.exists(DATA_COLLECTION_DIR):
            print("No data directory found! Please collect data first (press 'c').")
            return
        
        # Count samples
        total_samples = 0
        letters_found = []
        for letter_dir in os.listdir(DATA_COLLECTION_DIR):
            letter_path = os.path.join(DATA_COLLECTION_DIR, letter_dir)
            if os.path.isdir(letter_path):
                samples = len([f for f in os.listdir(letter_path) if f.endswith('.png')])
                if samples > 0:
                    total_samples += samples
                    letters_found.append(f"{letter_dir}: {samples} samples")
                    print(f"  Letter '{letter_dir}': {samples} samples")
        
        if total_samples == 0:
            print("No training data found! Please collect data first (press 'c').")
            return
        
        if len(letters_found) < 2:
            print(f"WARNING: Only found {len(letters_found)} letter(s). Need at least 2 letters to train.")
            print("Please collect data for at least 2 different letters.")
            return
        
        print(f"\nTotal samples: {total_samples}")
        print("Loading and preprocessing data...")
        
        # Load data from the model_trainer
        X, y = self.model_trainer.load_data()
        
        if X is None or len(X) == 0:
            print("Error loading data. Please check your data files.")
            return
        
        print(f"Loaded {len(X)} samples from {len(self.model_trainer.class_names)} classes")
        print("Starting training (this may take a few minutes)...")
        
        # Train the model
        history = self.model_trainer.train_model(X, y)
        
        if history:
            self.model_loaded = True
            print("\n✓✓✓ MODEL TRAINING SUCCESSFUL! ✓✓✓")
            print("Model saved to: models/trained_model.h5")
            print("\nNow you can:")
            print("  1. Press 'w' to switch to WRITE mode")
            print("  2. Press 'b' to enable WORD MODE")
            print("  3. Write continuously, lifting fingers between letters")
            print("  4. Press 's' to submit your word")
        else:
            print("\n✗ Model training failed.")

if __name__ == "__main__":
    # Create necessary directories
    os.makedirs(DATA_COLLECTION_DIR, exist_ok=True)
    os.makedirs('models', exist_ok=True)
    
    # Run the application
    system = AirWritingSystem()
    system.run()