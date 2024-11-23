# import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# from flask_wtf.csrf import CSRFProtect
# from dotenv import load_dotenv

# load_dotenv()„

db = SQLAlchemy()
migrate = Migrate()
# csrf = CSRFProtect()


def crate_app():
    app = Flask(__name__)
    # app.config.from_object('config.Config')

    db.init_app(app)
    migrate.init_app(app, db)
    # csrf.init_app(app)

    # import blueprints

    return app
