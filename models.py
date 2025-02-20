import datetime
import time
from sqlalchemy import Table, Column, Integer, ForeignKey
from werkzeug.security import generate_password_hash,check_password_hash
from extensions import db
from flask_login import UserMixin

post_tags = Table('post_tags',db.Model.metadata,
                  Column("post_id",Integer,ForeignKey('post.id')),
                        Column('tag_id',Integer,ForeignKey('tag.id')))

class User (UserMixin,db.Model):
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(20),unique=True,nullable=False)
    password_hash = db.Column(db.String(30))
    posts = db.relationship("Post",back_populates='user')

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

    def __init__(self,headline,body,user,file_path=None):
        self.headline = headline
        self.body = body
        self.user = user
        self.file_path = file_path

class Tag(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(50),unique=True,nullable=False)
    posts = db.relationship('Post',secondary='post_tags',back_populates='tags')

