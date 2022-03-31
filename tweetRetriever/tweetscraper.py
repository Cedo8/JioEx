import tweepy
import re

bearer_token = ""
client = tweepy.Client(bearer_token)


def get_tweets(username, max_num):
    user = client.get_user(username=username)
    user_id = user.data.id
    tweets = client.get_users_tweets(id=user_id, max_results=max_num)

    text = []
    for t in tweets.data:
        cleaned_text = clean_tweets(t.text)
        text.append(cleaned_text)

    return text


def clean_tweets(tweet_text):
    tweet_text = re.sub(r"@[A-Za-z0-9]", "", tweet_text)
    tweet_text = re.sub(r"#", "", tweet_text)
    tweet_text = re.sub(r"RT[\s]", "", tweet_text)
    tweet_text = re.sub(r"https?:\/\/\S+", "", tweet_text)

    return tweet_text
