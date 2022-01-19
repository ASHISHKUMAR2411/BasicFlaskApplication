from flask import Flask, Blueprint, request, render_template, flash, redirect, url_for, session
import re
from .models import User, Note
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, logout_user, login_required, current_user

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    try :
        boolean = session['boolean']
        if boolean == True:
            flash('You are already logged in', category='success')
            return render_template("profile.html")
    except:
        pass
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        print(email, password)
        user = User.query.filter_by(email=email).first()
        print(user)
        if user:
            if check_password_hash(user.password, password):
                flash('You are Succesfully logged in!', category='success')
                login_user()
                session['boolean'] = True
                return redirect(url_for('auth.notes'))
            else:
                flash('Incorrect password, Try Again ', category='error')
                return redirect(url_for('auth.login'))
        else:
            flash('User does not exist, Try Making an account', category='error')
            return redirect(url_for('auth.signup'))
    return render_template('login.html')


@auth.route('/logout')
def logout():
    session.pop('boolean', None)
    return render_template('logout.html')


@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    try :
        boolean = session['boolean']
        if boolean == True:
            flash('You are already logged in', category='success')
            return render_template("profile.html")
    except:
        pass
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
            flash('Successfully registered', category='success')
            return redirect(url_for('auth.login'))
    return render_template('signup.html')


@auth.route("/notes")
def notes():
    try :
        boolean = session['boolean']
        if boolean == True:
            return render_template("notes.html")
    except:
        return redirect(url_for('auth.login'))
    # the function can provide text, html or json anything to render on the website


# @auth.route('/notes')
# def notes():
#     notes = Note.query.all()
#     return render_template('notes.html', notes=notes)
