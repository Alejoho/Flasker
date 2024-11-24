from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timezone
from app import db


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    date_added = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    favorite_color = db.Column(db.String(120))
    password_hash = db.Column(db.String(162))

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
