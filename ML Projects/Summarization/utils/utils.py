from transformers import AutoTokenizer

model_nm = 't5-base'
device = 'cuda'

def tokenize_for_inference(text):
    tokenizer = AutoTokenizer.from_pretrained(model_nm)
    model_inputs = tokenizer.encode(
      text,
      max_length = 512,
      padding=True,
      truncation=True,
        return_tensors='pt'
    )
    return model_inputs.to(device)
