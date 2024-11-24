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


def create_app():
    app = Flask(__name__)
    # app.config.from_object('config.Config')

    from my_secrets import My_Secrets

    app.config["SQLALCHEMY_DATABASE_URI"] = (
        f"mysql+pymysql://{My_Secrets.user_name}:{My_Secrets.password}@localhost/{My_Secrets.db_name}"
    )
    app.config["SECRET_KEY"] = My_Secrets.key

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
