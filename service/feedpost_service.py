from models import User,Post,Tag
from datetime import datetime,time,date,timedelta

class TimelineManager():
    def __init__(self,user:User):
        self.user = user

    def fetch_latest_posts(self,amount:int,tag_name:str=None):
        posts:list[Post]
        
        search_day = datetime.today()
        if tag_name:
            posts = self._get_today_posts(search_day,tag_name)
        else:
            posts = self._get_today_posts(search_day)

        search_day = search_day - timedelta(days=1)
        if len(Post.query.filter(Post.reply_to_id.is_(None)).all()) < amount:
            return Post.query.filter(Post.reply_to_id.is_(None)).all()
        else:
            if tag_name and amount > len(Post.query.filter(Post.tags.any(Tag.name == tag_name),Post.reply_to_id.is_(None)).all()): amount = len(Post.query.filter(Post.tags.any(Tag.name == tag_name),Post.reply_to_id.is_(None)).all())
            while len(posts) < amount:
        
                if tag_name:
                    posts += self._get_today_posts(search_day,tag_name)
                else:
                    posts += self._get_today_posts(search_day)
                search_day = search_day - timedelta(days=1)
                
            return posts[:amount]


    def get_trend(self,posts:list[Post]):
        ##tag_likesで指定した日時の
        tag_likes = self._get_tags_likes(posts)
        sorted_tag_likes = dict(sorted(tag_likes.items(),key=lambda x:x[1],reverse=True))
        top_five_tags = dict(list(sorted_tag_likes.items())[:5])
        tags:list[Tag] = []
        for name in top_five_tags:
            tags.append(Tag(name))
        return tags



    def _get_tags_likes(self,posts:list[Post]):
        tag_likes = {}
        ##ポストの中のタグを取得してtag_likesにタグが含まれていたらtag_likesの中に数値をかさんするなかったら新しく
        ##作り投稿のlikesの値を入れる
        for post in posts:
            tags = post.tags
            for tag in tags:
                if tag.name not in tag_likes:
                    tag_likes[tag.name] = 0
                tag_likes[tag.name] += post.like_count()
        return tag_likes



    def _get_today_posts(self,target_date:date = None,tag_name:str=None):

        start_of_day = datetime.combine(target_date,time.min)
        end_of_day = datetime.combine(target_date,time.max)

        if tag_name:
            posts =  Post.query.filter(Post.created_at >= start_of_day,Post.created_at < end_of_day,Post.tags.any(Tag.name == tag_name))
        posts = Post.query.filter(Post.created_at >= start_of_day,Post.created_at < end_of_day)
        return posts.filter(Post.reply_to_id.is_(None)).all()


class UserTimeLine(TimelineManager):
    def get_timeline_someday(self,target_date:date,tag_name:str=None):
        start_of_day = datetime.combine(target_date, time.min)
        end_of_day = datetime.combine(target_date, time.max)

        if tag_name is None:
            posts = Post.query.filter(Post.created_at >= start_of_day, Post.created_at < end_of_day)
        else:
            posts = Post.query.filter(Post.created_at >= start_of_day, Post.created_at < end_of_day)
            posts = posts.filter(Post.tags.any(Tag.name == tag_name))
        return posts.all()


