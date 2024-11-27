from app import db
from datetime import datetime
from sqlalchemy import String, Text, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column


class Post(db.Model):
    __tablename__ = "posts"
    id = mapped_column(Integer, primary_key=True)
    title = mapped_column(String(255))
    content = mapped_column(Text)
    # author = mapped_column(String(255))
    date_posted: Mapped[datetime] = mapped_column(default=datetime.now())
    slug = mapped_column(String(255))

    user_id = mapped_column(Integer, ForeignKey("users.id"), nullable=False)


# class Post(db.Model):
#     __tablename__ = "posts"
#     id = db.Column(db.Integer, primary_key=True)
#     title = db.Column(db.String(255))
#     content = db.Column(db.Text)
#     author = db.Column(db.String(255))
#     date_posted = db.Column(db.DateTime, default=datetime.now())
#     slug = db.Column(db.String(255))
