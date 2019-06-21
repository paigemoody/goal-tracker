from flask import Flask

from flask_sqlalchemy import SQLAlchemy

from werkzeug.security import generate_password_hash, check_password_hash

import datetime 

db = SQLAlchemy()

##############################################################################
# Model definitions

class User(db.Model):
    """User info"""

    def __repr__(self): 
        """provide helpful represeation for user."""

        return f"<User user_id={self.user_id}>"

    __tablename__ = "users"

    user_id  = db.Column(db.Integer, autoincrement=True, primary_key=True)
    username = db.Column(db.String(100), nullable=False)    
    password = db.Column(db.String(128), nullable=False)

    # Flask-Login integration
    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.user_id

class Goal(db.Model):
    """Individual goals"""

    def __repr__(self):
        """provide helpful represeation for goal."""
        return f"<User user_id={self.goal_title}>"

    __tablename__ = "goals"

    goal_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    goal_title = db.Column(db.String(100))
    notes = db.Column(db.String(500))
    complete = db.Column(db.Boolean, nullable=False, default=False)
    created_date = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)

    # define relationship with user table 
    user = db.relationship("User",
                           backref=db.backref("goals"))

##############################################################################
# Helper functions


def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our PstgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///goal_tracker'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_ECHO'] = True
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from server import app
    connect_to_db(app)
    print("Connected to DB.")

