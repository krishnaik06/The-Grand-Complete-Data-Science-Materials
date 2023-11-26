
# Importing fastapi modules
from fastapi import FastAPI, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

# Importing prediction dependent modules
from utils_zero import Item_zeroshot
from transformers import pipeline
import torch

# Importing basic modules
import datetime
import logging
import sys
import ast

# Importing configuration modules
import configparser

# logging file location and format
logging.basicConfig(level = logging.INFO, filename = './topic_zeroshot.log',
                    filemode = 'w', format='%(asctime)s - %(levelname)s - %(message)s')


app = FastAPI()


# Module initialization
try:

    logging.info('Initialization')

    # Configuration Parser
    config = configparser.ConfigParser()
    config.read("./config_zero.ini")
    model_name = config['TOPIC_ZERO']['ZERO_NAME']
    candidate_labels = ast.literal_eval(config['TOPIC_ZERO']['TOPIC_MAIN'])

except Exception:
    logging.exception(sys.exc_info())
    raise HTTPException(status_code = 500, detail = 'PRELIMINARY INITIALIZATION FAILED')


try:
    
    # Zeroshot Module 
    logging.info('Pipeline initialization')

    num_of_gpus = torch.cuda.device_count()
    
    if num_of_gpus:
        model = pipeline('zero-shot-classification', model = './files', device = 0)
    else:
        model = pipeline('zero-shot-classification', model = './files')

except Exception:
    logging.exception(sys.exc_info())
    raise HTTPException(status_code = 500, detail = 'MODEL INITIALIZATION FAILED')


# Prediction Endpoint
@app.post("/v1.0/prediction")
async def read_text(data: Item_zeroshot):

    logging.info('Prediction endpoint execution')
    if data.model == model_name:
        time = datetime.datetime.now()

        if data.labels is not None:
            prediction_labels = data.labels
        else:
            prediction_labels = candidate_labels

        try:
            logging.info('Executing zeroshot module')
            result = model(data.summary, prediction_labels)
        except Exception:
            logging.exception(sys.exc_info())
            raise HTTPException(status_code=500, detail='ERROR IN ZEROSHOT MODULE')

        try:
            sorted_score = sorted(zip(result['labels'], result['scores']), key = lambda x : x[1], reverse = True)
            content = {'RESULT' : sorted_score, 'TIMESTAMP' : time}
            content = jsonable_encoder(content)
            return JSONResponse(content)
        except Exception:
            logging.exception(sys.exc_info())
            raise HTTPException(status_code=500, detail='ERROR IN RETURNING THE OUTPUT')

    else:
        logging.exception(sys.exc_info())
        raise HTTPException(status_code=404, detail='INVALID MODEL NAME - AVAILABLE MODEL : <bart-large-mnli>')
