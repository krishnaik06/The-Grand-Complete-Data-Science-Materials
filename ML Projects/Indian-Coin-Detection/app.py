import streamlit as st
import os
import cv2
from PIL import Image
from Indian_Coin_Detection.pipeline.predict import PredictionPipeline

import subprocess

def train_model():
    try:
        subprocess.run(["dvc", "repro"], check=True)
        st.write("Training successfully completed")
    except subprocess.CalledProcessError as e:
        st.error(f"Error running DVC repro: {e}")


def main():
    st.title('Indian Coin Detection')

    st.write("Click on the train button to train the model")
    if st.button("Train Model",key="train_button"):
        train_model()

    
    threshold = st.sidebar.slider('Confidence', min_value=0.0, max_value=1.0, value=0.65)
    
    list_of_models = ['temporary-model', 'yolo-nano', 'yolo-small', 'yolo-medium']
    try:
        model_type = st.sidebar.multiselect('Select The Custom Classes', 
                                            list_of_models, default=['temporary-model'])[0]
    except IndexError:
        model_type = None
        st.write("Please Choose a Model to Predict")
    
    image_filename = handle_image_upload()
    
    if image_filename is not None:
        st.write("Click on the predict button to predict the model")
        if st.button("Predict",key="prediction_button"):
            prediction, resized_output_img = perform_detection(image_filename, model_type, threshold)
            display_prediction(prediction, resized_output_img)
    else:
        st.sidebar.write("Please upload an image before predicting.")

def handle_image_upload():
    upload_folder = "uploads"
    os.makedirs(upload_folder, exist_ok=True)
    image_filename = None
    uploaded_image = st.file_uploader("Upload an image", type=["jpg", "png", "jpeg"])
    
    if uploaded_image is not None:
        image_filename = os.path.join(upload_folder, uploaded_image.name)
        with open(image_filename, "wb") as f:
            f.write(uploaded_image.read())

        img = cv2.imread(image_filename,cv2.IMREAD_UNCHANGED)
        original_img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

        # Display the resized uploaded image
        st.image(original_img, caption='Uploaded Image', use_column_width=True)
    
    return image_filename

def perform_detection(image_filename, model_type, threshold):
    img = cv2.imread(image_filename, cv2.IMREAD_UNCHANGED)
    original_img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    
    detection = PredictionPipeline(image_filename, model_type=model_type, threshold=threshold)
    prediction, resized_output_img = detection.predict()
    resized_output_img = cv2.cvtColor(resized_output_img, cv2.COLOR_RGB2BGR)
    
    return prediction, resized_output_img

def display_prediction(prediction, resized_output_img):
    st.sidebar.header("Prediction")
    st.sidebar.subheader("Prediction Output")
    st.sidebar.write(prediction)
    
    st.sidebar.subheader("Resized Output Image")
    st.sidebar.image(Image.fromarray(resized_output_img), caption='Resized Output Image', use_column_width=True)

if __name__ == "__main__":
    main()
