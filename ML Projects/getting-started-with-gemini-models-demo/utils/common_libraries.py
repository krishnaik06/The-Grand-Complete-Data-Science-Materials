import os, sys
from os.path import dirname as up

sys.path.append(os.path.abspath(os.path.join(up(__file__), os.pardir)))

import json

from google.oauth2 import service_account  # importing auth using service_account

from vertexai.preview.generative_models import (
    GenerationConfig,
    GenerativeModel,
    Image,
    Part,
)

import google.generativeai as genai

import logging
import requests
from PIL import Image
from io import BytesIO
