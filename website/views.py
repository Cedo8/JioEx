import os

from flask import Blueprint, jsonify, render_template, request, flash
from flask_login import login_required, current_user
import json

from . import db
from .models import User
from . import gps_locator
from . import scoring

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    return render_template("home.html", user=current_user)


@views.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'POST':
        first_name = request.form.get('first_name')
        twitter_handle = request.form.get('twitter_handle')
        tele_handle = request.form.get('tele_handle')
        age = request.form.get('age')
        message = request.form.get('message')
        additional_interests_string = request.form.get('interests')
        additional_interests = additional_interests_string.split(",")
        if len(additional_interests) == 1 and additional_interests[0] == '':
            additional_interests = []

        if len(first_name) < 2:
            flash('First name must be greater than 1 character.', category='error')
        elif not age.isdigit():
            flash('Age must be a numerical value.', category='error')
        else:
            current_user.first_name = first_name
            current_user.twitter_handle = twitter_handle
            current_user.tele_handle = tele_handle
            current_user.age = int(age)
            current_user.message = message if len(message) > 0 else current_user.message
            if len(additional_interests) > 0:
                for interest in additional_interests:
                    current_user.interests.append(interest)
            db.session.commit()
            flash('Profile updated!', category='success')

    return render_template("profile.html", user=current_user)


@views.route('/jionow', methods=['GET', 'POST'])
@login_required
def jionow():
    # To be updated to take in current location and activity
    if request.method == 'POST':
        activity = request.form.get('activity')
        location = request.form.get('location')

        if activity == 'Select activity type':
            flash('No Activity Chosen', category='error')
        elif location == 'Select Location':
            flash('No Location Chosen', category='error')
        else:
            if location != 'Current Location':
                lat, lng = gps_locator.find_latlng(location)
                update_location(lat, lng)

            if activity != 'Any':
                print(activity)

                users = User.query.filter(User.email != current_user.email).all()

                for usr in users:
                    if activity not in usr.interests:
                        users.remove(usr)
                print(users)
            else:
                users = User.query.filter(User.email != current_user.email).all()
            top10 = scoring.top10(current_user, users)

            return render_template("results.html", user=current_user, user_list=top10)

    lat, lng = gps_locator.current_latlng()
    update_location(lat, lng)
    #current_suburb = gps_locator.find_suburb(lat, lng)

    suburb_path = os.path.join(os.getcwd(), "website", "option_list/suburb.txt")
    suburb_file = open(suburb_path, "r")
    suburb_list = suburb_file.read().split("\n")

    activity_path = os.path.join(os.getcwd(), "website", "option_list/activity.txt")
    activity_file = open(activity_path, "r")
    activity_list = activity_file.read().split("\n")

    return render_template("jionow.html", user=current_user, suburb_list=suburb_list,
                           activity_list=activity_list)


def update_location(lat, lng):
    current_user.latitude = lat
    current_user.longitude = lng
