from transformers import pipeline
from transformers import AutoTokenizer
from nltk.tokenize import sent_tokenize


def count_token(inputs):
    tokenize = AutoTokenizer.from_pretrained('facebook/bart-large-cnn')
    return len(tokenize.encode(inputs))


def abstraction_call(inputs):
    count = 0
    desc, summ = '', ''
    last = False
    for sent in sent_tokenize(inputs):
        count_sent = count_token(sent)
        if count_sent + count > 1024:
            summ += ' ' + abstraction(desc)
            desc = sent
            count = count_sent
            last = True
        else:
            desc += ' ' + sent
            count += count_sent
            last = False
    if last is False:
        summ += ' ' + abstraction(desc)
    return summ


def abstraction(text):
    max_length = count_token(text)
    pipe = pipeline("summarization", model="facebook/bart-large-cnn", min_length=1, max_length=max_length)
    summarized_text = pipe(text)
    return summarized_text[0]['summary_text']

