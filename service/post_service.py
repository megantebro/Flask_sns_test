from models import Post,User
from extensions import db
from flask import current_app

def create_post(headline:str,body:str,username:str,file=None):
    try:
        user = User.query.filter_by(username=username).first()
        new_post = Post(user=user,body=body,headline=headline)
        db.session.add(new_post)
        db.session.commit()
        return True,"正常にポストされました"
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"ポスト作成中にエラーが発生しました{e}")
        return False,"ポスト作成中にエラーが発生しました"
