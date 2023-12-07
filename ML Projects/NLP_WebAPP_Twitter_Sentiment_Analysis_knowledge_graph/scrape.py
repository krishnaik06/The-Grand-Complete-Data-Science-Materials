import datetime
import pandas as pd
import snscrape.modules.twitter as sntwitter
from tqdm(total=count) import tqdm_notebook

def scrape_tweets(text, username, since, until, count, retweet, replies):
    # Define a function to search for tweets using snscrape
    def search(text, username, since, until, retweet, replies):
        global filename
        q = text
        if username != '':
            q += f" from:{username}"
        if until == '':
            until = datetime.datetime.strftime(datetime.date.today(), '%Y-%m-%d')
            q += f" until:{until}"
        if since == '':
            since = datetime.datetime.strftime(datetime.datetime.strptime(until, '%Y-%m-%d') - datetime.timedelta(days=365), '%Y-%m-%d')
            q += f" since:{since}"
        if retweet == 'y':
            q += f" exclude:retweets"
        if replies == 'y':
            q += f" exclude:replies"
        if username != '' and text != '':
            filename = f"{since}_{until}_{username}_{text}.csv"
        elif username != "":
            filename = f"{since}_{until}_{username}.csv"
        else:
            filename = f"{since}_{until}_{text}.csv"
            print(filename)
        return q

    q = search(text,username,since,until,retweet,replies)

    # Creating list to append tweet data
    tweets_list1 = []
    # Using TwitterSearchScraper to scrape data and append tweets to list
    if count == -1:
        for i, tweet in enumerate(tqdm_notebook(sntwitter.TwitterSearchScraper(q).get_items())):
            # Check if tweet is in English
            if tweet.lang == 'en':
                tweets_list1.append([tweet.date, tweet.id, tweet.content, tweet.user.username, tweet.lang, tweet.hashtags, tweet.replyCount, tweet.retweetCount, tweet.likeCount, tweet.quoteCount, tweet.media])
    else:
        with tqdm_notebook(total=count) as pbar:
            for i, tweet in enumerate(sntwitter.TwitterSearchScraper(q).get_items()):
                if i >= count:
                    break
                # Check if tweet is in English
                if tweet.lang == 'en':
                    tweets_list1.append([tweet.date, tweet.id, tweet.content, tweet.user.username, tweet.lang, tweet.hashtags, tweet.replyCount, tweet.retweetCount, tweet.likeCount, tweet.quoteCount, tweet.media])
                pbar.update(1)
    # Creating a dataframe from the tweets list above
    df = pd.DataFrame(tweets_list1, columns=['DateTime', 'TweetId', 'Text', 'Username', 'Language', 'Hashtags', 'ReplyCount', 'RetweetCount', 'LikeCount', 'QuoteCount', 'Media'])
    
    '''# Save the DataFrame with the scraped tweets to an Excel file
    df.to_csv(f'{filename}.csv', index=False)'''

    # Return the DataFrame with the scraped tweets
    return df, filename


