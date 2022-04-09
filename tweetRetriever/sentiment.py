from textblob import TextBlob


def get_polarity(text):
    return TextBlob(text).sentiment.polarity


def extract_sentiment(tweets):
    polarity = []
    sentiment = [0, 0, 0]
    for tweet in tweets:
        polarity.append(get_polarity(tweet))

    for score in polarity:
        if score < 0:
            sentiment[2] += 1
        elif score == 0:
            sentiment[1] += 1
        else:
            sentiment[0] += 1

    for i in range(len(sentiment)):
        sentiment[i] = sentiment[i]/len(polarity)

    return sentiment  # percentage of positive, neutral and negative tweets

    
if __name__ == '__main__':
    print(extract_sentiment('Amirul25334053'))

