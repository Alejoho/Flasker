from flask import Blueprint, render_template, flash
from app.forms import NamerForm

bp = Blueprint("name_routes", __name__)


@bp.route("/user/<name>")
def user(name):
    return render_template("user/user.html", user_name=name)


@bp.route("/name", methods=["GET", "POST"])
def name():
    my_name = None
    form = NamerForm()

    if form.validate_on_submit():
        my_name = form.name.data
        form.name.data = ""
        flash("Form submitted succesfully!")

    return render_template("name.html", name=my_name, form=form)
