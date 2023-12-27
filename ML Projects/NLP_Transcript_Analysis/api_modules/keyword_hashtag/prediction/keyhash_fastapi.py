
# Importing fastapi modules
from fastapi import FastAPI, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

# Importing keyword modules
from utils_key import Item, final_processing, over_all_key, divide_chunks, NER_transcript, nounKey_nerKey_summary_chunk, clean_transcript, camel
from keybert import KeyBERT
from keyphrase_vectorizers import KeyphraseCountVectorizer
import nltk
nltk.data.path.append("./files/nltk_data")
from nltk.tokenize import sent_tokenize
import spacy

# Importing basic modules
import datetime
import logging
import sys

# Importing configuration modules
import configparser


logging.basicConfig(level = logging.INFO, filename ='keyhash.log',
                    filemode = 'w', format='%(asctime)s - %(levelname)s - %(message)s')


app = FastAPI()


# Module initialization
try:
    config = configparser.ConfigParser()
    config.read("./config.ini")
    model_name = config['KEYWORD_HASHTAG']['MODEL_NAME']
    nlp = spacy.load('en_core_web_md')
except Exception:
    logging.exception(sys.exc_info())
    raise HTTPException(status_code = 500, detail = 'PRELIMINARY INITIALIZATION FAILED')

try:
    kw_extractor = KeyBERT('./files')  # Place the files in the same folder
except Exception:
    logging.exception(sys.exc_info())
    raise HTTPException(status_code = 500, detail = 'MODEL INITIALIZATION FAILED')


# Prediction Endpoint
@app.post("/v1.0/prediction")
async def read_text(data: Item):

    if data.model == model_name:
        time = datetime.datetime.now()
        
        logging.info('Executing keyword module')
        summary_text = data.summary
        transcript_text = data.transcript

        # clean transcript
        transcript_text = clean_transcript(transcript_text)
        
        try:
            summary_line_list = sent_tokenize(summary_text)
        except Exception:
            logging.exception(sys.exc_info())
            raise HTTPException(status_code=500, detail='SENTENCE TOKENIZING ERROR')

        # Dividing into chunks    
        summary_line_chunks_list = divide_chunks(summary_line_list)
        summary_chunks_txt_list = [' '.join(i) for i in summary_line_chunks_list]

        try:
            keybert_diversity_phrases = []
            NER_Keywords = []
            noun_keywords = []
            for new_text in summary_chunks_txt_list:
               
                try:
                    keywords_n = kw_extractor.extract_keywords(new_text, vectorizer=KeyphraseCountVectorizer(pos_pattern='<N.*>'), use_mmr=True, diversity=1.0,
                                                                keyphrase_ngram_range=(1, 1), stop_words='english', top_n=50)
                    keywords_noun = [i for i in keywords_n if i[1] > 0.2]
                    for i, _ in keywords_noun:
                        keybert_diversity_phrases.append(i)
                except:
                    logging.info('No keywords extracted in this loop')


                try:
                    keywords2_nn = kw_extractor.extract_keywords(new_text, vectorizer=KeyphraseCountVectorizer(pos_pattern='<N.+>+<N.+>'), use_mmr=True, diversity=1.0,
                                                                    keyphrase_ngram_range=(2, 3), stop_words='english', top_n=50)
                    keywords_nnounn = [i for i in keywords2_nn if i[1] > 0.2]
                    for i, _ in keywords_nnounn:
                        keybert_diversity_phrases.append(i)
                except:
                    logging.info('No keywords extracted in this loop')

                # Extrating noun and NER from chunk
                noun_keywords, NER_Keywords = nounKey_nerKey_summary_chunk(new_text, noun_keywords, NER_Keywords)
                
        except Exception:
            logging.exception(sys.exc_info())
            raise HTTPException(status_code=500, detail='KEYWORD EXTRACTION ERROR')
        

        # Overall keywords
        over_all_keywords, ner_keywords = over_all_key(keybert_diversity_phrases, NER_Keywords, noun_keywords)

        # keywords from transcript
        over_all_keywords, ner_keywords_trans = NER_transcript(transcript_text, over_all_keywords, ner_keywords)

        # postprocessing final keywords
        over_all_keywords, noun_keywords_all, ner_keywords_all = final_processing(over_all_keywords, ner_keywords_trans, keybert_diversity_phrases)

        # Hashtag
        hashtag_output = camel(keybert_diversity_phrases)

        # returning the result
        try:
            content = {'Title' : data.title, 'NER Keywords' : ner_keywords_all, 
                       'Noun Keywords' : noun_keywords_all, 'Over_all_keywords' : over_all_keywords, 
                       'hashtag' : hashtag_output, 'timestamp' : time
                       }
            content = jsonable_encoder(content)
            return JSONResponse(content)
        
        except Exception:
            logging.exception(sys.exc_info())
            raise HTTPException(status_code=500, detail='ERROR IN RETURNING THE OUTPUT')
        
    else:
        raise HTTPException(status_code=404, detail='INVALID MODEL NAME - AVAILABLE MODEL : <all-mpnet-base-v2>')
