import os

from flask import Flask, session, render_template, request
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
import configparser
import requests

from models import User, Review


def get_credentials(section, variable):
    parser = configparser.ConfigParser()
    parser.read("resources/credentials.ini", encoding='utf-8')
    return parser.get(section, variable)


app = Flask(__name__)
# Check for environment variable
if not os.getenv("DATABASE_URL"):
    os.environ['DATABASE_URL'] = get_credentials("HEROKU", "uri")

# Set up database
getenv = os.getenv("DATABASE_URL")
engine = create_engine(getenv)
db = SQLAlchemy()
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ['DATABASE_URL']
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

# Configure session to use filesystem
os.environ['FLASK_DEBUG'] = "1"
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


# Goodreads request
# res = requests.get("https://www.goodreads.com/book/review_counts.json",
#                    params={"key": get_credentials("GOODREADS", "key"), "isbns": "9781632168146"})
# print(res.json())

@app.route('/')
def index():
    return render_template('index.html', is_logged_in=is_logged_in())


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = str(request.form.get('input_email'))
        pwd = str(request.form.get('input_password'))
        display_name = str(request.form.get('input_name'))
        if User.query.filter_by(user_email=email).first():
            return render_template('error.html', error_message="This user already exist")
        db.session.add(User(user_email=email, user_password=pwd, user_display_name=display_name))
        print(f"Added new user to the database: {email} {display_name}")
        db.session.commit()
    return render_template('register.html', is_logged_in=is_logged_in())


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('input_email')
        password = request.form.get('input_password')
        result = User.query.filter_by(user_email=email, user_password=password).first()
        if not result:
            return render_template("error.html", error_message="Either wrong email or password. Try again")
        session["logged_in"] = True
    return render_template('login.html')


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    if request.method == 'POST':
        session["logged_in"] = False
    return render_template('logout.html')


def is_logged_in():
    return False if not session["logged_in"] else session["logged_in"]
