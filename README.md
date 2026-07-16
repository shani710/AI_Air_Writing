# 🤖 AI Air Writing Recognition System

## 📌 Overview

AI Air Writing is a real-time Human-Computer Interaction (HCI) system that enables users to write letters and words in the air using natural hand gestures. Instead of using a keyboard, mouse, or touchscreen, users can simply move their hand in front of a webcam to draw characters, which are then recognized using Deep Learning.

This project combines **Computer Vision**, **Hand Tracking**, and **Machine Learning** to create an interactive air-writing experience.

---

## 🚀 Features

* ✋ Real-time hand tracking using MediaPipe
* 🖊️ Pinch gesture detection for pen-up and pen-down functionality
* 🎥 Webcam-based interaction (no additional hardware required)
* 🧠 Character recognition using a Convolutional Neural Network (CNN)
* ⚡ Real-time drawing and prediction
* 📊 Lightweight and easy-to-train model

---

## 🔍 How It Works

1. **Hand Detection**

   * MediaPipe detects and tracks 21 hand landmarks in real time.

2. **Gesture Recognition**

   * A pinch gesture between fingers activates the writing mode.

3. **Air Drawing**

   * The fingertip trajectory is captured and rendered as a virtual drawing canvas.

4. **Character Recognition**

   * The drawn character is processed and passed to a CNN model trained using TensorFlow/Keras.

5. **Prediction Output**

   * The model predicts the most likely character and displays the result.

---

## 🛠️ Technology Stack

| Technology         | Purpose                          |
| ------------------ | -------------------------------- |
| Python             | Core Programming Language        |
| OpenCV             | Image Processing & Visualization |
| MediaPipe          | Real-Time Hand Tracking          |
| TensorFlow / Keras | Deep Learning Model Development  |
| Scikit-Learn       | Data Preprocessing & Evaluation  |
| NumPy              | Numerical Computations           |

---

## 📊 Model Performance

### Current Dataset

* Characters Supported: **A, N, O**
* Training Samples: **50 samples per class**
* Model Type: **Convolutional Neural Network (CNN)**

### Results

* Recognition Accuracy: **~70%**
* Real-time prediction capability
* Successfully distinguishes between supported characters

> Note: Accuracy is expected to improve with a larger and more diverse dataset.

---

## 📁 Project Structure

```bash
AI_Air_Writing/
│
├── dataset/                 # Training images
├── models/                  # Trained CNN models
├── data_collection.py       # Dataset generation
├── train_model.py           # Model training script
├── predict.py              # Real-time prediction
├── utils/                  # Helper functions
├── requirements.txt
└── README.md
```

---

## ⚙️ Installation

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/AI_Air_Writing.git
cd AI_Air_Writing
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the Application

```bash
python src main.py
```

---

## 🎯 Learning Outcomes

During this project, I gained hands-on experience with:

* Real-time Computer Vision applications
* Hand landmark detection and tracking
* Gesture-based Human-Computer Interaction
* Data collection and preprocessing techniques
* Training CNN models on custom datasets
* Building complete end-to-end Machine Learning pipelines
* Optimizing models for limited datasets

---

## 🔮 Future Improvements

* Support for the complete English alphabet (A–Z)
* Word and sentence recognition
* Improved gesture detection
* Larger training datasets for higher accuracy
* Real-time language modeling
* Web and mobile deployment
* Transformer-based character recognition

---

## 📸 Demo

Add screenshots, GIFs, or demo videos here to showcase the system in action.
🎥 [Watch Demo Video](./air_writing_project/air%20writing.mp4).


---
### Hand Tracking

![Hand Tracking](air_writing_project/air.png)
## 🤝 Contributing

Contributions, suggestions, and improvements are welcome. Feel free to fork the repository and submit a pull request.

---

## 📜 License

This project is licensed under the MIT License.

---

## 👨‍💻 Author

**Ghulam Abbas**

AI & Computer Vision Enthusiast | Python Developer | Machine Learning Practitioner

If you found this project useful, please ⭐ the repository and share your feedback.
