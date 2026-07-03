import cv2
import numpy as np
from scipy import interpolate

def smooth_trajectory(points, smoothing_factor=0.1):
    """Smooth the trajectory using interpolation"""
    if len(points) < 4:
        return points
    
    points = np.array(points)
    x = points[:, 0]
    y = points[:, 1]
    
    # Create parameter t
    t = np.linspace(0, 1, len(points))
    
    # Create interpolation functions
    fx = interpolate.interp1d(t, x, kind='quadratic')
    fy = interpolate.interp1d(t, y, kind='quadratic')
    
    # Generate smooth points
    t_smooth = np.linspace(0, 1, len(points) * 2)
    x_smooth = fx(t_smooth)
    y_smooth = fy(t_smooth)
    
    return np.column_stack((x_smooth, y_smooth)).astype(np.int32)

def normalize_trajectory(points, target_size=(28, 28)):
    """Normalize trajectory to fit in target image size"""
    if len(points) == 0:
        return points
    
    points = np.array(points)
    min_x, min_y = points.min(axis=0)
    max_x, max_y = points.max(axis=0)
    
    # Add padding
    padding_x = (max_x - min_x) * 0.1
    padding_y = (max_y - min_y) * 0.1
    
    min_x -= padding_x
    max_x += padding_x
    min_y -= padding_y
    max_y += padding_y
    
    # Scale to target size
    width_range = max_x - min_x
    height_range = max_y - min_y
    
    if width_range == 0:
        width_range = 1
    if height_range == 0:
        height_range = 1
    
    normalized = []
    for point in points:
        x = int(((point[0] - min_x) / width_range) * target_size[0])
        y = int(((point[1] - min_y) / height_range) * target_size[1])
        x = max(0, min(x, target_size[0]-1))
        y = max(0, min(y, target_size[1]-1))
        normalized.append((x, y))
    
    return np.array(normalized)

def augment_data(image):
    """Apply data augmentation to increase dataset size"""
    augmented = []
    
    # Original
    augmented.append(image)
    
    # Rotation
    rows, cols = image.shape
    M = cv2.getRotationMatrix2D((cols/2, rows/2), 15, 1)
    rotated = cv2.warpAffine(image, M, (cols, rows))
    augmented.append(rotated)
    
    M = cv2.getRotationMatrix2D((cols/2, rows/2), -15, 1)
    rotated = cv2.warpAffine(image, M, (cols, rows))
    augmented.append(rotated)
    
    # Translation
    M = np.float32([[1, 0, 3], [0, 1, 3]])
    translated = cv2.warpAffine(image, M, (cols, rows))
    augmented.append(translated)
    
    # Scaling
    scaled = cv2.resize(image, None, fx=0.9, fy=0.9)
    scaled = cv2.resize(scaled, (cols, rows))
    augmented.append(scaled)
    
    return augmented