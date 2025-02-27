import os

from flask import Flask, render_template

from dotenv import load_dotenv
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from market import routes

load_dotenv()

DB_USER = os.getenv("MYSQL_DB_USER")
DB_PASSWORD = os.getenv("MYSQL_DB_PASSWORD")
DB_HOST = os.getenv("MYSQL_DB_HOST")
DB_PORT = os.getenv("MYSQL_DB_PORT")
DB_NAME = os.getenv("MYSQL_DB_NAME")
CONNECTOR = os.getenv("MYSQL_CONNECTOR")

FLASK_SECRET_KEY = os.getenv("SECRET_KEY")


SQLALCHEMY_DATABASE_URI = f'mysql+{CONNECTOR}://{
    DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
app.config['SECRET_KEY'] = FLASK_SECRET_KEY

db = SQLAlchemy(app)

bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "login_page"
