from transformers import AutoTokenizer
from.ingest_data import get_data

model_nm = 't5-small'
tokenizer = AutoTokenizer.from_pretrained(model_nm)

def tokenize_data(x):
  model_inputs = tokenizer(
      x['document'],
      max_length = 512,
      padding=True,
      truncation=True
  )
  labels = tokenizer(
      x['summary'],
      max_length = 512,
      padding = True,
      truncation=True
  )
  model_inputs['labels'] = labels['input_ids']
  return model_inputs

def preprocess():
    dataset = get_data()
    tok_ds = dataset.map(tokenize_data, batched=True)
    return tok_ds