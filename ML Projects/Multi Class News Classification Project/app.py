import streamlit as st
import keras
import tensorflow as tf
import requests
import numpy as np
import nltk
import spacy
from nltk.corpus import stopwords
from tqdm import tqdm
import pandas as pd
import pycountry
from keras.preprocessing.text import one_hot,Tokenizer
from keras.utils import pad_sequences
import datetime

#Downloading some dependencies
# nltk.download('stopwords')
# nltk.download('punkt')
# nltk.download('wordnet')
nlp = spacy.load('en_core_web_sm')

#Loading the DL Model

model = tf.keras.models.load_model('News_Classification_bidirectional_lstm_model.keras')

#Setting the titles

st.markdown("<h1 style='text-align: center; color: white;'>Multi-Class News Classifier</h1>", unsafe_allow_html=True)

# # Creating a list of countries

# names_of_countries = []
# length = len(pycountry.countries)
# for i in range(length):
#     names_of_countries.append(list(pycountry.countries)[i].name)

#Fetching the country's ISO code
def fetch_country_code(name):
    code = pycountry.countries.get(name=name).alpha_2
    return code.lower()


#Fetching the news

def fetch_news(name, date_from, date_to):
    
    
    
    headers = {
       "User-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36 Edg/115.0.1901.200"
}
    news = []

    global final
    # code = fetch_country_code(country_name)
    
    code = 'us'
    query = name
    
    url = 'https://newsapi.org/v2/everything?q={}&from={}&to=()&language=en&sortBy=popularity&apiKey=a1e91cf9073f4b85aa784fe5f37e6294'.format(query, date_from, date_to)
        
    data = requests.get(url, headers=headers).json()
    # print('------------------------------------------------------------------------------------------------------------------')

    tot_res = data['totalResults']
    ls_name = []
    ls_title = []
    ls_desc = []
    ls_url = []
    ls_img_url = []
    publish_date = []
    ls_content = []
    print(url, tot_res)
    range_ = tot_res // 100
    for i in tqdm(range(1, range_)):
        try:
            next_page_url = 'https://newsapi.org/v2/everything?q={}&from={}&to={}&language=en&page={}&sortBy=popularity&apiKey=a1e91cf9073f4b85aa784fe5f37e6294'.format(query, date_from, date_to, str(i))
            for j in data['articles']:

                    name = j['source']['name'] 
                    title = j['title']
                    desc = j['description']
                    url = j['url']
                    img_url = j['urlToImage']
                    date = j['publishedAt']
                    content = j['content']

                    ls_name.append(name)
                    ls_title.append(title)
                    ls_desc.append(desc)
                    ls_url.append(url)
                    ls_img_url.append(img_url)
                    ls_content.append(content)
                    publish_date.append(date)

            data = requests.get(next_page_url, headers=headers).json()
            
        except:
            pass
    dic = ({
                'name': ls_name,
                'title': ls_title,
                'description': ls_desc,
                'content': ls_content,
                'url': ls_url,
                'img_url': ls_img_url,
                'Date': publish_date
    })
        
    final = pd.DataFrame(dic)  
    final.to_csv('news.csv', index=False)
    
    
