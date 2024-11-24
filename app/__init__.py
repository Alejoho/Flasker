import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# from flask_wtf.csrf import CSRFProtect
from dotenv import load_dotenv

load_dotenv()

db = SQLAlchemy()
migrate = Migrate()
# csrf = CSRFProtect()


def create_app():
    app = Flask(__name__)

    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")

    # print(f"SECRET_KEY: {os.environ.get('SECRET_KEY')}")
    # print(f"DATABASE_URL: {os.environ.get('DATABASE_URL')}")

    # app.config.from_object("config.Config")

    db.init_app(app)
    migrate.init_app(app, db)
    # csrf.init_app(app)

    from app.routes import (
        error_routes_bp,
        index_routes_bp,
        name_routes_bp,
        users_routes_bp,
    )

    app.register_blueprint(error_routes_bp, url_prefix="/error")
    app.register_blueprint(index_routes_bp)
    app.register_blueprint(name_routes_bp, url_prefix="/name")
    app.register_blueprint(users_routes_bp, url_prefix="/user")

    return app