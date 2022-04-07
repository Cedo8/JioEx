import csv
from tweetscraper import search_tweets
from langdetect import detect
from langdetect import DetectorFactory

DetectorFactory.seed = 0

search_terms = ["fitness", "sports", "workout", "exercise", "run", "jog", "swim", "sweat", "diet", "gym", "weight", "bulk", "reps", "protein", "health", "hiking", "basketball", "football"]

if __name__ == '__main__':
    with open('tweetRetriever\dataset2.csv', 'w', encoding='UTF-8', newline='') as f:
        writer = csv.writer(f)
        recorded_tweets = set()
        index = 1
        writer.writerow(["id", "Keyword", "Tweet", "Target"])
        for term in search_terms:
            tweets = search_tweets(term, 100)
            for t in tweets:
                t = t.encode("ascii", "ignore").decode()
                try:
                    if t not in recorded_tweets and len(t) > 3 and detect(t) == 'en':
                        writer.writerow([str(index), term, t])
                        recorded_tweets.add(t)
                        index += 1
                except:
                    continue
