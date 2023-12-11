import os
import sys
import numpy as np
import nltk
from transformers import AutoModelForSeq2SeqLM, BartTokenizer, DataCollatorForSeq2Seq, Seq2SeqTrainingArguments, Seq2SeqTrainer
from evaluate import load
from datasets import load_from_disk
from video_summarizer.logger import logger
from video_summarizer.exception import CustomException

class ModelTrainer:
    def __init__(self, model_checkpoint, processed_dataset_folder, trainer_artifact_dir):
        self.model_checkpoint = model_checkpoint
        self.dataset_folder = processed_dataset_folder
        self.trainer_artifact_folder = trainer_artifact_dir
        self.model = None
        self.tokenizer = None
        self.tokenized_train_dataset = None
        self.tokenized_test_dataset = None
        self.data_collator = None
        self.metric = load("rouge")

    def initialize_model_tokenizer(self):
        try:
            logger.info("Initializing model and tokenizer for training...")

            self.model = AutoModelForSeq2SeqLM.from_pretrained(self.model_checkpoint)
            self.tokenizer = BartTokenizer.from_pretrained(self.model_checkpoint)

        except Exception as e:
            logger.error(f"Exception occurred while initializing model and tokenizer: {e}")
            raise CustomException(e, sys)
        

    def load_tokenized_datasets(self):
        try:
            logger.info("Loading data from data processing artifacts for training...")

            self.tokenized_train_dataset = load_from_disk(os.path.join(self.dataset_folder, "proc_train"))
            self.tokenized_test_dataset = load_from_disk(os.path.join(self.dataset_folder, "proc_test"))
        except Exception as e:
            logger.error(f"Exception occurred while loading tokenized datasets: {e}")
            raise CustomException(e, sys)
        
    def initialize_collator(self):
        try:
            self.data_collator = DataCollatorForSeq2Seq(self.tokenizer, model=self.model)
        except Exception as e:
            logger.error(f"Exception occurred while initializing data collator: {e}")
            raise CustomException(e, sys)

    def setup_trainer(self):
        try:
            logger.info("setting up model trainer class...")
            batch_size = 64
            model_name = self.model_checkpoint.split("/")[-1]
            args = Seq2SeqTrainingArguments(
                f"{model_name}-finetuned",
                evaluation_strategy="epoch",
                learning_rate=2e-5,
                per_device_train_batch_size=batch_size,
                per_device_eval_batch_size=batch_size,
                weight_decay=0.01,
                save_total_limit=3,
                num_train_epochs=1,
                predict_with_generate=True,
                #fp16=True, It will work in CUDA ONLY
                fp16=False,
                push_to_hub=False,
            )
            self.trainer = Seq2SeqTrainer(
                model=self.model,
                args=args,
                train_dataset=self.tokenized_train_dataset,
                eval_dataset=self.tokenized_test_dataset,
                data_collator=self.data_collator,
                tokenizer=self.tokenizer,
                compute_metrics=self.compute_metrics
            )
        except Exception as e:
            logger.error(f"Exception occurred while setting up trainer: {e}")
            raise CustomException(e, sys)

    def compute_metrics(self, eval_pred):
        try:
            predictions, labels = eval_pred
            decoded_preds = self.tokenizer.batch_decode(predictions, skip_special_tokens=True)
            # Replace -100 in the labels as we can't decode them.
            labels = np.where(labels != -100, labels, self.tokenizer.pad_token_id)
            decoded_labels = self.tokenizer.batch_decode(labels, skip_special_tokens=True)

# a,b,c , d,e 
            # Rouge expects a newline after each sentence
            decoded_preds = ["\n".join(nltk.sent_tokenize(pred.strip())) for pred in decoded_preds]
            decoded_labels = ["\n".join(nltk.sent_tokenize(label.strip())) for label in decoded_labels]

            result = self.metric.compute(predictions=decoded_preds, references=decoded_labels, use_stemmer=True, 
                                         use_aggregator=True)
            result = {key: value * 100 for key, value in result.items()}

            prediction_lens = [np.count_nonzero(pred != self.tokenizer.pad_token_id) for pred in predictions]
            result["gen_len"] = np.mean(prediction_lens)

            return {k: round(v, 4) for k, v in result.items()}
        except Exception as e:
            logger.error(f"Exception occurred while computing metrics: {e}")
            raise CustomException(e, sys)
        
    def train_model(self):
        try:
            self.initialize_model_tokenizer()
            self.load_tokenized_datasets()
            self.initialize_collator()
            self.setup_trainer()

            self.trainer.train()
        except Exception as e:
            logger.error(f"Exception occurred during model training: {e}")
            raise CustomException(e, sys)
        
    def train(self):
        try:
            self.train_model()
            self.trainer.save_model(self.trainer_artifact_folder)
            logger.info("Model training completed.")
        except Exception as e:
            logger.error(f"Exception occurred during model training: {e}")
            raise CustomException(e, sys)