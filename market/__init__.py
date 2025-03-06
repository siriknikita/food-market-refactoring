# market/__init__.py
from flask import Flask, render_template

from market.blueprints import blueprints
from market.constants import FLASK_SECRET_KEY, SQLALCHEMY_DATABASE_URI
from market.extensions import db, bcrypt, login_manager  # Import from extensions

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
app.config['SECRET_KEY'] = FLASK_SECRET_KEY

db.init_app(app)
bcrypt.init_app(app)
login_manager.init_app(app)
login_manager.login_view = "auth.login_page"

for blueprint in blueprints:
    app.register_blueprint(blueprint, url_prefix="/{}".format(blueprint.name))
