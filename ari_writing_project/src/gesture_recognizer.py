import numpy as np

from config.settings import *

class GestureRecognizer:
    def __init__(self):
        self.last_gesture_frame = 0
        self.current_frame = 0
        self.is_writing = False
        self.gesture_history = []
        
    def calculate_distance(self, point1, point2):
        """Calculate Euclidean distance between two points"""
        return np.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)
    
    def is_pinch_gesture(self, index_tip, thumb_tip):
        """Detect if index finger and thumb are pinched"""
        distance = self.calculate_distance(index_tip, thumb_tip)
        return distance < PINCH_THRESHOLD * CAMERA_WIDTH
    
    def is_fist_gesture(self, fingertips):
        """Detect if hand is making a fist (all fingertips close together)"""
        # Get all fingertip positions
        positions = list(fingertips.values())
        if len(positions) < 2:
            return False
        
        # Calculate spread of fingertips
        center = np.mean(positions, axis=0)
        distances = [self.calculate_distance(pos, center) for pos in positions]
        avg_distance = np.mean(distances)
        
        return avg_distance < 50  # Threshold for fist
    
    def is_open_palm(self, fingertips):
        """Detect if hand is open (all fingers spread)"""
        positions = list(fingertips.values())
        if len(positions) < 2:
            return False
        
        # Calculate spread of fingertips
        center = np.mean(positions, axis=0)
        distances = [self.calculate_distance(pos, center) for pos in positions]
        avg_distance = np.mean(distances)
        
        return avg_distance > 100  # Threshold for open palm
    
    def update_gesture_state(self, index_tip, thumb_tip, fingertips=None):
        """Update the current gesture state"""
        self.current_frame += 1
        
        # Check for pinch gesture (start/continue writing)
        if self.is_pinch_gesture(index_tip, thumb_tip):
            if not self.is_writing and self.current_frame - self.last_gesture_frame > GESTURE_COOLDOWN_FRAMES:
                self.is_writing = True
                self.last_gesture_frame = self.current_frame
                return "START_WRITING"
            elif self.is_writing:
                return "WRITING"
        
        # Check for stop gesture (open palm or fist)
        elif fingertips and (self.is_open_palm(fingertips) or self.is_fist_gesture(fingertips)):
            if self.is_writing and self.current_frame - self.last_gesture_frame > GESTURE_COOLDOWN_FRAMES:
                self.is_writing = False
                self.last_gesture_frame = self.current_frame
                return "STOP_WRITING"
        
        return "IDLE"
    
    def reset(self):
        """Reset gesture recognizer state"""
        self.is_writing = False
        self.current_frame = 0
        self.last_gesture_frame = 0