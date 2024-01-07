# Required modules
import os
from src.entity import ModelEvaluationConfig
import torch
from transformers import AutoModelForSequenceClassification
from sklearn.metrics import (roc_curve, roc_auc_score, accuracy_score, precision_score, recall_score, f1_score)
import matplotlib.pyplot as plt
class ModelEvaluator:
    def __init__(self, eval_dataloader, model_path, config: ModelEvaluationConfig):
        # Initialize the ModelTrainer class with paths to training and validation data and a configuration object
        self.evaluation_data = eval_dataloader
        self.model_path = model_path
        self.config = config

    def evaluate_model(self):
        # Instantiate a sequence classification model
        model = AutoModelForSequenceClassification.from_pretrained(self.model_path)

        # Set hardware for model training (CUDA if available, otherwise CPU)
        device = torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu")
        model.to(device)

        model.eval()
        all_predictions = []
        all_labels = []
        all_probs = []

        for batch in self.evaluation_data:
            batch = {k: v.to(device) for k, v in batch.items()}
            with torch.no_grad():
                outputs = model(**batch)

            logits = outputs.logits
            predictions = torch.argmax(logits, dim=-1)

            # Append predictions and labels for later evaluation
            all_predictions.extend(predictions.cpu().numpy())
            all_labels.extend(batch["labels"].cpu().numpy())
            all_probs.extend(torch.softmax(logits, dim=-1)[:, 1].cpu().numpy())  # Assuming binary classification

        # Ensure that all_labels and logits have the same length
        assert len(all_labels) == len(all_predictions), "Inconsistent number of samples"

        # Compute metrics
        accuracy = accuracy_score(all_labels, all_predictions)
        precision = precision_score(all_labels, all_predictions)
        recall = recall_score(all_labels, all_predictions)
        f1 = f1_score(all_labels, all_predictions)
        roc_auc = roc_auc_score(all_labels, all_probs)

        with open(self.config.evaluation_file, 'w') as f:
            f.write("-:Model's Evaluation Report:-")
            f.write(f"  \nAccuracy: {accuracy}")
            f.write(f"  \nPrecision: {precision}")
            f.write(f"  \nRecall: {recall}")
            f.write(f"  \nF1 Score: {f1}")

        # ROC Curve
        fpr, tpr, _ = roc_curve(all_labels, all_probs)
        # Plot ROC Curve
        plt.figure(figsize=(8, 8))
        plt.plot(fpr, tpr, color='darkorange', lw=2, label='ROC curve (area = {:.2f})'.format(roc_auc))
        plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
        plt.xlabel('False Positive Rate')
        plt.ylabel('True Positive Rate')
        plt.title('Receiver Operating Characteristic (ROC) Curve')
        plt.legend(loc="lower right")
        # Save the plot to local storage
        plt.savefig(os.path.join(self.config.root_dir,'roc_curve_plot.png'))