def preprocess():
    
    df = pd.read_csv('news.csv')
    print(df)

    
    df['tags'] = df['title'] + df['description'] + df['content']
    
    df['tags'] = df['tags'].astype('str')

    #Lowercasing

    df['tags'] =  df['tags'].str.lower()
    #Removing Contradictions

    import contractions

    def remove_contradictions(text):

        return " ".join([contractions.fix(word.text) for word in nlp(text)])

    df['tags']= df['tags'].apply(remove_contradictions)
    
    # Removing HTML tags

    import re

    def remove_html(text):
        pattern = re.compile('<.*?>')
        return pattern.sub(r'', text)

    df['tags'] =  df['tags'].apply(remove_html)

    #Remove @

    def remove_at_the_rate(text):

        ls = []
        new = []

        ls = nlp(text)

        for word in ls:
            if word.text != "@":
                new.append(word.text)

        return ' '.join(new)

    df['tags'] =  df['tags'].apply(remove_at_the_rate)
    
    #Removing URL

    import re

    def remove_url(text):
        pattern = re.compile(r'https?://\S+|www\.\S+')
        return pattern.sub(r'', text)

    df['tags']=  df['tags'].apply(remove_url)


    #Remmove punctuation

    import string

    punc = string.punctuation

    def  remove_punc(text):

        return text.translate(str.maketrans('', '', punc))

    df['tags']=  df['tags'].apply(remove_punc)

    # Removing stop words


    from nltk.corpus import stopwords

    stopwords = stopwords.words('english')

    def remove_stop_words(text):
        ls = []
        new = []

        ls = nlp(text)

        for word in ls:
            if word.text not in stopwords:

                new.append(word.text)

        return ' '.join(new)

    df['tags'] =  df['tags'].apply(remove_stop_words)

    def Lemmetization(text):

        return " ".join([word.lemma_ for word in nlp(text)])


    df['tags'] =  df['tags'].apply(Lemmetization)
    
    def is_alpha(string):
    
        ls = string.split()
        new = []
        # print(ls)
        for word in ls:
            if word.isalpha()==True:
                new.append(word)
        return ' '.join(new)
    
    df['tags'] =  df['tags'].apply(is_alpha)
    
    df.to_csv('preprocessed.csv', index=False)

def predict():
    
    preprocessed = pd.read_csv('preprocessed.csv')
    train_df = pd.read_csv('train_transformed.csv')
    news = pd.read_csv('news.csv')
    tok = Tokenizer()
    tok.fit_on_texts(train_df['tags'])
    
    max_len = 100
    
    encd_news = tok.texts_to_sequences(preprocessed['tags'])
    embd_dim = 200
    
    pad_news = pad_sequences(maxlen = max_len, padding='pre', sequences=encd_news)
    
    
    y_pred = model.predict([pad_news], 1024)
    y_pred = np.argmax(y_pred, axis=1)
    y_pred = y_pred.T
    # print(y_pred)
    dic = {
        'predictions': y_pred
    }
    pred = pd.DataFrame(dic)
    predicitions_merged = pd.concat([news, pred], axis=1)
    print(predicitions_merged)
    print(predicitions_merged.duplicated().sum())
    predicitions_merged['predictions'] = predicitions_merged['predictions'].astype('str')
    # print(type(predicitions_merged.iloc[0,7]))
    print(predicitions_merged.duplicated().sum())
    predicitions_merged['predictions'].replace(to_replace=['0', '1', '2', '3'],value=['World', 'Sports', 'Business', 'Sci-Fi/Tech'], inplace=True)
    predicitions_merged.drop_duplicates(inplace=True)
    predicitions_merged.fillna('N/A', inplace=True)
    predicitions_merged.to_csv('predictions.csv', index=False)

    
