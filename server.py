
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
    goals_dict = json.loads(request.form['goals'])

    updated_goals = []

    for goal in goals_dict:
        if goal != 'new-goal':

            completed = goals_dict[goal]['complete']
            goal_id = goal
            # get goal object 
            goal = Goal.query.filter(Goal.goal_id == goal_id).one()

            if goal.complete != completed:

                goal.complete = completed

                db.session.commit()

                updated_goals.append(goal.goal_title)

    if len(updated_goals) > 0:

        goals_changed_str = ""

        for i in range(0, len(updated_goals)):

            goals_changed_str+= updated_goals[i]

        return f"Updated: {goals_changed_str}"

    else: 
        return "Already up to date!"
    

@app.route('/add_goal', methods=["POST"])
@login_required
def add_goal():
    """Add new goal data to db."""

    goal_title = request.form['title']
    goal_notes = request.form['notes']

    goal = Goal(user_id=current_user.user_id,
                goal_title=goal_title,
                notes = goal_notes
                )
    
    db.session.add(goal)
    db.session.commit()

    return f"Added: {goal_title}!" 

@app.route('/delete_goal', methods=["POST"])
@login_required
def delete_goal():
    """Delete goal data in db."""

    goal_id = request.form['id']

    Goal.query.filter(Goal.goal_id == goal_id).delete()

    db.session.commit()

    return f"Goal deleted!"


@app.route('/edit_goal', methods=["POST"])
@login_required
def edit_goal():
    """Edit existing goal."""

    goal_id = request.form['goalId']
    goal_title = request.form['newTitle']
    goal_notes = request.form['newNotes']

    goal = Goal.query.filter(Goal.goal_id == goal_id).one()

    goal.goal_title = goal_title

    goal.notes = goal_notes

    db.session.commit()

    return f"Updated: {goal_title}!"


if __name__ == "__main__":

    app.debug = True
    app.jinja_env.auto_reload = app.debug
    connect_to_db(app)
    app.run(port=5000, host='0.0.0.0')

