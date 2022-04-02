from unicodedata import category
from flask import Blueprint, jsonify, render_template, request, flash
from flask_login import login_required, current_user
from .models import Note
from .models import User
from . import db
import json

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

    # To be updated to take in current location and activity
    if request.method == 'POST':
        message = request.form.get('message')
        current_user.message = message
        db.session.commit()
        flash('Details Confirmed!', category='success')

        # To add code to send the information to backend for processing
        test_user1 = User(first_name="Test1", age=22, interests=["Swimming", "Dancing"], message="Hi I am Test1.")
        test_user2 = User(first_name="Test2", age=19, interests=["Hiking", "Jogging"], message="Hi I am Test2.")
        current_user.result = [test_user1, test_user2]
        
        # Render the results page instead
        return results()

    return render_template("jionow.html", user=current_user)

@views.route('/results', methods=['GET', 'POST'])
@login_required
def results():
    return render_template("results.html", user=current_user)

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
