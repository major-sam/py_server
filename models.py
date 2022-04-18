"""
models.py
- Data classes for the surveyapi application
"""

from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(255), nullable=False)
    account = db.Column(db.String(255),unique=True)
    admin = db.Column(db.Bool)
    enabled = db.Column(db.Bool)
    schID  = db.relationship('Scheduler', backref="user", lazy=False)

    def __init__(self, name, password, email=None, account=None
                 schedulerID=None, admin=False, enabled=True,):
        self.name = name
        self.password = generate_password_hash(password, method='sha256')
        self.email = email
        self.account = account
        self.admin = admin
        self.enabled = enabled
        self.schID = schedulerID
