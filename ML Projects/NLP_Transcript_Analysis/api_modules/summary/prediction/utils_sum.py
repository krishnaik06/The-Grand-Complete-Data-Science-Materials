
# Importing function dependent packages
from nltk.tokenize import sent_tokenize
from pydantic import BaseModel, constr
import re

# Importing basic libraries
import configparser

# Importing fastapi libraries
from fastapi import HTTPException


# Configuration parser
config = configparser.ConfigParser()
config.read("./config_summarize.ini")
chunk_size = int(config['SUMMARIZE']['CHUNK_SIZE'])


# Prediction module input scheme
class Item(BaseModel):
    title: str
    transcript: constr(min_length = 30)
    model: str


# transcript cleaning - removing timestamp and newline character
def clean_transcript(transcript_text):
    try:
        regex = r"\d+.\d+-\d+.\d+"
        removed_timestamp = re.sub(regex, "", transcript_text)
        cleaned_text = removed_timestamp.replace("\n", "")
        cleaned_text = cleaned_text.replace("\\", "")
        return cleaned_text
    except Exception:
        raise HTTPException(status_code = 500, detail = 'TRANSCRIPT CLEANING ERROR')


# Tokenising the transcript
def preprocess_transcript(transcript_text, num_word_th=0):
    try:
        output_list = []
        assert(type(transcript_text)==list)
        for line in transcript_text:
            line_list = sent_tokenize(line)
            for l in line_list:
                if len(l) > num_word_th:
                    output_list.append(l)
        return output_list
    except Exception:
        raise HTTPException(status_code = 500, detail = 'PREPROCESSING ERROR')


# Creating transcript chunks 
def divide_chunks(l, n=chunk_size):
    try:
        for i in range(0, len(l), n):
            yield l[i:i + n]
    except Exception:
        raise HTTPException(status_code = 500, detail = 'DIVIDING CHUNKS ERROR')
