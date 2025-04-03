import datetime
import time

from sqlalchemy import Table, Column, Integer, ForeignKey
from werkzeug.security import generate_password_hash,check_password_hash
from extensions import db
from flask_login import UserMixin
from flask import current_app
post_tags = Table('post_tags',db.Model.metadata,
                  Column("post_id",Integer,ForeignKey('post.id')),
                        Column('tag_id',Integer,ForeignKey('tag.id')))

class User (UserMixin,db.Model):
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(20),unique=True,nullable=False)
    password_hash = db.Column(db.String(30))
    posts = db.relationship("Post",back_populates='user')
    likes = db.relationship('Like',back_populates="user",cascade="all,delete-orphan")

    def is_liking(self,post):
        return Like.query.filter_by(user_id=self.id,post_id=post.id).first() is not None

    def set_password(self,password):
        self.password_hash = generate_password_hash(password)

    def check_password(self,password):
        return check_password_hash(self.password_hash,password)

class Post(db.Model):

    id = db.Column(db.Integer,primary_key=True)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'))
    user = db.relationship("User",back_populates="posts")
    headline = db.Column(db.String(30))
    body = db.Column(db.String(300))
    created_at = db.Column(db.DateTime,default=datetime.datetime.utcnow())
    file_path = db.Column(db.String(255))
    tags = db.relationship('Tag',secondary=post_tags,back_populates='posts')
    likes = db.relationship('Like',back_populates='post',cascade='all,delete-orphan')


    def like_count(self):
        return len(self.likes)

    def is_liked_by(self,user):
        return Like.query.filter_by(user_id=user.id,post_id=self.id).first() is not None

    def __init__(self,headline,body,user,file_path=None,tags=None):
        self.headline = headline
        self.body = body
        self.user = user
        self.file_path = file_path
        self.tags = tags

class Tag(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(50),unique=True,nullable=False)
    posts = db.relationship('Post',secondary='post_tags',back_populates='tags')

    def __init__(self,name:str):
        self.name = name

class Like(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id',ondelete='CASCADE'),nullable=False)
    post_id = db.Column(db.Integer,db.ForeignKey('post.id',ondelete='CASCADE'),nullable=False)
    created_at = db.Column(db.DateTime,default = datetime.datetime.utcnow())

    user = db.relationship("User",back_populates='likes')
    post = db.relationship("Post",back_populates='likes')

class File(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    file_name = db.Column(db.String(30))



