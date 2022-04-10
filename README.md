# JioEx
JioEx is a location-based application that helps to connect users with other nearby sports enthusiasts who are looking for someone to exercise with, with the intention of keeping users motivated in their exercise goals.

### Description
The application recommends exercise buddies to users based on features, such as location proximity, common interests, free time, current fitness level and future fitness goals. A messaging interface is also available for connected users to get to know each other better and initiate meet ups. 

The main goal of the project is to develop a robust matching algorithm that allows us to classify users and pair up potentially compatible candidates based on a set of features, including (but not limited to) users’ background, personality, interests and preferences.

### Target Users
Formally, the target users of JioEx are sports enthusiasts who are looking for people to exercise with. However, we believe that this application can be used by anyone who wants to exercise, regardless of their fitness level or their frequency of workouts.

## Running the website locally
- Ensure you have a python virtual environment of your choice like `pyenv` or `Anaconda`.
- Activate your virtual environment.
- In virtual environment `(venv)`, install dependencies with: `pip install -r requirements.txt`
- Get your Bearer Token from [twitter developer](https://developer.twitter.com/) and input into line 4 of the tweetRetriever/tweetscraper.py
- Proceed to download the [tweet classification model](https://drive.google.com/file/d/1QNvlZu_3Kf4cRwVmPx7Z3nhCmh_ItJEN/view?usp=sharing)
- Place the model into the tweetRetriever folder.
- In virtual environment `(venv)`, to run python backend server: `python3 main.py`

Server runs by default at http://127.0.0.1:5000/

### Resources
* [tweepy](https://github.com/tweepy/tweepy), a library for Twitter
