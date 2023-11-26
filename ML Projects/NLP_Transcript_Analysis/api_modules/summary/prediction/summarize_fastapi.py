
# Importing fastapi modules
from fastapi import FastAPI, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

# Importing summary modules
import torch
from transformers import pipeline
from utils_sum import preprocess_transcript, divide_chunks, Item, clean_transcript

# Importing basic modules
import datetime
import logging
import sys
import nltk
nltk.data.path.append("./files/nltk_data")

# Importing configuration modules
import configparser


# Logging configuration
logging.basicConfig(level = logging.INFO, filename ='summarize.log',
                    filemode = 'w', format='%(asctime)s - %(levelname)s - %(message)s')


app = FastAPI()


# Module initialization
try:
    logging.info('Module Initialization')

    # Configuration parser
    config = configparser.ConfigParser()
    config.read("./config_summarize.ini")
    model_name = config['SUMMARIZE']['MODEL_NAME']
    num_word = int(config['SUMMARIZE']['WORDS'])
except Exception:
    raise HTTPException(status_code = 500, detail = 'PRELIMINARY INITIALIZATION FAILED')


try:
    # Initialization of summary module
    num_of_gpus = torch.cuda.device_count()
    if num_of_gpus:
        summarizer = pipeline("summarization", model = "./files", device = 0)  # GPU enabled instance, Place the dependent files in same folder
    else:
        summarizer = pipeline("summarization", model = "./files")  # No GPU instance, Place the dependent files in same folder
except Exception:
    raise HTTPException(status_code = 500, detail = 'MODEL INITIALIZATION FAILED')


# Prediction Endpoint
@app.post("/v1.0/prediction")
async def read_text(data: Item):

    logging.info('Executing Prediction API')
    if data.model == model_name:
        time = datetime.datetime.now()

        logging.info('Performing transcript cleaning')
        cleaned_transcript = clean_transcript(data.transcript)

        logging.info('Preprocessing transcript')
        transcript_txt_lines = preprocess_transcript([cleaned_transcript], num_word_th = num_word)

        logging.info('Dividing the transcript into chunks')
        transcript_txt_chunks = divide_chunks(transcript_txt_lines)

        try:
            logging.info('Executing prediction module')
            final_sum = []
            for chunk_lines in transcript_txt_chunks:
                chunk_text = ' '.join(chunk_lines)
                MAX_LENGTH = len(chunk_text.split()) // 10 + 1  # 10%
                MIN_LENGTH = len(chunk_text.split()) // 50 + 1  # 2%
                chunk_sum = summarizer(chunk_text, max_length = MAX_LENGTH, min_length = MIN_LENGTH)
                final_sum.append(chunk_sum[0].get('summary_text'))
            summary_text = ' '.join(final_sum)
        except Exception:
            logging.exception(sys.exc_info())
            raise HTTPException(status_code=500, detail='ERROR IN EXTRACTING SUMMARY MODULE')


        try:
            logging.info('Returning the output')
            content = {'TITLE' : data.title, 'SUMMARY' : summary_text, 'TIMESTAMP' : time}
            content = jsonable_encoder(content)
            return JSONResponse(content)
        except Exception:
            logging.exception(sys.exc_info())
            raise HTTPException(status_code=500, detail='ERROR IN DISPLAYING THE OUTPUT')
        
    else:
        raise HTTPException(status_code=404, detail='INVALID MODEL NAME - AVAILABLE MODEL : <bart-large-cnn>')
