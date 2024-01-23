# Relationship-Extraction-Network-Of-The-Witcher
![network pic 2](https://user-images.githubusercontent.com/22730220/174459596-56fe0394-f263-4090-8ee6-61d77b9a3363.jpeg)

# Strategy

## Web-Scraping
* Web-scraping from [Witcher WIKI](https://witcher.fandom.com/wiki/Witcher_Wiki)
* [Selenium](https://selenium-python.readthedocs.io/)

## Named Entity recognition
**Named Entity Recognition** (NER) is a natural language processing technique that identifies and classifies named entities in text into predefined categories, such as people, organizations, and locations.
* NER using [Spacy](https://spacy.io/api/entityrecognizer)
* Spacy [English language model](https://spacy.io/models/en)

## Preprocessing
1. Tokenized every books into a list of sentences and label them with the name of the characters appearing in the sentence
2. Define a window size of how far two sentences are apart from each other and assume that if two characters are mentioned in two sentences within this window then there is a relationship between them.

## Resources
1. [Books](https://github.com/dworschak/Witcher/tree/master)

## Python Librabries
| Libraries | Used for | 
| -------- | -------- | 
| Selenium    | Webscraping. Beginner friendly. Suitable to small project     | 
| Spacy    | Text processing     |
| networkx    | Analyzing network relationship     |
| pyvis    | network graph visualization     |
| re    | Regular Expression     |
