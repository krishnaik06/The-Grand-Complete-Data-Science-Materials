import torch
from transformers import (
    AutoTokenizer, 
    AutoModelForSequenceClassification
)
import torch.nn.functional as F
from src.utils.common import read_yaml
from src.constants import CONFIG_YAML_FILE


class PredictionPipeline:
    def __init__(self, text):
        # Load the tokenizer
        self.configuration = read_yaml(CONFIG_YAML_FILE)
        model_path = self.configuration.model_training.trained_model
        self.text = text
        self.tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")
        self.saved_model = AutoModelForSequenceClassification.from_pretrained(model_path)            


    def predict_label(self):
        tokenized_text = self.tokenizer(self.text, truncation=True, padding=True, return_tensors="pt")
        with torch.no_grad():
            logits = self.saved_model(**tokenized_text).logits
        # Assuming logits[:, 1] corresponds to the positive class
        predicted_label = torch.argmax(logits, dim=-1).item()
        # return the predicted label
        return predicted_label