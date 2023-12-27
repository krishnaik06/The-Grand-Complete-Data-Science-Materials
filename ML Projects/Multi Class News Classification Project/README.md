
# Multi-Class News Classification WebApp


- **Primary Goal**: To provide an interface to users to find news under certain categories such as Tech, World, Business and Sports

- **Solution**: Made use of the AGI news kaggle dataset and NLP-based preprocessing techniques along with custom-trained Word2Vec model alongwth Bi-LSTM model.

- **Result**: Succesfully built the said WebApp with streamlit as front-end. Achieved an accuracy of 91% with precision 91 % and recall 90%

- **Tools Used**: Keras, Tensorflow, Word2Vec (Word Embeddings), Bi-LSTMs, NLTK, Spacy, Streamlit
## Features

- Can display news category wise be it Tech, World, Sports or Business
- News are fetched from a avriety of news resources through NewsAPI which gives different perspective on the same topic/domain.
- Gives user the ability to select a period of time to fetch the news articles.

## Tech Stack

**Backend(Logic):** Tensorflow, Keras, Word2Vec, Neural Networks,  Bi-LSTM, NLTK, Spacy, Pickle, Render(Deployment)

**Frontend:** Streamlit (Build)


## API Reference

#### NewsApi Key (REQUIRED)

```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `api_key` | `string` | **Required**. Your API key |

```


## Run Locally


Clone the project

```bash
  git clone https://github.com/YuvrajSingh-mist/News_Multiclass_Category_Classifier
```

Go to the project directory

```bash
  cd News_Multiclass_Category_Classifier
```

Install dependencies

```bash
  pip install -r requirements.txt
```


Start the WebApp

```bash
  streamlit run app.py
```


## Authors

- [@Yuvraj Singh](https://www.github.com/YuvrajSingh-mist)

