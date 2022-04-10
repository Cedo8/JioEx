import tweepy
import re

bearer_token = ""
client = tweepy.Client(bearer_token)


def clean_tweets(tweet_arr):
    text = []
    for t in tweet_arr:
        cleaned_text = clean_tweet(t.text)
        text.append(cleaned_text)

    return text


def clean_tweet(tweet_text):
    tweet_text = re.sub(r"@[A-Za-z0-9]", "", tweet_text)
    tweet_text = re.sub(r"#", "", tweet_text)
    tweet_text = re.sub(r"RT[\s]", "", tweet_text)
    tweet_text = re.sub(r"https?:\/\/\S+", "", tweet_text)

    return tweet_text


def get_tweets(username, max_num):
    user = client.get_user(username=username)
    user_id = user.data.id
    tweets = client.get_users_tweets(id=user_id, max_results=max_num)

    return clean_tweets(tweets.data)


# for manual annotate classification model
def search_tweets(query, max_no_result):
    if max_no_result < 10:
        max_no_result = 10
    elif max_no_result > 100:
        max_no_result = 100

    tweets = client.search_recent_tweets(query=query, max_results=max_no_result, sort_order='relevancy');
    return clean_tweets(tweets.data)

# testing tweets scraping
# print(get_tweets("harrisssss97", 5))