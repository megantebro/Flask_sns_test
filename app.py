import datetime
from crypt import methods

from flask import Flask, render_template, request, redirect,current_app,jsonify
import os

from werkzeug.security import check_password_hash
from models import User,Post,Tag
from service.post_service import create_post
from service.user_service import create_user
import service.user_service as user_service
from extensions import db,login_manager
from flask_login import login_user, current_user, logout_user, login_required
from flask_moment import Moment
from service import feedpost_service,post_service



app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY") or 'daljkealifeiaj9294'
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'database.db')
db.init_app(app)
login_manager.init_app(app)
moment = Moment(app)
with app.app_context():
    db.create_all()

@app.route("/")
def index():
    if current_user.is_authenticated:
        return redirect("home")
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

@app.route("/logout")
def logout():
    logout_user()
    return redirect("/login")

@app.route("/home",methods=["GET"])
@app.route("/home/<int:year>/<int:month>/<int:day>")
@app.route("/home/<int:year>/<int:month>/<int:day>/<string:tag_name>")
def home(year=None,month=None,day=None,tag_name=None):

    if year is None or month is None or day is None:
        current_date = datetime.date.today()
        return redirect(f"/home/{current_date.strftime('%Y/%m/%d')}")
    else:
        current_date = datetime.date(year, month, day)

        # ここで current_date を使用して必要な処理を行う
    user_timeline = feedpost_service.UserTimeLine(user=current_user)
    tags = user_timeline.get_trend(target_date=current_date)
    return render_template('home.html',posts=user_timeline.get_timeline_someday(current_date,tag_name),
                           current_date=current_date,tags=tags)




@app.route("/api/post",methods=['POST'])
@login_required
def do_post():
    data = request.get_json()

    if create_post(headline=data.get('header'),body=data.get('body'),username=data.get('username')):
        current_app.logger.info("正常にpostが作成されました")

    return redirect("/home")

@app.route("/api/post_delete/<int:post_id>",methods=["POST"])
@login_required
def delete_post(post_id):
    current_app.logger.info(post_id)
    post = Post.query.get(post_id)
    post_service.delete_post(post)


@app.route("/api/like_post/<int:post_id>/<int:user_id>",methods=["POST"])
def like_post(post_id,user_id):
    post = Post.query.get(post_id)
    user = User.query.get(user_id)
    if post and user:
        if not user.is_liking(post):
           user_service.like_post(user,post)
        else:
           user_service.unlike_post(user,post)
        return jsonify({'success': True, 'new_like_count': post.like_count()})
    return jsonify({'success': False}), 400


if __name__ == "__main__":
    app.run(debug=True,host="0.0.0.0",port=5001)
