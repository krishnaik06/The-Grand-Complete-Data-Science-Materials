from flask import Flask
from video_summarizer.logger import logging
from video_summarizer.exception import CustomException
import os, sys

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    try:
        raise Exception("We are testing our custom exception file") # error
    except Exception as e:
        summary = CustomException(e, sys)
        logging.info(summary.error_message)
        logging.info("We are testing logging module")
        
        return "hello World"

if __name__=="__main__":
    app.run(debug=True)