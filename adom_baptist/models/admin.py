from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from datetime import datetime

from extensions import db

class Admin(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    profile_pic = db.Column(db.String(255), nullable=True)
    
    # relationship between admin and sermon, members
    sermons = db.relationship('Sermon', backref='admin', lazy=True)
    members = db.relationship('Member', back_populates='admin', cascade="all, delete-orphan")   
    def __repr__(self):
        return f"<Admin {self.username}>"
    
    @property
    def is_admin(self):
        return True


    def get_id(self):
        return f"admin:{self.id}"