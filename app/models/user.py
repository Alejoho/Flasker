from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timezone
from app import db
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from typing import Optional


class User(db.Model, UserMixin):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(20), nullable=False, unique=True)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    email: Mapped[str] = mapped_column(String(120), nullable=False, unique=True)
    date_added: Mapped[datetime] = mapped_column(default=datetime.now())
    favorite_color: Mapped[Optional[str]] = mapped_column(String(120))
    password_hash: Mapped[str] = mapped_column(String(162))

    @property
    def password(self):
        raise AttributeError("password is not accesible")

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self) -> str:
        return f"<Name {self.name}>"


# class User(db.Model, UserMixin):
#     __tablename__ = "users"
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(20), nullable=False, unique=True)
#     name = db.Column(db.String(200), nullable=False)
#     email = db.Column(db.String(120), nullable=False, unique=True)
#     date_added = db.Column(db.DateTime, default=datetime.now(timezone.utc))
#     favorite_color = db.Column(db.String(120))
#     password_hash = db.Column(db.String(162))

#     @property
#     def password(self):
#         raise AttributeError("password is not accesible")

#     @password.setter
#     def password(self, password):
#         self.password_hash = generate_password_hash(password)

#     def verify_password(self, password):
#         return check_password_hash(self.password_hash, password)

#     def __repr__(self) -> str:
#         return f"<Name {self.name}>"
