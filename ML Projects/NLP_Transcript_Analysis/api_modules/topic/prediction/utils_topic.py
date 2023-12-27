

# Importing dependent modules
import numpy as np
import math
from pydantic import BaseModel, constr, conlist
from scipy.special import softmax

# Importing fastapi libraries
from fastapi import HTTPException

# Prediction endpoint input scheme
class Item(BaseModel):
    title: str
    summary: constr(min_length=20)
    model: str

# calculate similarity score - v1 to v2: (v1 dot v2)/{||v1||*||v2||)
def cosine_similarity(v1, v2):
    try:
        sumxx, sumxy, sumyy = 0, 0, 0
        for i in range(len(v1)):
            x = v1[i];
            y = v2[i]
            sumxx += x * x
            sumyy += y * y
            sumxy += x * y
        return sumxy / math.sqrt(sumxx * sumyy)
    except Exception:
        raise HTTPException(status_code = 500, detail = 'COSINE SIMILARITY CALCULATION FAILED')


# Getting similarity score for text and prediction
def get_similarities_model1(embed_text, embed_topic):
    try:
        SCALE_SCORE = 20
        scored = []
        for i in range(len(embed_topic)):
            for j in range(len(embed_text)):
                score = np.round(cosine_similarity((embed_text[j]), (embed_topic[i])), 3)
                scored.append(score * SCALE_SCORE)
        scored = softmax(np.array(scored))
        return scored
    except Exception:
        raise HTTPException(status_code = 500, detail = 'RESULT SCORING FAILED')


