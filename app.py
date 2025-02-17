from flask import Flask, render_template, request, redirect
import os

from werkzeug.security import check_password_hash

from models import User
from service.user_service import create_user
from extensions import db,login_manager
from flask_login import login_user,current_user


app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY") or 'daljkealifeiaj9294'
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'database.db')
db.init_app(app)
login_manager.init_app(app)

with app.app_context():
    db.create_all()

@app.route("/")
def index():

    return render_template("sigin.html",title="サインイン")

@app.route("/-sigin", methods=["POST"])
def index_post():
    data = request.form
    success, message = create_user(data['name'], data["password"])
    if success:
        user = User.query.filter_by(username=data["name"]).first()
        if user:
            login_user(user)  # user.id ではなく user オブジェクトを渡す
            return redirect("/home")
        else:
            return render_template("sigin.html",message=message,title="サインイン")
    else:
        return render_template("sigin.html",message=message,title="サインイン")  # create_user からのエラーメッセージを表示


@app.route("/login")
def login():
    return render_template("login.html",title="ログイン")

@app.route("/-login",methods=["POST"])
def login_post():
    data = request.form
    name = data["name"]
    password = data["password"]
    user = User.query.filter_by(username=name).first()
    remember = True if request.form.get('remember') else False
    if user and check_password_hash(user.password_hash, password):
        login_user(user, remember=remember)
        return redirect("/home")
    else:
        return render_template("login.html", message="ログインに失敗しました",title="ログイン")

@app.route("/home")
def home():
    if current_user.username:
        return render_template("home.html")
    else:
        return render_template("home.html")
if __name__ == "__main__":
    app.run(debug=True)
