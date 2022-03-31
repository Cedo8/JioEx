import tweepy

bearer_token = ""
client = tweepy.Client(bearer_token)


def get_tweets(username, max_num):
    user = client.get_user(username=username)
    user_id = user.data.id
    tweets = client.get_users_tweets(id=user_id, max_results=max_num)
    return tweets
