# Required modules
import pandas as pd
from src.logger import logging
from src.entity import ModelTrainerConfig
from src.utils.common import data_object, tokenize_data
import torch
from torch.utils.data import DataLoader
from transformers import (
    AutoModelForSequenceClassification, 
    AdamW, 
    get_scheduler
)
from tqdm.auto import tqdm

class ModelTrainer:
    def __init__(self, train_data_path, valid_data_path, config: ModelTrainerConfig):
        # Initialize the ModelTrainer class with paths to training and validation data and a configuration object
        self.train_texts_path = train_data_path
        self.valid_texts_path = valid_data_path
        self.config = config

    def train_model(self):
        # Read training and validation data from CSV files
        train_df = pd.read_csv(self.train_texts_path)
        valid_df = pd.read_csv(self.valid_texts_path)

        # Create a data object for tokenization
        data = data_object(train_df.iloc[:8, :], valid_df.iloc[:8, :])
        # Tokenize the data using provided model checkpoint
        data_collator, tokenized_data = tokenize_data(data, self.config.model_ckpt)
        # Define data loaders for further processing
        train_dataloader = DataLoader(
            tokenized_data["train"], shuffle=True, batch_size=self.config.train_batch_size, collate_fn=data_collator
        )
        eval_dataloader = DataLoader(
            tokenized_data["validation"], batch_size=self.config.train_batch_size, collate_fn=data_collator
        )
        
        # Check shape of a batch
        for batch in train_dataloader:
            break
        {k: v.shape for k, v in batch.items()}

        # Instantiate a sequence classification model
        model = AutoModelForSequenceClassification.from_pretrained(self.config.model_ckpt, num_labels=self.config.num_labels)
        # Configure optimizer and learning rate
        optimizer = AdamW(model.parameters(), lr=float(self.config.learning_rate))
        # Set epochs, training steps, and scheduler
        num_epochs = self.config.num_train_epochs
        num_training_steps = num_epochs * len(train_dataloader)
        lr_scheduler = get_scheduler(
            "linear",
            optimizer=optimizer,
            num_warmup_steps=self.config.num_warmup_steps,
            num_training_steps=num_training_steps,
        )

        # Set hardware for model training (CUDA if available, otherwise CPU)
        device = torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu")
        model.to(device)

        # Training loop
        # Show progress of training
        logging.info("Training loop start.....")
        progress_bar = tqdm(range(num_training_steps))
        model.train()

        for epoch in range(num_epochs):
            for batch in train_dataloader:
                batch = {k: v.to(device) for k, v in batch.items()}
                outputs = model(**batch)
                loss = outputs.loss
                loss.backward()
                optimizer.step()
                lr_scheduler.step()
                optimizer.zero_grad()
                progress_bar.update(1)
        logging.info("Training loop end.....")

        # Save the trained model to the specified directory
        model_save_path = self.config.trained_model_dir
        model.save_pretrained(model_save_path)
        logging.info(f"Trained model saved at {self.config.trained_model_dir}.....")

        # return the evaluation data
        return eval_dataloader