import cv2
import numpy as np
from config.settings import *

class VirtualCanvas:
    def __init__(self, width=CANVAS_WIDTH, height=CANVAS_HEIGHT):
        self.width = width
        self.height = height
        self.canvas = np.zeros((height, width, 3), dtype=np.uint8)
        self.last_point = None
        self.trajectory = []  # Store all points for recognition
        self.current_stroke = []  # Current stroke points
        
    def clear_canvas(self):
        """Clear the canvas"""
        self.canvas = np.zeros((self.height, self.width, 3), dtype=np.uint8)
        self.trajectory = []
        self.current_stroke = []
        self.last_point = None
        
    def draw_point(self, point, color=DRAWING_COLOR, thickness=DRAWING_THICKNESS):
        """Draw a single point on the canvas"""
        if point is None:
            return
        
        # Draw circle at the point
        cv2.circle(self.canvas, point, thickness//2, color, -1)
        
        # Draw line from last point if exists
        if self.last_point is not None:
            cv2.line(self.canvas, self.last_point, point, color, thickness)
        
        self.last_point = point
        self.current_stroke.append(point)
        self.trajectory.append(point)
        
    def end_stroke(self):
        """End the current stroke"""
        self.current_stroke = []
        self.last_point = None
        
    def get_canvas_image(self):
        """Get the current canvas image"""
        return self.canvas.copy()
    
    def get_trajectory_image(self, size=IMAGE_SIZE):
        """Convert trajectory to image for recognition"""
        # Create blank image
        img = np.zeros((size[1], size[0]), dtype=np.uint8)
        
        if len(self.trajectory) < 5:
            return img
        
        # Normalize trajectory points to fit in the image
        points = np.array(self.trajectory)
        min_x, min_y = points.min(axis=0)
        max_x, max_y = points.max(axis=0)
        
        # Add padding
        padding = 20
        width_range = max_x - min_x + 2*padding
        height_range = max_y - min_y + 2*padding
        
        if width_range == 0 or height_range == 0:
            return img
        
        # Scale and translate points
        scaled_points = []
        for point in points:
            x = int(((point[0] - min_x + padding) / width_range) * size[0])
            y = int(((point[1] - min_y + padding) / height_range) * size[1])
            # Clamp to image bounds
            x = max(0, min(x, size[0]-1))
            y = max(0, min(y, size[1]-1))
            scaled_points.append((x, y))
        
        # Draw the trajectory on the image
        for i in range(1, len(scaled_points)):
            cv2.line(img, scaled_points[i-1], scaled_points[i], 255, 2)
        
        # Apply Gaussian blur to smooth the image
        img = cv2.GaussianBlur(img, (3, 3), 0)
        
        return img
    
    def overlay_on_frame(self, frame, alpha=0.5):
        """Overlay canvas on the camera frame"""
        return cv2.addWeighted(frame, 1-alpha, self.canvas, alpha, 0)