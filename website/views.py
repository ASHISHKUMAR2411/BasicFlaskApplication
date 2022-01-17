from flask import Blueprint, render_template, request, redirect, url_for, flash
# A blueprint is an object that allows defining application functions without requiring an application object ahead of time.

views = Blueprint("views", __name__)
# views is like an object of the views which aloow render any function inside views.py


# Then we route the app to given url to render the content inside the given function
@views.route("/")
def home():
    # the function can provide text, html or json anything to render on the website
    return render_template("home.html")

