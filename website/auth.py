from flask import Blueprint, render_template, request, flash, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from datetime import datetime
#import tensorflow as tf
#import tensorflow_hub as hub
import os

from .models import User
from . import db
from . import gps_locator
from tweetRetriever import sentiment
from tweetRetriever import tweetscraper
#from tweetRetriever import classify

auth = Blueprint('auth', __name__)
#model = tf.keras.models.load_model('./trained_model.h5', custom_objects={'KerasLayer': hub.KerasLayer})

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                
                # scrape user twitter and update db
                twitter_handle = user.twitter_handle
                tweets_list = tweetscraper.get_tweets(twitter_handle[1:], 50)
                
                # Caluclate percentage of fitness tweets using tweet classifier
                #classified_tweet = classify.classify_tweet(model, tweets_list)
                #user.fitness = classify.calculate_fitness(classified_tweet)

                # Calculate sentiment using sentiment analyzer
                sentiment_array = sentiment.extract_sentiment(tweets_list)
                user.positive_post = sentiment_array[0]
                user.neutral_post = sentiment_array[1]
                user.negative_post = sentiment_array[2]

                # Obtain user current location
                lat, lng = gps_locator.current_latlng()
                current_user.latitude = lat
                current_user.longitude = lng

                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')

    return render_template("login.html", user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        twitter_handle = request.form.get('twitterHandle')
        tele_handle = request.form.get('teleHandle')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        age = request.form.get('age')
        gender = request.form.get('gender')
        interests = request.form.getlist('interests[]')
        latitude, longitude = gps_locator.current_latlng()
        fitness = 0.000000
        positive_post = 0.000000
        neutral_post = 0.000000
        negative_post = 0.000000

        user = User.query.filter_by(email=email).first()

        if user:
            flash('Email already exist.', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif len(first_name) < 2:
            flash('First name must be greater than 1 character.', category='error')
        elif len(twitter_handle) < 2:
            flash('Please enter a valid twitter handle', category='error')
        elif len(tele_handle) < 2:
            flash('Please enter a valid telegram handle', category='error')
        elif not age.isdigit():
            flash('Age must be a numerical value.', category='error')
        elif gender == "Select gender":
            flash('Please select your gender.', category='error')
        elif password1 != password2:
            flash('Password don\'t match.', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        else:
            new_user = User(email=email, first_name=first_name, twitter_handle=twitter_handle, tele_handle=tele_handle,
                            password=generate_password_hash(password1, method='sha256'), age=age, gender=gender,
                            interests=interests, latitude=latitude, longitude=longitude, fitness=fitness,
                            positive_post=positive_post, neutral_post=neutral_post, negative_post=negative_post)

            db.session.add(new_user)
            db.session.commit()
            #login_user(new_user, remember=True)
            flash('Account created!', category='success')  # add user to database
            return redirect(url_for('views.home'))

    activity_path = os.path.join(os.getcwd(), "website", "option_list/activity.txt")
    activity_file = open(activity_path, "r")
    activity_list = activity_file.read().split("\n")

    return render_template("sign_up.html", user=current_user, activity_list=activity_list)
