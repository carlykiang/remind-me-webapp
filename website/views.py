from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, logout_user, current_user
from .models import Note, db, Setting
import json

views = Blueprint('views', __name__)

@views.route('/')
def homepage():
    return render_template("homepage.html", user=current_user)

@views.route('/settings')
def settings():
    return render_template("settings.html", user=current_user)

@views.route('/color', methods=['GET', 'POST'])
@login_required
def color():
    if request.method == 'POST':
        color = request.form.get('color')
        print(color)
        new_color = Setting(color=color, user_id=current_user.id)
        db.session.add(new_color)
        db.session.commit()
        flash('Background changed!', category='success') 
        obj = db.session.query(Setting).order_by(Setting.id.desc()).first()
      
        if color == 'blue':
            hex = "rgb(152, 216, 238)"
        return render_template("home.html", user=current_user, bgcolor = color)



@views.route('/home', methods=['GET', 'POST'])
@login_required
def home():
    
    if request.method == 'POST':
        note = request.form.get('note')
        if len(note) <1:
            flash('Note is too short!', category='error')
        else:
            new_note = Note(text=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Note added!', category='success')
 
    return render_template("home.html", user=current_user)

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