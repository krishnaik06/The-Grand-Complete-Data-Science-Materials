import os, sys
from os.path import dirname as up

sys.path.append(os.path.abspath(os.path.join(up(__file__), os.pardir)))

from utils.common_libraries import *

# Loading Environment Variables
GOOGLE_AI_STUDIO = os.getenv("GOOGLE_AI_STUDIO")
GOOGLE_APPLICATION_CREDENTIALS = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
GEMINI_PRO = os.getenv("GEMINI_PRO", "gemini-pro")
GEMINI_PRO_VISION = os.getenv("GEMINI_PRO_VISION", "gemini-pro-vision")

# if __name__ == "__main__":
#     print(GEMINI_PRO)
