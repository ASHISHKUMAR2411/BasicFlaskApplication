from flask import Blueprint, render_template
from flask_login import current_user
# A blueprint is an object that allows defining application functions without requiring an application object ahead of time.

views = Blueprint("views", __name__)
# views is like an object of the views which aloow render any function inside views.py


# Then we route the app to given url to render the content inside the given function
@views.route("/")
def home():
    # try:
    #     boolean = session['boolean']
    #     if boolean == True:
    #         session.pop("boolean", None)
    # except:
    #     pass
    # the function can provide text, html or json anything to render on the website
    return render_template("home.html", user=current_user)

