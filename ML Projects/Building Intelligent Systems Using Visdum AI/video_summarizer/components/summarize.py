import sys
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
from video_summarizer.exception import CustomException
from video_summarizer.logger import logger


class Summarizer:
  def load_model(self):
      try:
          logger.info("Loading tokenizer and model...")
          try:
              self.tokenizer = AutoTokenizer.from_pretrained("best_model")
              self.model = AutoModelForSeq2SeqLM.from_pretrained("best_model")
              logger.info("Tokenizer and model loaded from the best_model directory")
          except:
              try:
                  logger.info("Model not available in the best_model directory. Checking model trainer artifacts...")

                  self.tokenizer = AutoTokenizer.from_pretrained("artifacts/model_trainer")
                  self.model = AutoModelForSeq2SeqLM.from_pretrained("artifacts/model_trainer")

                  logger.info("Tokenizer and model loaded from the artifacts/model_trainer directory")
              except:
                  logger.info("Model not available in artifacts/model_trainer and best_model directories. Loading from Hugging Face model hub...")

                  self.tokenizer = AutoTokenizer.from_pretrained("sshleifer/distilbart-cnn-12-6")
                  self.model = AutoModelForSeq2SeqLM.from_pretrained("sshleifer/distilbart-cnn-12-6")

                  logger.info("Tokenizer and model loaded from Hugging Face model hub")
      except Exception as e:
          logger.error("Error loading the model.")
          raise CustomException(e, sys)

  def summarize_text(self, transcript):
      try:
          logger.info("Initiating summarizer...")

# dataet max_length-> 1024 - 1055 = 21
          inputs = self.tokenizer(transcript,
                            max_length=1024,
                            truncation=True,
                            return_tensors="pt")

          summary_ids = self.model.generate(
              inputs["input_ids"], num_beams=2, min_length=50, max_length=1024)
          
          summary = self.tokenizer.batch_decode(
              summary_ids, skip_special_tokens=True, clean_up_tokenization_spaces=False)[0]
          
          return summary
      except Exception as e:
          logger.error("Check your Best Model directory.")
          raise CustomException(e, sys)
