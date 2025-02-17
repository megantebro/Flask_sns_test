
from werkzeug.security import generate_password_hash,check_password_hash
from extensions import db
from flask_login import UserMixin

class User (UserMixin,db.Model):
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(20),unique=True,nullable=False)
    password_hash = db.Column(db.String(30))

    def set_password(self,password):
        self.password_hash = generate_password_hash(password)

    def check_password(self,password):
        return check_password_hash(self.password_hash,password)
    

class Post(db.Model):
    user = db.Column(db.User)