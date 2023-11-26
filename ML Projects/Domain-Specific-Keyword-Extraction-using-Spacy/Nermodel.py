#importing libraries
from spacy.lang.en import English 
from spacy import displacy  
import re
import pandas as pd
import spacy
import random
#reading text file containing text data
f = open("data.txt", "r",encoding='cp1252')
paragraph = f.read()
#reading label data
labels = pd.read_csv('labels.csv')
data_dict = labels.set_index('entities')['labels'].to_dict()

nlp = English()
nlp.add_pipe(nlp.create_pipe('sentencizer')) # updated
doc = nlp(paragraph)
sentences = [sent.string.strip() for sent in doc.sents]

inner_tuple = ()
outer_tuple = ()
outer_list = []
for sentence in sentences:
    wordList = re.sub("[^\w]", " ",  sentence).split()
    for word in wordList:
        
        inner_dict = {}
        inner_list = []
        if word in data_dict:
            start_word = sentence.find(word)
            end_word = start_word+len(word)
            label = data_dict.get(word)
            inner_tuple = (start_word,end_word,label)
            inner_list.append(inner_tuple)
            inner_dict['entities'] = inner_list
            outer_tuple = (sentence,inner_dict)
            outer_list.append(outer_tuple)

TRAIN_DATA = outer_list
print(outer_list)

def train_spacy(data,iterations):
    TRAIN_DATA = data
    nlp = spacy.blank('en')  # create blank Language class
    # create the built-in pipeline components and add them to the pipeline
    # nlp.create_pipe works for built-ins that are registered with spaCy
    if 'ner' not in nlp.pipe_names:
        ner = nlp.create_pipe('ner')
        nlp.add_pipe(ner, last=True)
       

    # add labels
    for _, annotations in TRAIN_DATA:
        for ent in annotations.get('entities'):
            ner.add_label(ent[2])

    # get names of other pipes to disable them during training
    other_pipes = [pipe for pipe in nlp.pipe_names if pipe != 'ner']
    with nlp.disable_pipes(*other_pipes):  # only train NER
        optimizer = nlp.begin_training()
        for itn in range(iterations):
            print("Starting iteration " + str(itn))
            random.shuffle(TRAIN_DATA)
            losses = {}
            for text, annotations in TRAIN_DATA:
                nlp.update(
                    [text],  # batch of texts
                    [annotations],  # batch of annotations
                    drop=0.2,  # dropout - make it harder to memorise data
                    sgd=optimizer,  # callable to update weights
                    losses=losses)
            print(losses)
    return nlp

#20 represents the number of iteration, you can give iteration based on our requirements
prdnlp = train_spacy(TRAIN_DATA, 20)

# Save our trained Model
modelfile = input("Enter your Model Name: ")
prdnlp.to_disk(modelfile)

#Test your text
test_text = input("Enter your testing text: ")
doc = prdnlp(test_text)
for ent in doc.ents:
    print(ent.text, ent.start_char, ent.end_char, ent.label_)
spacy.displacy.render(doc, style="ent", page="true")
