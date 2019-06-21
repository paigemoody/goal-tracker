from jinja2 import StrictUndefined

from flask import Flask, render_template, redirect, request, flash, session, jsonify, send_file

from flask_debugtoolbar import DebugToolbarExtension

import json

from random import choice

from model import User, Goal, connect_to_db, db

from flask_login import LoginManager, login_user, logout_user, login_required, current_user

from werkzeug.security import generate_password_hash, check_password_hash

import os

app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = os.environ['flask_session_key']

####################################
# Configuration for login handling
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


@login_manager.user_loader
def load_user(user_id):
    """Requirement for flask_login."""

    return User.query.filter(User.user_id == user_id).first()


####################################

@app.route('/')
def index():
    """Homepage."""
    return render_template('login.html')


if __name__ == "__main__":

    app.debug = True
    app.jinja_env.auto_reload = app.debug
    connect_to_db(app)
    app.run(port=5000, host='0.0.0.0')





