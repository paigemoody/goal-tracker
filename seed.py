from sqlalchemy import func
from model import User, Goal
import datetime
from model import connect_to_db, db
from server import app
import json
from werkzeug.security import generate_password_hash, check_password_hash


def load_users():
    print("USERS")

    # Delete all rows in table, so if we need to run this a second time,
    # we won't be trying to add duplicate users
    User.query.delete()

    # Read u.user file and insert data
    for row in open("seed_data/users"):
        row = row.rstrip()
        user_id, username, password = row.split("|")

        user = User(
            user_id=user_id,
            username=username,
            password=generate_password_hash(password),
        )
        # add to the session
        db.session.add(user)
    # commit data
    db.session.commit()


def load_goals():
    print("GOALS")

    # Delete all rows in table, so if we need to run this a second time,
    # we won't be trying to add duplicate goals
    Goal.query.delete()

    # Read u.user file and insert data
    for row in open("seed_data/goals"):

        row = row.rstrip()

        goal_id, user_id, goal_title, notes = row.split("|")

        goal = Goal(
            goal_id=goal_id, user_id=user_id, goal_title=goal_title, notes=notes
        )

        # add to the session
        db.session.add(goal)

    # commit data
    db.session.commit()


################## AUTO INCREMENT RESET ##################
# resent auto increment to start after highest seed id
def set_val_user_id():
    """Set value for the next user_id after seeding database"""

    # Get the Max user_id in the database
    result = db.session.query(func.max(User.user_id)).one()
    max_id = int(result[0])

    # Set the value for the next user_id to be max_id + 1
    query = "SELECT setval('users_user_id_seq', :new_id)"
    db.session.execute(query, {"new_id": max_id + 1})
    db.session.commit()


def set_val_goal_id():
    """Set value for the next goal_id after seeding database"""

    result = db.session.query(func.max(Goal.goal_id)).one()
    max_id = int(result[0])

    query = "SELECT setval('goals_goal_id_seq', :new_id)"
    db.session.execute(query, {"new_id": max_id + 1})
    db.session.commit()


if __name__ == "__main__":
    connect_to_db(app)

    # In case tables haven't been created, create them
    db.create_all()

    # Import different types of data
    load_users()
    set_val_user_id()

    load_goals()
    set_val_goal_id()
