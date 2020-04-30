import os

from flask import Flask, session, render_template, request
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
import configparser
import requests

app = Flask(__name__)


def get_credentials(section, variable):
    parser = configparser.ConfigParser()
    parser.read("resources/credentials.ini", encoding='utf-8')
    return parser.get(section, variable)


# Check for environment variable
if not os.getenv("DATABASE_URL"):
    os.environ['DATABASE_URL'] = get_credentials("HEROKU", "uri")

# Configure session to use filesystem
os.environ['FLASK_DEBUG'] = "1"
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
getenv = os.getenv("DATABASE_URL")
print(getenv)
engine = create_engine(getenv)
db = scoped_session(sessionmaker(bind=engine))


# Goodreads request
# res = requests.get("https://www.goodreads.com/book/review_counts.json",
#                    params={"key": get_credentials("GOODREADS", "key"), "isbns": "9781632168146"})
# print(res.json())

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        display_name = request.form.get('input_name')
        email = request.form.get('input_email')
        password = request.form.get('input_password')
        if not password == request.form.get('input_repeated_password'):
            print("nope")
        # query = "UPDATE "
        db.execute("SELECT * FROM database")
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html')
