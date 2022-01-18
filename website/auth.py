from flask import Flask, Blueprint, request, render_template, flash
import re

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    # if request.method == 'GET':
    #     return render_template('login.html')
    # else:
    #     username = request.form.get('username')
    #     password = request.form.get('password')
    #     if username == 'admin' and password == 'admin':
    #         return render_template('index.html')
    #     else:
    return render_template('login.html')


@auth.route('/logout')
def logout():
    return render_template('logout.html')


@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form.get('logemail')
        name = request.form.get('logname')
        password = request.form.get('logpass')
        confirmPass = request.form.get('logpassconfirm')
        regex = '^[a-zA-Z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
        if len(email) < 4:
            flash('Email must be at least 4 characters long', category='error')
        elif not re.search(regex, email):
            flash('Invalid email address', category='error')
        elif len(name) < 2:
            flash('Name must be at least 2 characters long', category='error')
        elif len(password) < 8:
            flash('Password must be at least 8 characters long', category='error')
        elif password != confirmPass:
            flash('Passwords do not match', category='error')
        else:
            flash('Successfully registered', category='success')
            # return render_template('signup.html')
    return render_template('signup.html')
