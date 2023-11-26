
# Importing fastapi modules
from fastapi import FastAPI, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

# Importing prediction dependent modules
from utils_topic import Item, get_similarities_model1
from sentence_transformers import SentenceTransformer

# Importing basic modules
import datetime
import logging
import sys
import numpy as np
import ast

# Importing configuration modules
import configparser

# logging file location and format
logging.basicConfig(level = logging.INFO, filename ='topic.log',
                    filemode = 'w', format='%(asctime)s - %(levelname)s - %(message)s')


app = FastAPI()


# Module initialization
try:
    logging.info('Initialization')
    # Configuration Parser
    config = configparser.ConfigParser()
    config.read("./config_topic.ini")
    model_name = config['TOPIC']['MODEL_NAME']
    candidate_labels= ast.literal_eval(config['TOPIC']['TOPIC_MAIN'])
except Exception:
    logging.exception(sys.exc_info())
    raise HTTPException(status_code = 500, detail = 'PRELIMINARY INITIALIZATION FAILED')


try:
    # Topic Module 
    logging.info('transformer module initialization')
    model1 = SentenceTransformer('./files') # Place files in the same folder
except Exception:
    logging.exception(sys.exc_info())
    raise HTTPException(status_code = 500, detail = 'MODEL INITIALIZATION FAILED')


try:
    # Topic Embeddings
    logging.info('Getting embeddings for topics')
    embedded_topic = []
    for i in range(len(candidate_labels)):
        embed = model1.encode(candidate_labels[i])
        embedded_topic.append(embed)
except Exception:
    logging.exception(sys.exc_info())
    raise HTTPException(status_code = 500, detail = 'TOPIC EMBEDDING FAILED')


# Prediction Endpoint
@app.post("/v1.0/prediction")
async def read_text(data: Item):

    logging.info('Prediction endpoint execution')
    if data.model == model_name:
        time = datetime.datetime.now()
        logging.info('Executing prediction module')
        global embedded_topic

        try:
            logging.info('Getting embeddings for summary')
            embedded_text = []
            embed = model1.encode(data.summary)
            embedded_text.append(embed)
            embedded_text = np.array(embedded_text)
        except Exception:
            logging.exception(sys.exc_info())
            raise HTTPException(status_code = 500, detail = 'SUMMARY EMBEDDING FAILED')
        

        logging.info('Getting similarity score for topics and summary')
        score = get_similarities_model1(embedded_text, embedded_topic)
        score = [round(x, 3) for x in score]
        topic_score_list = sorted(zip(candidate_labels, score), key=lambda x: x[1], reverse=True)

        try:
            # returning the result
            logging.info('returning the result')
            content = {'TITLE' : data.title,'TOPICS' : dict(topic_score_list), 'TIMESTAMP' : time
                        }
            content = jsonable_encoder(content)
            return JSONResponse(content)
        
        except Exception:
            logging.exception(sys.exc_info())
            raise HTTPException(status_code=500, detail='ERROR IN RETURNING THE OUTPUT')
        
    else:
        logging.exception(sys.exc_info())
        raise HTTPException(status_code=404, detail='INVALID MODEL NAME - AVAILABLE MODEL : <all-mpnet-base-v2>')
