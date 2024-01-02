import numpy as np
from rouge import Rouge


def rouge_eval(prediction, reference):
    rouge_metric = Rouge()
    score = rouge_metric.get_scores(prediction, reference, avg=True)
    return score

