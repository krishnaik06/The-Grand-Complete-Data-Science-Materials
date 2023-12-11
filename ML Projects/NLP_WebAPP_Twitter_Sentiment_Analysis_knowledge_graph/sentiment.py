import re
import pandas as pd
import matplotlib.pyplot as plt
from textblob import TextBlob

# Regex to clean the text
def clean_tweet(tweet):
    # Remove mentions and URLs
    tweet = re.sub(r'@[A-Za-z0-9_]+', '', tweet)
    tweet = re.sub(r'https?://[A-Za-z0-9./]+', '', tweet)
    # Remove special characters and digits
    tweet = re.sub(r'[^\w\s]', '', tweet)
    tweet = re.sub(r'\d+', '', tweet)
    # Remove \n and _
    tweet = re.sub(r'[\n_]', '', tweet)
    # Convert to lowercase
    tweet = tweet.lower()
    return tweet

# Text blob to get polarity and subjectivity
def get_sentiment(tweet):
    analysis = TextBlob(tweet)
    return analysis.sentiment.polarity, analysis.sentiment.subjectivity

# classifying as Positive/Negative Sentiment
def get_sentiment_label(polarity):
    if polarity >= 0:
        return 'positive'
    else:
        return 'negative'

# main function which call every function of the file
def analyze_sentiment(tweets, filename):
    # Creating a dataframe from the tweets list
    df = pd.DataFrame(tweets, columns=['DateTime', 'TweetId', 'Text', 'Username', 'Language', 'Hashtags', 'ReplyCount', 'RetweetCount', 'LikeCount', 'QuoteCount', 'Media'])

    # Clean the tweets
    df['clean_text'] = df['Text'].apply(clean_tweet)

    # Apply sentiment analysis
    df['sentiment_polarity'], df['sentiment_subjectivity'] = zip(*df['clean_text'].apply(get_sentiment))

    # Map polarity values to sentiment labels
    df['sentiment'] = df['sentiment_polarity'].apply(get_sentiment_label)

    df.to_csv(f'{filename}', index=False)

    # Get sentiment counts
    sentiment_counts = df['sentiment'].value_counts()

    # Create a bar plot of the sentiment counts
    plt.bar(sentiment_counts.index, sentiment_counts.values)

    # Set the plot title and axis labels
    plt.title('Sentiment Analysis Results')
    plt.xlabel('Sentiment')
    plt.ylabel('Count')

    # Return the sentiment counts as a dictionary
    return sentiment_counts.to_dict()
