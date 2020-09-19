from . import db
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from datetime import DateTime

class User(db.Model):
    __tablename__ = 'user'

    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    posts = relationship("Post", back_populates="user")

    def __init__(self, username, password_hash):
        self.username = username
        self.password_hash = password_hash

    def __repr__(self):
        return '<username {}>'.format(self.username)

class Post(db.Model):
    __tablename__ = 'post'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    author_id = db.Column(db.Integer, ForeignKey('user.user_id', ondelete='CASCADE'), nullable=False)
    user = relationship("User", back_populates="posts")
    title = db.Column(db.String(), nullable=False)
    body = db.Column(db.String(), nullable=False)
    created = db.Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    def __init__(self, title, body):
        self.title = title
        self.body = body

    def __repr__(self):
        return '<id {}>'.format(self.id)