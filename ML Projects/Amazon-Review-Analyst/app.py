import streamlit as st

import numpy as np
import pandas as pd
import re

import os

from keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences

import pickle

import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

# Download the stopwords if not already downloaded
nltk.download('stopwords')
nltk.download('punkt')

from amazon_review import Product
import htmls

import plotly.express as px
import plotly.graph_objects as go
import plotly.colors

import streamlit.components.v1 as com

from PIL import Image
import base64

cwd = os.path.dirname(__file__)

assets_path = os.path.join(cwd, r'assets')
styles_path = os.path.join(cwd, r'styles')

page_icon = Image.open(os.path.join(assets_path, 'conversation.png'))
default_image = Image.open(os.path.join(assets_path, 'default.jpg'))

# com.html(htmls.background)


## Setting page properties
st.set_page_config(
    page_title="Review Analyst",
    page_icon=page_icon,
    layout="wide"
)

def add_bg_from_url(image_file):
    with open(image_file, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    st.markdown(
         f"""
         <style>
         .stApp {{
             background-image: url(data:image/{"jpg"};base64,{encoded_string.decode()});
             background-size: cover;
             background-size: cover;
         }}
         </style>
         """,
         unsafe_allow_html=True
     )

add_bg_from_url(os.path.join(assets_path, r'Product_Background.jpg'))

## Injecting custom css defines in styles.css in styles directory
with open(os.path.join(styles_path, 'styles.css')) as css:
    st.markdown(f"<style>{css.read()}</style>", unsafe_allow_html=True)

## Initilizing session state variables
if 'received_url' not in st.session_state:
    st.session_state.received_url = False   # for accepting url on pressing enter in URL field

if 'rerunning' not in st.session_state:
    st.session_state.rerunning = False      # for letting program know its rerunning due to interactive widgets

if 'product' not in st.session_state:
    st.session_state.product = False        # for storing product details

if 'old_url' not in st.session_state:
    st.session_state.old_url = False        # URL from previous search

if 'new_url' not in st.session_state:
    st.session_state.new_url = False        # URL from current search

if 'radio_selected' not in st.session_state:
    st.session_state.radio_selected = False # holds the value when radio button selected
    
if 'proceed' not in st.session_state:
    st.session_state.proceed = False        # holds the value if proceed button selected

if 'num_pages' not in st.session_state:
    st.session_state.num_pages = False      # holds the value for selected number of pages

if 'continue_flow' not in st.session_state:
    st.session_state.continue_flow = False      # for page increment in page number field

if 'radio_state' not in st.session_state:
    st.session_state.radio_state = False      # for page increment in page number field

if 'model' not in st.session_state:
    st.session_state.model = False           # for storing the model
    st.session_state.tokenizer = False           # for storing the tokenizer

## Main header of the web app
st.write(htmls.header, unsafe_allow_html=True)

## Horizontal line
st.markdown(htmls.horizontal_line, unsafe_allow_html=True)

def accept_url():
    """this functions make sure the URL is updated when user hits enter
    """
    st.session_state.received_url = True
    st.session_state.rerunning = False

def change_radio():
    """this functions the sets the value of session state varibles for radio buttons and proceed button 
    """
    print('changing radio selected and proceed to true')
    st.session_state.radio_selected = True
    st.session_state.proceed = True

def set_page_num(a):
    """this funstion sets the valu of number of pages into session state variable
    """
    # print('inside set_page_num')
    st.session_state.continue_flow = a

def preprocess(reviews_df):
    """This is used to preprocess the data before sentiment analysis

    It performs operations like lower the case, removing HTML tags, removing URLs, removing special characters,
    removing accented characters and removing emails.

    Args:
        reviews_df (pandas.core.frame.DataFrame): A pandas dataframe with "reviews" column.

    Returns:
        pandas.core.frame.DataFrame: A pandas dataframe with preprocessed test in new column "cleaned reviews".
    """
    reviews_df['cleaned_reviews'] = reviews_df['reviews'].str.lower()
    reviews_df['cleaned_reviews'] = reviews_df['cleaned_reviews'].apply(lambda r: re.sub(r'http\S+', '', r))
    reviews_df['cleaned_reviews'] = reviews_df['cleaned_reviews'].apply(lambda r: re.sub(r'\S*@\S+', '', r))
    reviews_df['cleaned_reviews'] = reviews_df['cleaned_reviews'].apply(lambda r: re.sub(r'\S*#\S+', '', r))
    reviews_df['cleaned_reviews'] = reviews_df['cleaned_reviews'].apply(lambda r: re.sub(r'<.*?>', '', r))

    translate_values = {'â€™': "'"}

    reviews_df['cleaned_reviews'] = reviews_df['cleaned_reviews'].apply(lambda r: r.translate(translate_values))
    reviews_df['cleaned_reviews'] = reviews_df['cleaned_reviews'].apply(lambda r: re.sub(r'[^a-zA-Z\'\s]', ' ', r))
    # reviews_df['cleaned_reviews'] = reviews_df['cleaned_reviews'].apply(lambda r: re.sub(r'[^a-zA-Z0-9\'\s]', ' ', r))
    reviews_df['cleaned_reviews'] = reviews_df['cleaned_reviews'].apply(lambda r: r.strip())

    # Get the list of English stopwords
    english_stopwords = nltk.corpus.stopwords.words('english')

    not_stopwords = ['but', 'no', 'nor', 'not', "don't", "aren't", "couldn't", "didn't", "doesn't", "hadn't", "hasn't", "haven't", "isn't", "mightn't", "mustn't", "needn't", "shan't", "shouldn't", "wasn't", "weren't", "won't", "wouldn't", 'this', 'other', 'others', 'than']

    stopwords = [i for i in english_stopwords if i not in not_stopwords]

    stopwords.extend([' ', ''])
    
    stemmer = PorterStemmer()
    reviews_df['cleaned_reviews'] = reviews_df['cleaned_reviews'].apply(lambda r: nltk.word_tokenize(r))
    reviews_df['cleaned_reviews'] = reviews_df['cleaned_reviews'].apply(lambda r: [stemmer.stem(word) for word in r])
    stopwords = [stemmer.stem(word) for word in stopwords]

    reviews_df['cleaned_reviews'] = reviews_df['cleaned_reviews'].apply(lambda r: ' '.join([i for i in r if i not in stopwords]))

    return reviews_df

@st.cache_resource
def load_ml_model():
    """This function loads BERT Pretrained model for sentiment analysis and creates a pipeline.

    Model used: finiteautomata/beto-sentiment-analysis


    Returns:
        transformers.modellines.text_classification.TextClassificationPipeline: a transmormers pipeline.
    """
    model_name = r'amazon_review_sentiment_cnn_model_v2.h5'
    tokenizer_name = r'tokenizer_v2.pickle'
    model_files_path = os.path.join(cwd, f'model')
    model_path = os.path.join(model_files_path, model_name)
    tokenizer_path = os.path.join(model_files_path, tokenizer_name)
    model = load_model(model_path)
    with open(tokenizer_path, 'rb') as f:
        tokenizer = pickle.load(f)
    return model, tokenizer


form = st.container()   # container for input 
with form:
    ## Text field to get URL of the product
    url = st.text_input('Enter the url: ', placeholder='Enter the product URL', label_visibility='collapsed', on_change=accept_url, help='Copy the URL of the product from amazon and paste.')
    submit = st.button('**Submit**')

if (submit and url) or (st.session_state.received_url and url) or st.session_state.rerunning:


    st.session_state.rerunning = True
    st.session_state.received_url = False
    st.session_state.new_url = url

    # body = st.container()

    body = st.empty()
    if st.session_state.new_url != st.session_state.old_url:
        st.session_state.proceed = False
        st.session_state.num_pages = 0
        st.session_state.continue_flow = False
        st.session_state.radio_selected = False
        st.session_state.old_url = st.session_state.new_url
        st.session_state.product = False
        body.empty()
        print(f'inside if {body}')

    with body.container():
        if not st.session_state.product:
            with st.spinner('Searching product...'):
                if not st.session_state.model:
                    st.session_state.model, st.session_state.tokenizer = load_ml_model()
                # print(url)
                st.session_state.product =  Product(url)
                # print()

        product = st.session_state.product
        if product.__str__() == 'No product found':
            st.error('Unable to find the product. Please retry.')
            # st.stop()
        else:
            a, b = st.columns([1,5], gap='small')
            if product.image:
                a.image(product.image)
            else:
                a.image(default_image)
            b.write(f'### [{product.product_name}]({product.product_link})', )


            all_ratings  = product.ratings

            # pie_chart = px.pie(values=list(all_ratings.values()), names=list(all_ratings.keys()), hole=0.5) 
            # st.plotly_chart(pie_chart)

            keys = list(all_ratings.keys())
            bold_keys = [f'<b>{i}</b>' for i in keys]
            fig = go.Figure(data=[go.Pie(labels=bold_keys, values=list(all_ratings.values()), textinfo='label+percent', hole=0.5, title="<b>All Reviews</b>", title_font = dict(size=26,family='Verdana', 
                                            color='#571c25'))], layout={'showlegend':False, 'colorway':plotly.colors.diverging.RdBu})

            fig.update_layout(legend=dict(
                                    x=0.2,
                                    xanchor='right',
                                    #   bgcolor='#e5e5e5',
                                    bordercolor='#7f7f7f',
                                    #   borderwidth=2,
                                    # orientation='h',
                                    traceorder='normal'
                                    ),
                                paper_bgcolor = "rgba(0,0,0,0)", plot_bgcolor = "rgba(0,0,0,0)",
                                height=500, width=500, margin=go.layout.Margin(t=20))
        
            fig.update_traces(textinfo='label+percent', textfont_size=20, textfont={'color': '#571c25'}, textposition='outside',)

            st.markdown(htmls.horizontal_line, unsafe_allow_html=True)
            
            if product.total_reviews != 0:
                if product.average_ratings == '0 out of 5':
                    st.error('Not ratings yet.')
                    a, c1, c2, c3, b = st.columns((1,2,2,2,1), gap='small')
                    c2.metric(label='Total Reviews', value=product.total_reviews)
                left, middle, right = st.columns((1.25, 6, 1))
                with middle:
                    st.plotly_chart(fig, use_container_width=True)
                a, c1, c2, c3, b = st.columns((1,2,2,2,1), gap='small')
                
                c1.metric(label='Total Ratings', value=product.total_ratings)
                c2.metric(label='Total Reviews', value=product.total_reviews)
                avg_ratings = product.average_ratings.split()
                c3.metric(label='Average Ratings', value=f"{avg_ratings[0]}/{avg_ratings[-1]}")

                st.markdown(htmls.horizontal_line, unsafe_allow_html=True)
                
                rad_options = ('Yes (this might take more time for larger number of pages)', 'No (to analyse reviews from latest number of pages)')
                print('1', st.session_state.proceed)
                if not st.session_state.proceed:
                    if product.num_pages > 5:
                        # st.markdown(f"### {product.num_pages} pages available. Do you want to run for all pages?")
                        st.markdown(f"""<h3 style="text-align: center;">{product.num_pages} pages available. Do you want to run for all pages?</h3>""", unsafe_allow_html=True)
                        a3, b3, c3 = st.columns((3,2,3))
                        st.session_state.radio_state = b3.radio('Do you want to run for all pages?', rad_options, label_visibility='collapsed')
                        proceed = st.button('Proceed', on_click=change_radio)
                    else:
                        st.session_state.num_pages = product.num_pages
                        st.session_state.proceed = True
                
                num_pages = st.session_state.num_pages

                progress = st.empty()
                with progress.container():
                    if (st.session_state.proceed and not st.session_state.num_pages):
                        # print(f'{st.session_state.radio_state=}')
                        if st.session_state.radio_state == rad_options[1]:
                            st.markdown(f"#### Specify the number of pages to analyze from {product.num_pages} available pages.")
                            page_num = st.number_input('enter the number of pages', value=5, min_value=0, max_value=product.num_pages, label_visibility='collapsed', key='page', on_change=set_page_num, args=('Hold', ))
                            # print(f'{page_num=}, {st.session_state.num_pages=}, {st.session_state.continue_flow=}')
                            st.button('Continue', on_click=set_page_num, args=(True, ))
                            if st.session_state.continue_flow == True:
                                st.session_state.num_pages = page_num
                            else:
                                st.session_state.num_pages = 0
                        else:
                            st.session_state.num_pages = product.num_pages

                num_pages = st.session_state.num_pages
                if st.session_state.proceed and st.session_state.num_pages:
                    i = 1
                    reviews = []
                    with progress.container():
                        bar_header = st.empty()
                        bar = st.progress(0)
                        bar_caption = st.empty()
                    while True:
                        bar_header.write(f"### Total number of pages to fetch {num_pages}")
                        if i == num_pages+1:
                            break
                        print(f'getting reviews from page no. {i}')
                        bar.progress(i/num_pages)
                        bar_caption.caption(f'fetching page number {i}')
                        page_reviews = product.pagination(i)
                        if page_reviews:    
                            reviews.extend(page_reviews)
                        else:
                            continue
                        i+=1

                    bar_header.empty()
                    bar.empty()
                    bar_caption.empty()

                    reviews = [i[0] if len(i) != 0 else '' for i in reviews]
                    reviews_df = pd.DataFrame({'reviews':reviews})
                    reviews_df['reviews'] = reviews_df['reviews'].apply(lambda r: re.sub(r'<.*?>', ' ', r))

                    reviews_df = preprocess(reviews_df)

                    progress.empty()

                    with progress.container():
                        model = st.session_state.model
                        tokenizer = st.session_state.tokenizer

                        with st.spinner('Analyzing all reviews...'):    
                            reviews_list = reviews_df.cleaned_reviews.to_list()
                            reviews_list_encoded = tokenizer.texts_to_sequences(reviews_list)
                            reviews_list_encoded = pad_sequences(reviews_list_encoded, padding='post')
                            predictions = np.argmax(model.predict(reviews_list_encoded), axis=1)
                            mapping = {0:'negative', 1:'mixed', 2:'positive'}
                            reviews_df['sentiment'] = [mapping[i] for i in predictions]
                            sentiment_counts = reviews_df['sentiment'].value_counts().to_dict()

                        positive = sentiment_counts.get('positive', 0)
                        negative = sentiment_counts.get('negative', 0)
                        mixed = sentiment_counts.get('mixed', 0)

                        a, c1, c2, c3, b = st.columns((1,2,2,2,1), gap='small')
                        c1.metric(label='Positive Reviews', value=positive)
                        c2.metric(label='Mixed Reviews', value=mixed)
                        c3.metric(label='Negative Reviews', value=negative)

                        
                        yes = positive + (mixed/2)
                        no = negative + (mixed/2)

                        if yes > no:
                            max = yes
                        else:
                            max = no
                        min = -max

                        a, b, c = st.columns(3)
                        percent = ((yes - no) - min)/(max - min) * 100
                        if percent >= 75:
                            # st.balloons()
                            b.write('## You should buy this product😊')
                        elif percent < 75 and percent >= 25:
                            b.write(f'## You should consider this product {round(percent)}%🤔')
                        else:
                            b.write('## You should not buy this product😔')
                        
                        a, b, c = st.columns(3)

                        with a.expander(f"{positive} Posivive Reviews"):
                            pos_df = reviews_df[reviews_df.sentiment == 'positive'].reset_index()
                            pos_df.index = pos_df.index + 1
                            st.table(pos_df['reviews'])
                        with b.expander(f"{mixed} Mixed Reviews"):
                            mix_df = reviews_df[reviews_df.sentiment == 'mixed'].reset_index()
                            mix_df.index = mix_df.index + 1
                            st.table(mix_df['reviews'])
                        with c.expander(f"{negative} Negative Reviews"):
                            neg_df = reviews_df[reviews_df.sentiment == 'negative'].reset_index()
                            neg_df.index = neg_df.index + 1
                            st.table(neg_df['reviews'])
            elif product.average_ratings != '0 out of 5':
                a, c1, c3, b = st.columns((1,2,2,1), gap='small')
            
                c1.metric(label='Total Ratings', value=product.total_ratings)
                avg_ratings = product.average_ratings.split()
                c3.metric(label='Average Ratings', value=f"{avg_ratings[0]}/{avg_ratings[-1]}")
            else:
                st.error('No ratings or review yet.')

a, b, c, d = st.columns((25,1,1,1))

def get_encoded_img(path):
    with open(path, "rb") as image_file:
        image_base64 = base64.b64encode(image_file.read())
        return image_base64.decode()

b.markdown(f"""<a href='https://www.instagram.com/shivammavihs/'><img style="width:25px; height:25px" src='data:image/png;base64,{get_encoded_img(os.path.join(assets_path, 'instagram.png'))}'></a>""", unsafe_allow_html=True)
c.markdown(f"""<a href='https://github.com/shivammavihs'><img style="width:25px; height:25px" src='data:image/png;base64,{get_encoded_img(os.path.join(assets_path, 'github.png'))}'></a>""", unsafe_allow_html=True)
d.markdown(f"""<a href='linkedin.com/in/shivam-patel-02998488'><img style="width:25px; height:25px" src='data:image/png;base64,{get_encoded_img(os.path.join(assets_path, 'linkedin (1).png'))}'></a>""", unsafe_allow_html=True)

