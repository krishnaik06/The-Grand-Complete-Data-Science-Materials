import spacy
import re
# Load the English language model
nlp = spacy.load("en_core_web_sm")

def extract_keywords(text):
    # Process the text with spaCy
    doc = nlp(text)

    # Extract keywords based on relevant criteria (e.g., noun phrases)
    keywords = [chunk.text for chunk in doc.noun_chunks]

    return keywords

