# Welcome Boss!
from flask import Flask, render_template, request, redirect
import os
import pandas as pd
import matplotlib.pyplot as plt
import base64
from io import BytesIO
from wordcloud import WordCloud
import snscrape.modules.twitter as sntwitter
from tqdm.notebook import tqdm_notebook
import datetime
import re
from textblob import TextBlob
from scrape import scrape_tweets
from sentiment import analyze_sentiment

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/result', methods=['POST', 'GET'])
def result():
    if request.method == 'POST':
        # Get the form data
        text = request.form['text']
        username = request.form['username']
        since = request.form['since']
        until = request.form['until']
        count = request.form['count']
        retweet = request.form.get('retweet','n')
        replies = request.form.get('replies','n')

        # Scrape the tweets
        tweets,filename = scrape_tweets(text, username, since, until, int(count), retweet, replies)

        # Analyze the sentiment
        sentiment_counts = analyze_sentiment(tweets, filename)

        # Read the CSV file into a pandas DataFrame
        data = pd.read_csv(f'{filename}')
        first_five = data.head()
        last_five = data.tail()
        count_df = data.shape[0]
        sentiment_counts = data['sentiment'].value_counts()

        # Create a figure with three subplots
        fig, axs = plt.subplots(1, 4, figsize=(20,5))
        
        # Create a bar chart of the sentiment counts in the first subplot
        axs[0].bar(sentiment_counts.index, sentiment_counts.values)
        axs[0].set_title('Sentiment Analysis Results')
        axs[0].set_xlabel('Sentiment')
        axs[0].set_ylabel('Count')
        
        # Generate a word cloud from the positive tweets in the second subplot
        positive_df = data[data['sentiment'] == 'positive']
        text = ' '.join(positive_df['clean_text'].tolist())
        wordcloud_p = WordCloud(width=800, height=800, background_color='white').generate(text)
        axs[1].imshow(wordcloud_p, interpolation='bilinear')
        axs[1].set_title('Positive Word Cloud')
        axs[1].axis('off')
        
        # Generate a word cloud from the negative tweets in the third subplot
        negative_df = data[data['sentiment'] == 'negative']
        text = ' '.join(negative_df['clean_text'].tolist())
        wordcloud_n = WordCloud(width=800, height=800, background_color='white').generate(text)
        axs[2].imshow(wordcloud_n, interpolation='bilinear')
        axs[2].set_title('Negative Word Cloud')
        axs[2].axis('off')
        
        # Create a pie chart of the sentiment counts
        axs[3].pie(sentiment_counts.values, labels=sentiment_counts.index, autopct='%1.1f%%')
        axs[3].set_title('Sentiment Analysis Results')
        

        # Save the figure as a base64-encoded string
        buffer = BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        plot_url = base64.b64encode(buffer.getvalue()).decode()

        # Render the result template with the sentiment counts and the URLs of the bar chart, pie chart, and word cloud
        return render_template('result.html', first_five=first_five, last_five=last_five,  sentiment_counts=sentiment_counts, result=count_df, plot_url=plot_url)
    else:
        return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
