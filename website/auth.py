from flask import Blueprint, render_template, request, flash, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from datetime import datetime

from .models import User
from . import db
import gps_locator

auth = Blueprint('auth', __name__)


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

                # last scrape the user twitter(scrape once a week)

                # now = datetime.now() --> add this info to user db

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
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        age = request.form.get('age')
        gender = request.form.get('gender')
        interests_string = request.form.get('interests')
        interests = interests_string.split(",")
        lat, lng = gps_locator.current_latlng()
        latitude = lat
        longitude = lng
        sporty_post = 0.000000
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
        elif not age.isdigit():
            flash('Age must be a numerical value.', category='error')
        elif gender == "Select gender":
            flash('Please select your gender.', category='error')
        elif password1 != password2:
            flash('Password don\'t match.', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        else:
            new_user = User(email=email, first_name=first_name, twitter_handle=twitter_handle,
                            password=generate_password_hash(password1, method='sha256'), age=age, gender=gender,
                            interests=interests, latitude=latitude, longitude=longitude, sporty_post=sporty_post,
                            positive_post=positive_post, neutral_post=neutral_post, negative_post=negative_post)

            db.session.add(new_user)
            db.session.commit()
            # login_user(user, remember=True)
            flash('Account created!', category='success')  # add user to database
            return redirect(url_for('views.home'))

    return render_template("sign_up.html", user=current_user)
