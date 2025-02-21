from models import User,Post
from datetime import datetime,time,date

class TimelineManager():
    def __init__(self,user:User):
        self.user = user

class UserTimeLine(TimelineManager):
    def get_timeline_someday(self,target_date:date):
        start_of_day = datetime.combine(target_date, time.min)
        end_of_day = datetime.combine(target_date, time.max)

        posts = Post.query.filter(Post.created_at >= start_of_day, Post.created_at < end_of_day).all()

        return posts
