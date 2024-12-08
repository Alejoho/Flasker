from flask import Blueprint, render_template

bp = Blueprint("error_routes", __name__)


@bp.app_errorhandler(404)
def page_not_found(e):
    return render_template("error/404.html"), 404


@bp.app_errorhandler(500)
def page_not_found(e):
    return render_template("error/500.html"), 500
