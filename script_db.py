# Creates the tables from my code in the db

from app import db, app

with app.app_context():
    db.create_all()
