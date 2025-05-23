from models import Post,User,Tag
from extensions import db
from flask import current_app
import re

def create_post(headline:str,body:str,username:str,filename:str=None,reply_to_id:int = None):
    try:
        if reply_to_id: reply_to_id = int(reply_to_id)
        user = User.query.filter_by(username=username).first()
        tags = search_tags(body)
        if not filename:
            new_post = Post(user=user,body=body,headline=headline,tags=tags,reply_to_id=reply_to_id)
        else:
            new_post = Post(user=user,body=body,headline=headline,tags=tags,file_path=f"/static/uploads/{filename}",reply_to_id=reply_to_id)
        db.session.add(new_post)
        db.session.commit()
        return True,"正常にポストされました"
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"ポスト作成中にエラーが発生しました{e}")
        return False,"ポスト作成中にエラーが発生しました"


def delete_post(post:Post):
    try:
        db.session.delete(post)
        db.session.commit()
        return True
    except  Exception as e:
        db.session.rollback()
        current_app.logger.error(f"ポスト削除中にエラーが発生しました{e}")
        return False

def search_tags(text:str):
    tags_str = re.findall(r"#(\w+)",text)

    tags = []
    for tag_name in tags_str:
        tag = Tag.query.filter_by(name=tag_name).first()
        if not tag:
            tag = Tag(name=tag_name)
            create_tag(tag)
        tags.append(tag)
    return tags

def create_tag(tag:Tag):
    try:
        db.session.add(tag)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"タグ作成中にエラーが発生しました{e}")


