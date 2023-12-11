from utils.utils import tokenize_for_inference
from transformers import AutoTokenizer

def infer_model(trainer):
    tokenizer = AutoTokenizer.from_pretrained('t5-base')
    text = input("Enter the text you want to summarize: ")
    tokenized = tokenize_for_inference(text)
    generated = trainer.model.generate(tokenized, max_length=256)
    
    # Convert the generated output back to text
    summary = tokenizer.decode(generated.squeeze(), skip_special_tokens=True)
    print(summary)
    return summary
