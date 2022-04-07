from unicodedata import category
from flask import Blueprint, jsonify, render_template, request, flash
from flask_login import login_required, current_user
import json

from .models import Note
from . import db
from .models import User
from . import gps_locator
from . import scoring

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        note = request.form.get('note')

        if len(note) < 1:
            flash('Note is too short!', category='error')
        else:
            new_note = Note(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Note added!', category='success')

    return render_template("home.html", user=current_user)

@views.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'POST':
        first_name = request.form.get('first_name')
        twitter_handle = request.form.get('twitter_handle')
        age = request.form.get('age')
        message = request.form.get('message')
        additional_interests_string = request.form.get('interests')
        additional_interests = additional_interests_string.split(",")

        if len(first_name) < 2:
            flash('First name must be greater than 1 character.', category='error')
        elif not age.isdigit():
            flash('Age must be a numerical value.', category='error')
        elif len(message) < 2:
            flash('Message must contain more than 1 character.', category='error')
        else:
            current_user.first_name = first_name
            current_user.twitter_handle = twitter_handle
            current_user.age = int(age)
            current_user.message = message
            for interest in additional_interests:
                current_user.interests.append(interest)
            db.session.commit()
            flash('Profile updated!', category='success')
        
    return render_template("profile.html", user=current_user)

@views.route('/jionow', methods=['GET', 'POST'])
@login_required
def jionow():
    if request.method == 'POST':
        activity = request.form.get('activity')
        users = User.query.filter(User.interests.contains([activity])).all()
        top10 = scoring.top10(current_user, users)

        return render_template("result.html", top10)

        message = request.form.get('message')
        current_user.message = message
        db.session.commit()
        flash('Details Confirmed!', category='success')

    lat, lng = gps_locator.current_latlng()
    current_user.latitude = lat
    current_user.longitude = lng
    current_suburb = gps_locator.find_suburb(lat, lng)

    return render_template("jionow.html", user=current_user, suburb=current_suburb)

@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()
    
    return jsonify({})
