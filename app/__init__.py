import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager
from dotenv import load_dotenv

load_dotenv()

db = SQLAlchemy()
migrate = Migrate()
csrf = CSRFProtect()
login_manager = LoginManager()


def create_app():
    app = Flask(__name__)

    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")

    # app.config.from_object("config.Config")

    db.init_app(app)
    migrate.init_app(app, db)
    csrf.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = "user_routes.login"

    @login_manager.user_loader
    def load_user(user_id):
        from app.models import User

        return User.query.get_or_404(int(user_id))

    from app.routes import (
        error_routes_bp,
        index_routes_bp,
        name_routes_bp,
        user_routes_bp,
        post_routes_bp,
    )

    app.register_blueprint(error_routes_bp)
    app.register_blueprint(index_routes_bp)
    app.register_blueprint(name_routes_bp)
    app.register_blueprint(user_routes_bp)
    app.register_blueprint(post_routes_bp)

    return app
