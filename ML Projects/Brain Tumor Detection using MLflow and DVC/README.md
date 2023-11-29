## About Dataset

## What is a brain tumor?
A brain tumor is a collection, or mass, of abnormal cells in your brain. Your skull, which encloses your brain, is very rigid. Any growth inside such a restricted space can cause problems. Brain tumors can be cancerous (malignant) or noncancerous (benign). When benign or malignant tumors grow, they can cause the pressure inside your skull to increase. This can cause brain damage, and it can be life-threatening.

## The importance of the subject:
Early detection and classification of brain tumors is an important research domain in the field of medical imaging and accordingly helps in selecting the most convenient treatment method to save patients life therefore

## Methods:
The application of deep learning approaches in context to improve health diagnosis is providing impactful solutions. According to the World Health Organization (WHO), proper brain tumor diagnosis involves detection, brain tumor location identification, and classification of the tumor on the basis of malignancy, grade, and type. This experimental work in the diagnosis of brain tumors using Magnetic Resonance Imaging (MRI) involves detecting the tumor, classifying the tumor in terms of grade, type, and identification of tumor location. This method has experimented in terms of utilizing one model for classifying brain MRI on different classification tasks rather than an individual model for each classification task. The Convolutional Neural Network (CNN) based multi-task classification is equipped for the classification and detection of tumors. The identification of brain tumor location is also done using a CNN-based model by segmenting the brain tumor.

## Dataset Description:
This dataset contains 7023 images of human brain MRI images which are classified into 4 classes: glioma - meningioma - no tumor and pituitary.

## Webapp Demo:
[brain tumor.webm](https://github.com/gbiamgaurav/Brain-Tumor-Detection-using-MLflow-DVC/assets/81230208/acb08ac1-5227-44e9-a5c6-e3d7de6f9f50)

[Checkout the Webapp here](https://brain-tumor-detection-using-mlflow-dvc-792mqwjfhxn9zmrmg9yjrm.streamlit.app/)


## MFLOW commands to run

``` bash

export `MLFLOW_TRACKING_URI`

export `MLFLOW_TRACKING_USERNAME`

export `MLFLOW_TRACKING_PASSWORD`

```

## DVC commands to run 

``` bash

`dvc init`

`dvc repro`

`dvc dag`

```

## Tech Stack used in this Project:

Python

Streamlit

Pretrained_model = RESNET50 (https://keras.io/api/applications/resnet/#resnet50-function)

MLFLOW (https://mlflow.org/)

DVC (https://dvc.org/)

DagsHub (https://dagshub.com/gbiamgaurav/Brain-Tumor-Detection-using-MLflow-DVC)


