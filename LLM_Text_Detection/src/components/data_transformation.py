# Import necessary modules
import os
import pandas as pd
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
from src.logger import logging
from src.entity import DataTransformationConfig
from sklearn.model_selection import train_test_split

# Download NLTK resources
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('wordnet')

# Class definition for DataTransformation
class DataTransformation:
    def __init__(self, raw_text_path, config: DataTransformationConfig):
        # Initialize the DataTransformation class with a raw text path and a configuration object
        self.raw_text_path = raw_text_path
        self.config = config

    # Clean text by removing symbols, extra spaces, numbers, alphanumerics, etc., and convert into lowercase
    def clean_text(self, text):
        # Convert the whole text into lowercase
        text = text.lower()
        # Remove unwanted characters from text using regex patterns
        pattern1 = re.compile(r'[^a-zA-Z\s]')
        pattern2 = re.compile(r'\n')
        # Replace matched characters with an empty string and space
        text = pattern1.sub('', text)
        cleaned_text = pattern2.sub(' ', text)
        return cleaned_text

    # Tokenize the texts for removing stopwords, convert text into tokens
    def tokenize_text(self, text):
        words = word_tokenize(text)
        return words

    # Remove stopwords from tokenized text
    def remove_stopwords(self, tokens):
        # English language stopwords
        stop_words = set(stopwords.words('english'))
        filtered_tokens = [word for word in tokens if word not in stop_words]
        return filtered_tokens

    # Stem the tokens
    def stem_tokens(self, tokens):
        # Porter stemmer
        stemmer = PorterStemmer()
        stemmed_tokens = [stemmer.stem(word) for word in tokens]
        return stemmed_tokens

    # Get filtered text after above cleaning processes
    def filtered_text(self, tokens_list):
        text = ' '.join(tokens_list)
        return text

    def transform_text(self):
        # Load the dataset from the CSV file
        df = pd.read_csv(self.raw_text_path)
        logging.info("Data cleaning starts...")
        # Apply the cleaning and transformation processes to the 'text' column
        logging.info("Removing punctuations, symbols etc. from text and converting to lowercase...")
        df['text'] = df['text'].apply(self.clean_text)
        logging.info("Converting text into tokens...")
        df['text'] = df['text'].apply(self.tokenize_text)
        logging.info("Removing stopwords from tokenized text...")
        df['text'] = df['text'].apply(self.remove_stopwords)
        logging.info("Performing steming on tokenized text...")
        df['text'] = df['text'].apply(self.stem_tokens)
        logging.info("Getting filtered text from tokenized text...")
        df['text'] = df['text'].apply(self.filtered_text)
        logging.info("Data cleaning/transformation end...")
        # Save the cleaned text to a new CSV file
        logging.info(f"Cleaned text saved at {self.config.cleaned_text_file}...")
        # Shuffle the dataset
        df = df.sample(frac=1, random_state=42, ignore_index=True)
        df.to_csv(self.config.cleaned_text_file, index=False)

        # Split the cleaned text data into train, test and validation splits
        df_train, df_test  = train_test_split(df, random_state=42, test_size=0.3)
        df_valid, df_test = train_test_split(df_test, random_state=42, test_size=0.5)
        # Save the splits into drive
        df_train.to_csv(self.config.train_text_file, index=False)
        df_test.to_csv(self.config.test_text_file, index=False)
        df_valid.to_csv(self.config.valid_text_file, index=False)