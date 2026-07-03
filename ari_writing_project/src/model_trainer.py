import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import numpy as np
import cv2
import os
from sklearn.model_selection import train_test_split
from config.settings import *
from models.cnn_model import create_cnn_model

class ModelTrainer:
    def __init__(self):
        self.model = None
        self.class_names = []
        
    def load_data(self, data_dir=DATA_COLLECTION_DIR):
        """Load collected data for training"""
        images = []
        labels = []
        self.class_names = []
        
        # Get all letter directories
        if not os.path.exists(data_dir):
            print(f"Data directory {data_dir} not found!")
            return None, None
        
        for letter_dir in sorted(os.listdir(data_dir)):
            letter_path = os.path.join(data_dir, letter_dir)
            if os.path.isdir(letter_path):
                self.class_names.append(letter_dir)
                label = len(self.class_names) - 1
                
                # Load all images for this letter
                for img_file in os.listdir(letter_path):
                    if img_file.endswith(('.png', '.jpg', '.jpeg')):
                        img_path = os.path.join(letter_path, img_file)
                        img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
                        if img is not None:
                            img = cv2.resize(img, IMAGE_SIZE)
                            images.append(img)
                            labels.append(label)
        
        if not images:
            print("No data found! Please collect data first.")
            return None, None
        
        # Convert to numpy arrays
        X = np.array(images).reshape(-1, IMAGE_SIZE[0], IMAGE_SIZE[1], 1)
        y = np.array(labels)
        
        # Normalize pixel values
        X = X / 255.0
        
        return X, y
    
    def train_model(self, X, y):
        """Train the CNN model"""
        if X is None or y is None:
            return None
        
        # Split data
        X_train, X_val, y_train, y_val = train_test_split(
            X, y, test_size=VALIDATION_SPLIT, random_state=42, stratify=y
        )
        
        # Create model
        self.model = create_cnn_model(IMAGE_SIZE[0], IMAGE_SIZE[1], len(self.class_names))
        
        # Compile model
        self.model.compile(
            optimizer=keras.optimizers.Adam(learning_rate=LEARNING_RATE),
            loss='sparse_categorical_crossentropy',
            metrics=['accuracy']
        )
        
        # Callbacks
        callbacks = [
            keras.callbacks.EarlyStopping(patience=10, restore_best_weights=True),
            keras.callbacks.ReduceLROnPlateau(factor=0.5, patience=5),
            keras.callbacks.ModelCheckpoint('models/trained_model.h5', save_best_only=True)
        ]
        
        # Train model
        history = self.model.fit(
            X_train, y_train,
            validation_data=(X_val, y_val),
            epochs=EPOCHS,
            batch_size=BATCH_SIZE,
            callbacks=callbacks,
            verbose=1
        )
        
        # Evaluate model
        test_loss, test_acc = self.model.evaluate(X_val, y_val)
        print(f"Validation accuracy: {test_acc:.4f}")
        
        # Save model
        self.model.save('models/trained_model.h5')
        print("Model saved to models/trained_model.h5")
        
        return history
    
    def load_model(self, model_path='models/trained_model.h5'):
        """Load a trained model"""
        if os.path.exists(model_path):
            try:
                self.model = keras.models.load_model(model_path)
                print(f"Model loaded from {model_path}")
                return True
            except Exception as e:
                print(f"Error loading model: {e}")
                return False
        else:
            print(f"No existing model found at {model_path}")
            print("You'll need to collect data and train a model first.")
            return False