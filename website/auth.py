from flask import Flask, Blueprint, jsonify, request, render_template, flash, redirect, url_for, session
import re
from .models import User, Note
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, logout_user, login_required, current_user
import json


auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    # try :
    #     boolean = session['boolean']
    #     if boolean == True:
    #         flash('You are already logged in', category='success')
    #         return render_template("profile.html")
    # except:
    #     pass
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('You are Succesfully logged in!', category='success')
                login_user(user, remember = True)
                
                # session['boolean'] = True
                return redirect(url_for('auth.notes'))
            else:
                flash('Incorrect password, Try Again ', category='error')
                return redirect(url_for('auth.login'))
        else:
            flash('User does not exist, Try Making an account', category='error')
            return redirect(url_for('auth.signup'))
    return render_template('login.html', user=current_user)


@auth.route('/logout')
@login_required
def logout():
    # need to show pop up for asking for confirmation
    logout_user()
    # session.pop('boolean', None)
    return redirect(url_for('auth.login'))


@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    # try :
    #     boolean = session['boolean']
    #     if boolean == True:
    #         flash('You are already logged in', category='success')
    #         return render_template("profile.html")
    # except:
    #     pass
    if request.method == 'POST':
        logemail = request.form.get('logemail')
        logname = request.form.get('logname')
        logpass = request.form.get('logpass')
        logpassconfirm = request.form.get('logpassconfirm')
        regex = '^[a-zA-Z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
        user = User.query.filter_by(email=logemail).first()
        if user:
            flash('User already exists, Try Logging in ', category='error')
        elif len(logemail) < 4:
            flash('Email must be at least 4 characters long', category='error')
        elif not re.search(regex, logemail):
            flash('Invalid email address', category='error')
        elif len(logname) < 2:
            flash('Name must be at least 2 characters long', category='error')
        elif len(logpass) < 8:
            flash('Password must be at least 8 characters long', category='error')
        elif logpass != logpassconfirm:
            flash('Passwords do not match', category='error')
        else:
            db.create_all()
            new_user = User(first_name=logname, email=logemail, password=generate_password_hash(logpass, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(user, remember = True)
            flash('Successfully registered', category='success')
            return redirect(url_for('auth.login'))
    return render_template('signup.html', user=current_user)


@auth.route("/notes", methods=['GET', 'POST'])
@login_required
def notes():
    if request.method == 'POST':
        note = request.form.get('note')
        if len(note) < 1:
            flash('Note must be at least 1 character long', category='error')
        else:
            new_note = Note(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Note added', category='success')
            return redirect(url_for('auth.notes'))
    return render_template("notes.html", user=current_user)
    # try :
    #     boolean = session['boolean']
    #     if boolean == True:
    #         return render_template("notes.html")
    # except:
        # return redirect(url_for('auth.login'))
    # the function can provide text, html or json anything to render on the website

@auth.route("/profile")
@login_required
def profile():
    return render_template("profile.html", user=current_user);


# @auth.route('/notes')
# def notes():
#     notes = Note.query.all()
#     return render_template('notes.html', notes=notes)
@auth.route('/delete-note', methods=['POST'])
def delete_node():
    note = json.loads(request.data)
    noteID = note['noteId']
    note = Note.query.get(noteID)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()
            flash('Note deleted', category='success')
    return jsonify({})
