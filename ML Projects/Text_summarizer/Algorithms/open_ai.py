from openai import OpenAI
import tiktoken
from nltk.tokenize import sent_tokenize


def get_total_token(text, model='gpt-3.5-turbo'):
    encoding = tiktoken.encoding_for_model(model)
    return len(encoding.encode(text))


def open_ai_gpt(input_desc, open_ai_key, model='gpt-3.5-turbo'):
    client = OpenAI(api_key=open_ai_key)
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are an expert in providing summary of given text"},
            {"role": "user", "content": input_desc}
        ]
    )
    return response['choices'][0]['message']['content']


def open_ai_gpt_call(inputs, open_ai_key):
    count = 0
    desc, summ = '', ''
    last = False
    for sent in sent_tokenize(inputs):
        count_sent = get_total_token(sent)
        if count_sent + count > 4096:
            summ += ' ' + open_ai_gpt(desc, open_ai_key)
            desc = sent
            count = count_sent
            last = True
        else:
            desc += ' ' + sent
            count += count_sent
            last = False
    if last is False:
        summ += ' ' + open_ai_gpt(desc, open_ai_key)
    return summ
