import matplotlib.pyplot as plt
import numpy as np
import cv2

def plot_training_history(history):
    """Plot training history"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))
    
    # Plot accuracy
    ax1.plot(history.history['accuracy'], label='Training Accuracy')
    ax1.plot(history.history['val_accuracy'], label='Validation Accuracy')
    ax1.set_title('Model Accuracy')
    ax1.set_xlabel('Epoch')
    ax1.set_ylabel('Accuracy')
    ax1.legend()
    
    # Plot loss
    ax2.plot(history.history['loss'], label='Training Loss')
    ax2.plot(history.history['val_loss'], label='Validation Loss')
    ax2.set_title('Model Loss')
    ax2.set_xlabel('Epoch')
    ax2.set_ylabel('Loss')
    ax2.legend()
    
    plt.tight_layout()
    plt.show()

def display_confusion_matrix(cm, class_names):
    """Display confusion matrix"""
    plt.figure(figsize=(10, 8))
    plt.imshow(cm, interpolation='nearest', cmap=plt.cm.Blues)
    plt.title('Confusion Matrix')
    plt.colorbar()
    
    tick_marks = np.arange(len(class_names))
    plt.xticks(tick_marks, class_names, rotation=45)
    plt.yticks(tick_marks, class_names)
    
    # Add text annotations
    thresh = cm.max() / 2.
    for i in range(cm.shape[0]):
        for j in range(cm.shape[1]):
            plt.text(j, i, format(cm[i, j], 'd'),
                    horizontalalignment="center",
                    color="white" if cm[i, j] > thresh else "black")
    
    plt.ylabel('True label')
    plt.xlabel('Predicted label')
    plt.tight_layout()
    plt.show()

def visualize_trajectory(trajectory, save_path=None):
    """Visualize the writing trajectory"""
    if len(trajectory) == 0:
        return
    
    trajectory = np.array(trajectory)
    
    plt.figure(figsize=(8, 6))
    plt.plot(trajectory[:, 0], trajectory[:, 1], 'b-', linewidth=2)
    plt.plot(trajectory[0, 0], trajectory[0, 1], 'go', label='Start')
    plt.plot(trajectory[-1, 0], trajectory[-1, 1], 'ro', label='End')
    plt.title('Writing Trajectory')
    plt.xlabel('X coordinate')
    plt.ylabel('Y coordinate')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.gca().invert_yaxis()  # Invert Y axis to match image coordinates
    
    if save_path:
        plt.savefig(save_path)
    plt.show()