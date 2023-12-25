from keyword_extract import extract_keywords
import re
import spacy

nlp = spacy.load("en_core_web_sm")

# Function to extract entities (name, location, skills)
def extract_entities(text):
    doc = nlp(text)
    entities = {
        "name": [],
        "location": [],
        "skills": [],
        "keywords": []
    }

    for ent in doc.ents:
        if ent.label_ == "PERSON":
            entities["name"].append(ent.text)
        elif ent.label_ == "GPE":
            entities["location"].append(ent.text)
        elif ent.label_ == "SKILLS":
            entities["skills"].append(ent.text)

    return entities

# Function to extract phone numbers using regular expressions
def extract_phone_numbers(text):
    phone_numbers = re.findall(r'\b\d{3}[-.\s]?\d{3}[-.\s]?\d{4}\b', text)
    return phone_numbers

# Function to extract email addresses using regular expressions
def extract_emails(text):
    emails = re.findall(r'\S+@\S+', text)
    return emails

# Function to extract information (skills, location, keywords)
def extract_information(text):
    extracted_entities = {
        "name": [],
        "location": [],
        "skills": [],
        "keywords": []
    }

    doc = nlp(text)
    
    # Extract skills using specific rules or patterns
    skills_list = ["Python", "Machine Learning", "Data Analysis", "SQL", "Latex"]
    for token in doc:
        if token.text in skills_list:
            extracted_entities["skills"].append(token.text)
    
    # Extract location entities (modify as per your requirements)
    for ent in doc.ents:
        if ent.label_ == "GPE":
            extracted_entities["location"].append(ent.text)

    # Extract keywords using your preferred technique (e.g., YAKE)
    extracted_entities["keywords"] = extract_keywords(text)

    return extracted_entities