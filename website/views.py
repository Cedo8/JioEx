from unicodedata import category
from flask import Blueprint, jsonify, render_template, request, flash
from flask_login import login_required, current_user
from .models import Note
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
        message = request.form.get('message')
        current_user.message = message
        print(current_user.message)
        db.session.commit()
        flash('Profile updated!', category='success')

    return render_template("profile.html", user=current_user)

@views.route('/jionow', methods=['GET', 'POST'])
@login_required
def jionow():
    if request.method == 'POST':
        message = request.form.get('message')
        current_user.message = message
        db.session.commit()
        flash('Details Confirmed!', category='success')

    return render_template("jionow.html", user=current_user)

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
