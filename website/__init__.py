# as this file make the website a package, and now we can write function and class to import them
from flask import Flask
import os
from dotenv import load_dotenv, find_dotenv
from flask_sqlalchemy import SQLAlchemy
load_dotenv(find_dotenv())
# to load our credential we have use dotenv package for our website

db = SQLAlchemy()
DB_NAME = os.getenv('DB_NAME')
secret_key = os.getenv('SECRET_KEY')
# print(secret_key)


def create_app():
    # here Flask(__name__) means whenever Flask is called it takes the name of the place where it is called
    app = Flask(__name__)

    # Here app.config() is using secret_key for Encrypting the cookies and password
    app.config['SECRET_KEY'] = secret_key
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)
    from .views import views
    from .auth import auth
    # now register the Blueprints for app to regonise
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    # return app with taking __name__ from where it was called
    return app
