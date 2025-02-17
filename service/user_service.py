from models import User
from extensions import db, login_manager
from flask_login import LoginManager

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
        return False, f"ユーザー作成中にエラーが発生しました: {str(e)}"



@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

