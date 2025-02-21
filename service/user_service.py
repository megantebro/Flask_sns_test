from models import User,Post,Like
from extensions import db, login_manager
from flask_login import LoginManager
from flask import current_app

def create_user(username, password):
    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        return False, "ユーザー名は既に使用されています"
    try:
        new_user = User(username=username)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        return True, "ユーザーが正常に作成されました"
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"ユーザー作成中にエラーが発生しました{e}")
        return False, f"ユーザー作成中にエラーが発生しました: {str(e)}"

def like_post(user:User,post:Post):
    if not user.is_liking(post=post):
        like = Like(user_id=user.id,post_id=post.id)
        try:
            db.session.add(like)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            current_app.logger.error("いいね登録中にエラーが発生しました" + str(e))

def unlike_post(user:User,post:Post):
    like = Like.query.filter_by(user_id=user.id,post_id=post.id).first()
    try:
        if like:
            db.session.delete(like)
            db.session.commit()
    except Exception as e:
        db.session.rollback()
        current_app.logger.error("いいね解除中にエラーが発生しました" + str(e))


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

