import os

from dotenv import load_dotenv

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
