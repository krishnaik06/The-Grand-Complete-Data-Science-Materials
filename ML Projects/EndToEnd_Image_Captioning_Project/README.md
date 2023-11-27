# Image Captioning Project

This project implements an end-to-end Image Captioning system using VGG16, CNN, and LSTM. It generates descriptive captions for input images by combining the power of convolutional neural networks (CNN) for image feature extraction and long short-term memory (LSTM) networks for language modeling.

## Overview

The Image Captioning system follows the following steps:

1. Preprocessing: The input images are preprocessed to extract features using the VGG16 model. These features serve as the visual representation of the images.

2. Text Preprocessing: The captions associated with the images are preprocessed by tokenizing them into words and creating a vocabulary of unique words.

3. Model Architecture: The architecture consists of a CNN for image feature extraction and an LSTM network for generating captions. The CNN encodes the image features, while the LSTM decodes the features to generate descriptive captions.

4. Training: The model is trained using a dataset of images and corresponding captions. The image features are extracted using the pre-trained VGG16 model, and the captions are processed and fed into the LSTM network.

5. Caption Generation: Given a new input image, the trained model generates captions by first extracting the image features using the CNN and then using the LSTM to generate a sequence of words based on the image features.

## Dependencies

- Python 3.x
- TensorFlow
- Keras
- NumPy
- NLTK

## Installation

1. Clone the repository:

### app link(not fitted perfectly due to limited resources so that there would be chances of wrong predictions
https://sunilgiri7-end-to-end-image-screening-project-streamlit-z7uirv.streamlit.app/

