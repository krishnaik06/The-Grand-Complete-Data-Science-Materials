# Domain-Specific-Keyword-Extraction-using-Spacy
* Named entity recognition (NER) , also known as entity chunking/extraction , is a popular technique used in information extraction to     identify and segment the named entities and classify or categorize them under various predefined classes.
* In any text document, there are particular terms that represent specific entities that are more informative and have a unique context.   These entities are known as named entities , which more specifically refer to terms that represent real-world objects like people,       places, organizations, and so on, which are often denoted by proper names. A naive approach could be to find these by looking at the     noun phrases in text documents. 
<h1>Goal</h2>

* Customized NER model is created using NER to find domain specific Keyword
<h1>Background</h1>

* NER plays very important role in information extraction.
* When we have large corpus containing different keywords related to different domain,NER comes in action in those scenarios.
* NER can be beneficial in news headlines.

<h1>Data Preparation</h1>
  
  *  Data preparation is the main challenging task in NER.
  *  In this project , I have created a corpus of 65 records.
  *  data.txt contains 65 sentences.
  *  labels.csv contains entities and labels 
<h1>Model Training</h1>
  
  * Customized model is created using spacy to find domain specific keyword.
  * Here the domain specific keywords are food,cloth.
  * The user is asked to enter the model name and the model is saved with the same name in local directory.
<h1>Testing</h1>
  
  * The user is asked to enter the text.
  * The user will get domain specific keyword:food,cloth based on the text
<h1>SetUp</h1>
  
  * pip install spacy
<h1>Steps to follow to execute the project</h1>
  
  * clone the repository into your local system
  * Run the command: python Nermodel.py
  * Note You can change the number of iterations based on your requirement, I have kept 20.
  * After the completion of model training, you need to enter the model name and the model is downloaded into your local directory         where the code is stored.
  * Finally , you need to enter the text and you will get the keyword based on your text.
  
  <h1>Future Work</h1>
  
  * I have used only 65 sentences to train the model, you can use more corpus and train the model.
  * You can use as many lables as you want,you can add more lables 
  * You can use NER in news headlines and you can extract domain specific keyword from the news.
  
  
  ![pic](https://user-images.githubusercontent.com/17763961/103242008-d8f98100-497a-11eb-9923-4c49df164a3f.jpg)
  
  ![pic2](https://user-images.githubusercontent.com/17763961/103242100-27a71b00-497b-11eb-9441-2ea522baf044.png)