def display():
    
    bar = st.progress(25)
    predicitions_merged = pd.read_csv('predictions.csv')
    tabs_titles = ['World', 'Sports', 'Business', 'Sci-Fi/Tech']
    
    tab1, tab2, tab3, tab4 = st.tabs(tabs_titles)

    with tab1:
    
        for i in range(predicitions_merged.shape[0]):
            
            if predicitions_merged.iloc[i, 7] == 'World':
                st.markdown("<h4 style='text-align: center; color: white;'>{}</h4>".format(predicitions_merged.iloc[i, 1]), unsafe_allow_html=True)
                st.divider()
                
                col1, col2, col3 = st.columns([5, 5, 3])
                
                with col1:
                    try:
                        img_url = predicitions_merged.iloc[i, 5]
                        image = st.image(img_url)
                    except:
                        pass
                
                with col2:
                    desc = predicitions_merged.iloc[i, 2]
                    st.write(desc)
                    
                with col3:
                    date = predicitions_merged.iloc[i, 6]
                    date = date[:10]
                    with st.expander('Published'):
                        st.write(date)
                    with st.expander('Source'):
                        st.write(predicitions_merged.iloc[i, 0])
                    
                
                with st.expander('Description'):
                    
                    content = predicitions_merged.iloc[i, 2]
                    st.write(content)
                
                with st.expander('Content'):
                    
                    content = predicitions_merged.iloc[i, 3]
                    st.write(content)
                    
                with st.expander('Website'):
                    
                    url = predicitions_merged.iloc[i, 4]
                    st.write(url)
                    
         
    with tab2:
        
            bar.progress(50)        
            for i in range((predicitions_merged.shape[0])):
            
                if predicitions_merged.iloc[i, 7] == 'Sports':
                    st.markdown("<h4 style='text-align: center; color: white;'>{}</h4>".format(predicitions_merged.iloc[i, 1]), unsafe_allow_html=True)
                    st.divider()

                    col1, col2, col3 = st.columns([5, 5, 3])

                    with col1:
                        try:
                            img_url = predicitions_merged.iloc[i, 5]
                            image = st.image(img_url)
                        except:
                            pass
                    
                    with col2:
                        desc = predicitions_merged.iloc[i, 2]
                        st.write(desc)

                    with col3:
                        date = predicitions_merged.iloc[i, 6]
                        date = date[:10]
                        with st.expander('Published'):
                            st.write(date)
                        with st.expander('Source'):
                            st.write(predicitions_merged.iloc[i, 0])


                    with st.expander('Description'):

                        content = predicitions_merged.iloc[i, 2]
                        st.write(content)

                    with st.expander('Content'):

                        content = predicitions_merged.iloc[i, 3]
                        st.write(content)

                    with st.expander('Website'):

                        url = predicitions_merged.iloc[i, 4]
                        st.write(url)
    
    with tab3:
            bar.progress(75)        
            for i in range(predicitions_merged.shape[0]):
            
                if predicitions_merged.iloc[i, 7] == 'Business':
                    st.markdown("<h4 style='text-align: center; color: white;'>{}</h4>".format(predicitions_merged.iloc[i, 1]), unsafe_allow_html=True)
                    st.divider()

                    col1, col2, col3 = st.columns([5, 5, 3])

                    try:
                        img_url = predicitions_merged.iloc[i, 5]
                        image = st.image(img_url)
                    except:
                        pass
                    
                    with col2:
                        desc = predicitions_merged.iloc[i, 2]
                        st.write(desc)

                    with col3:
                        date = predicitions_merged.iloc[i, 6]
                        date = date[:10]
                        with st.expander('Published'):
                            st.write(date)
                        with st.expander('Source'):
                            st.write(predicitions_merged.iloc[i, 0])


                    with st.expander('Description'):

                        content = predicitions_merged.iloc[i, 2]
                        st.write(content)

                    with st.expander('Content'):

                        content = predicitions_merged.iloc[i, 3]
                        st.write(content)

                    with st.expander('Website'):

                        url = predicitions_merged.iloc[i, 4]
                        st.write(url)
    
    with tab4:
            bar.progress(100)   
            for i in range(predicitions_merged.shape[0]):
            
                if predicitions_merged.iloc[i, 7] == 'Sci-Fi/Tech':
                    st.markdown("<h4 style='text-align: center; color: white;'>{}</h4>".format(predicitions_merged.iloc[i, 1]), unsafe_allow_html=True)
                    st.divider()

                    col1, col2, col3 = st.columns([5, 5, 3])

                    try:
                        img_url = predicitions_merged.iloc[i, 5]
                        image = st.image(img_url)
                    except:
                        pass

                    with col2:
                        desc = predicitions_merged.iloc[i, 2]
                        st.write(desc)

                    with col3:
                        date = predicitions_merged.iloc[i, 6]
                        date = date[:10]
                        with st.expander('Published'):
                            st.write(date)
                        with st.expander('Source'):
                            st.write(predicitions_merged.iloc[i, 0])


                    with st.expander('Description'):

                        content = predicitions_merged.iloc[i, 2]
                        st.write(content)

                    with st.expander('Content'):

                        content = predicitions_merged.iloc[i, 3]
                        st.write(content)

                    with st.expander('Website'):

                        url = predicitions_merged.iloc[i, 4]
                        st.write(url)
    
                        
                        
name = st.text_input('Enter a keyword that you want your articles to have!')
date_from = st.date_input('From date for news articles', value = datetime.date(2023, 8, 27), min_value  = datetime.date(2020, 1, 1))
date_to = st.date_input('To date for news articles', value = datetime.date(2023, 8, 27), min_value  = datetime.date(2020, 1, 1))

if st.button('Fetch!'):

    fetch_news(name, date_from, date_to)

    preprocess()

    predict()

    display()