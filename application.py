import os

from flask import Flask, session
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
import configparser

app = Flask(__name__)


def get_credentials(variable):
    parser = configparser.ConfigParser()
    parser.read("resources/credentials.ini", encoding='utf-8')
    return parser.get("CONFIG", variable)


# Check for environment variable
if not os.getenv("DATABASE_URL"):
    os.environ['DATABASE_URL'] = get_credentials("config.uri")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))


@app.route("/")
def index():
    return "Project 1: TODO"
