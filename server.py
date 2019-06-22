
from model import User, Goal, connect_to_db, db

from flask import Flask, render_template, redirect, request, flash, session, jsonify, send_file
from flask_debugtoolbar import DebugToolbarExtension
from flask_login import LoginManager, login_user, logout_user, login_required, current_user

from werkzeug.security import generate_password_hash, check_password_hash
from jinja2 import StrictUndefined

import json
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
    return redirect('/login')

@app.route('/login')
def get_login():
    """Display login page."""

    # if logged in, send to goals dashboard
    if current_user.is_authenticated: 
        return redirect('/goals')

    # if not logged in show login
    else: 
        return render_template("login.html")


@app.route('/login_submission', methods=['POST'])
def login_sub():
    """Process login."""

    username = request.form.get('username')
    password = request.form.get('password')

    user = User.query.filter(User.username == username).first()
    if user:

        if check_password_hash(user.password, password):

            user.is_authenticated = True 

            login_user(user)

            flash(f'Welcome {user.username}!') 

            return redirect(f"/goals") 

    flash('Wrong username and/or password')

    return redirect('/login')

@app.route("/logout")
@login_required
def logout():

    logout_user()

    return redirect('/login')

@app.route("/register", methods=["POST"])
def register_process():
    """Processes registration request."""
    username=request.form['username']
    password=request.form['password']

    old_user_username = User.query.filter(User.username == username).first()

    # try to get user associated with email from database

    # if username is taken, tell user and send them back to the login page
    if old_user_username:
        flash(f'Bummer .... {username} already taken!')
        return redirect('/login')
    else:
        # make a new user object with email, username and pw
        new_user = User(username=username,password=generate_password_hash(password))

        # add database changes to staging  
        db.session.add(new_user)
        # commit db changes 
        db.session.commit()

        user = User.query.filter(User.username == username).first()

        user.is_authenticated = True 

        login_user(user)
        flash(f'Welcome {user.username}!')
        return redirect('/goals')

    

@app.route('/goals')
@login_required
def get_user_goals():
    """Goal dashboard."""
    return render_template('goal_dashboard.html')


@app.route('/save_goals', methods=["POST"])
@login_required
def save_goals():
    """Update and save goals data to db."""

    user_id = request.form['userId']

    print("\n\nuser:", user_id)

    goals_dict = json.loads(request.form['goals'])

    print(goals_dict)

    print(f"\n\n\n\nsaving {user_id}'s goals")

    return "OK!"

if __name__ == "__main__":

    app.debug = True
    app.jinja_env.auto_reload = app.debug
    connect_to_db(app)
    app.run(port=5000, host='0.0.0.0')





