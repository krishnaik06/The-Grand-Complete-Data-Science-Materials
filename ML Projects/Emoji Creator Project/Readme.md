 Emoji Generator Based on Facial Emotions

## Introduction

This project is a **GUI-based application** built using **Tkinter** that generates emojis based on facial emotions. It detects the user's facial expressions in real time using the webcam, predicts emotions like happiness, sadness, anger, etc., and displays an appropriate emoji corresponding to the detected emotion.

### Key Features:
- **Real-time Facial Emotion Detection**: Uses **OpenCV** to capture video input from the webcam.
- **Emotion Prediction**: Employs a **deep learning model** built with **TensorFlow** and **Keras** to classify emotions.
- **Emoji Generation**: The app displays the corresponding emoji based on the detected facial expression.
- **GUI**: Built using **Tkinter** to provide a simple and user-friendly interface.

## Project Overview

### Steps:
1. **Face Detection**: Detect the face from the video feed using OpenCV and **Haar Cascade Classifier** (`haarcascade_frontalface_default.xml`).
2. **Emotion Detection**: Preprocess the face and feed it into the pre-trained deep learning model to classify the emotion.
3. **Emoji Display**: Display an emoji that represents the detected emotion.

## Directory Structure

```
Emoji-Generator/
│
├── Model/
│   ├── emotion_model.h5                   # Pre-trained Keras model for emotion detection
│   └── haarcascade_frontalface_default.xml # Haar cascade for face detection
│
├── emojis/
│   ├── happy.png                           # Emoji for happy emotion
│   ├── sad.png                             # Emoji for sad emotion
│   ├── angry.png                           # Emoji for angry emotion
│   └── ...                                 # Other emojis for various emotions
│
├── app.py                                  # Main Python script for running the Tkinter app
├── README.md                               # Project documentation
├── requirements.txt                        # List of required Python libraries
└── utils.py                                # Helper functions for preprocessing and detection
```

## Setup Instructions

### Step 1: Create a Virtual Environment

Before you run the project, create a virtual environment to isolate the dependencies.

```bash
# For Windows
python -m venv venv
venv\Scripts\activate

# For macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 2: Install the Required Dependencies

The necessary Python packages for this project are listed in `requirements.txt`. Install them by running:

```bash
pip install -r requirements.txt
```

Packages you will need:
- **TensorFlow**
- **Keras**
- **OpenCV (cv2)**
- **Tkinter**
- **Numpy**

### Step 3: Download Pretrained Model

The pre-trained emotion detection model (`emotion_model.h5`) is already included in the `Model/` directory. If you need to retrain the model or want to explore further, ensure that you have TensorFlow/Keras set up for training.

### Step 4: Running the GUI Application

To start the GUI application, run the `app.py` file:

```bash
python app.py
```

This will launch the GUI interface, where you can start detecting emotions in real-time using your webcam. The corresponding emoji will be displayed based on the detected emotion.

## Model Overview

The emotion detection model is a **Convolutional Neural Network (CNN)** trained to classify facial expressions. The model was built using **TensorFlow** and **Keras**, and the following emotions are supported:
- Happy
- Sad
- Angry
- Surprised
- Neutral

### Model Architecture:
- **Convolutional Layers**: Extract features from the input face image.
- **Max Pooling Layers**: Downsample the feature maps.
- **Fully Connected Layers**: Classify the emotions based on the extracted features.
- **Softmax Activation**: Outputs probabilities for each emotion class.

## Data Preprocessing

The facial images captured from the webcam are preprocessed before feeding into the model:
- **Grayscale Conversion**: The images are converted to grayscale to reduce complexity.
- **Face Detection**: OpenCV’s Haar Cascade Classifier is used to detect the face from the video frame.
- **Resizing**: The detected face is resized to the dimensions required by the model (48x48 pixels).
- **Normalization**: The pixel values are normalized to [0, 1] for better model performance.

## Emoji Display

Once the emotion is detected, the corresponding emoji is displayed on the GUI. The emojis are stored in the `emojis/` folder and loaded into the app when an emotion is detected.

Supported emojis:
- Happy (`happy.png`)
- Sad (`sad.png`)
- Angry (`angry.png`)
- Surprised (`surprised.png`)
- Neutral (`neutral.png`)

## Example Usage

### Step 1: Launch the App
Once you run `app.py`, a window will open with a live video feed from your webcam.

### Step 2: Start Detection
Click the **Start** button, and the system will start detecting your facial emotions in real-time.

### Step 3: View Emoji
As soon as your emotion is detected, the corresponding emoji (happy, sad, angry, etc.) will appear in the GUI.

### Sample Interface:

- Webcam feed on the left side.
- Emoji based on detected emotion on the right side.

## Conclusion

This project demonstrates how we can integrate **deep learning models** with **GUI-based applications** using Tkinter. By leveraging real-time facial emotion detection, this application offers a fun and interactive way to generate emojis. With further improvements, this can be expanded for more practical use cases such as emotional AI, personalized responses, or interactive systems.

---
