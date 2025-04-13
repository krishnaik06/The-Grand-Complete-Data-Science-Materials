
# Suicide and Depression Analysis using NLP

This project is an NLP-based suicide detection model that classifies text content into either "suicide" or "not suicide" categories. By analyzing the content of posts, it can provide insights into whether the text indicates a risk of suicidal ideation, supporting mental health professionals and platforms in identifying and addressing at-risk content.

# Table of Contents
<ul>
  <li>Project Overview</li>
  <li>Key Features</li>
  <li>Installation</li>
  <li>Usage</li>
  <li><a href="https://www.kaggle.com/datasets/nikhileswarkomati/suicide-watch">Data Set</a>
  <li>Methodology</li>
  <li>Results</li>
  <li>Contributing</li>
  <li>License</li>
</ul>

# Project Overview
Given the rising concerns about mental health in online spaces, this project leverages Natural Language Processing (NLP) to detect signs of suicidal ideation within written content. By classifying text into "suicide" or "not suicide" categories, the model aims to assist in early detection and intervention efforts for at-risk individuals.

# Key Features
<ul>
  <li>Suicide Detection: Automatically classifies posts based on the likelihood of containing suicide-related language.</li>
  <li>Text Analysis: Uses NLP preprocessing to analyze linguistic features commonly found in high-risk content.</li>
  <li>Real-Time Prediction: Allows users to input text and receive an instant classification.</li>
  <li>Model Accuracy: Trained on suicide-related datasets to ensure reliable and sensitive identification.</li>
</ul>

# Installation

1. Clone the repository:
  git clone https://github.com/arnabdatta03/Suicide-Depression-Analysis.git

 2. Install the required dependencies:
   "pip install -r requirements.txt"

# Usage
1. Load the Model: Use the pre-trained model available in the repository by running load_model.py.
2. Enter Text Content: Input the content you want to analyze.
3. View Results: The model will classify the input as either "suicide" or "not suicide."

# Model Training and Methodology
1. Data Preprocessing: The model preprocesses text by cleaning, tokenizing, and removing stop words.
2. Feature Engineering: NLP techniques like TF-IDF and word embeddings are used to capture context.
3. Model Training: Trained on suicide-related data with a binary classification approach using algorithms like logistic regression or LSTM for deep learning.

<b>Remind it that we have download a pickle file to fast the training and testing process for our model our pickle file link is <a href="https://www.kaggle.com/datasets/authman/pickled-glove840b300d-for-10sec-loading">Pickle File Zip</a>download the zip file and open and connect to your model glove.840B.300d.pkl this file and it enhance your model running time without it the model can be nead time 4 to 5 days for train okay you need to create a dynamic routing for add your file because "Google Colab" does not support this big file its size around 2.6gb so first you need to create a dynamic routing the code is below</b> 

 <p>1. Mount Google Drive</p>
<p> import pickle</p>
<p>from google.colab import drive</p>
<p>drive.mount('/content/drive')</p>
<p>with open('/content/drive/path where file upload/glove.840B.300d.pkl', 'rb') as fp:</p>
<p>glove_embedding = pickle.load(fp)</p>

<b>next completing dynamic routing you have to download your model tokenizer.pkl and also model.h5 file into and other dataset also your glove.840B.300d.pkl file in same dir and others required packages and then the model is ready to use</b>

# Model Run CMD
Open Vscode terminal in which dir your all file and write "streamlit run App.py"

# Results
The model achieves accuracy in distinguishing posts with suicidal intent. See the results folder for performance metrics, including accuracy, precision, and recall.


# Contributing
Contributions to improve accuracy and expand dataset diversity are welcome. Please open an issue or submit a pull request for review.

# License
This project is licensed under the BSD 3-Clause "New" or "Revised" <a href="https://github.com/arnabdatta03/Suicide-Depression-Analysis/blob/main/LICENSE">LICENSE</a> - see the LICENSE file for details.



