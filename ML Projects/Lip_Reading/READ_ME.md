# Lip-Reading Model

This repository contains the code for a lip-reading model using TensorFlow. The model is designed to predict the text from lip movements in a given video.

## Table of Contents
- [Introduction](#introduction)
- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Dataset](#dataset)
- [Model Architecture](#model-architecture)
- [References](#references)
- [License](#license)
- [Links](#links)

## Introduction

Lip-reading involves understanding spoken language by observing lip movements. This project aims to build a lip-reading model using TensorFlow, capable of predicting text from lip movement videos.

## Features

- TensorFlow-based lip-reading model
- Dataset preprocessing utilities
- Training and evaluation scripts
- Pre-trained model weights

## Requirements

pip install -r requirements.txt

- Python 3.x
- TensorFlow
- OpenCV
- NumPy
- Matplotlib
- Imageio
- gdown

## Installation

Clone the repository to your local machine:

git clone https://github.com/Pradhyumnasg/Lip_Reading.git
cd lip-reading

##Usage:

Follow the steps below to use the lip-reading model:

1.Download the dataset and preprocess the data.
2.Define the model architecture in the code.
3.Train the model using the provided training script.
4.Evaluate the model on the test dataset.

##Datasets:

Provided the URL in the code cell if you run the cell it will download automatically

##Model Architecture:

The lip-reading model consists of a Convolutional Neural Network (CNN) followed by Long Short-Term Memory (LSTM) layers.

##References:

Jančurak, M., Lips, M., & Matas, J. (2015). LipNet: End-to-end speech recognition via a deep recurrent convolutional network. In Proceedings of the IEEE International Conference on Computer Vision (pp. 741-748). IEEE Computer Society.

License:

This project is licensed under the MIT License. Feel free to modify and distribute it as per the terms of the license.

Links:

Original Paper: https://arxiv.org/abs/1611.01599 
ASR Tutorial: https://keras.io/examples/audio/ctc_asr/