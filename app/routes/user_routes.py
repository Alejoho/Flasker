from flask import Blueprint, render_template, redirect, url_for, flash
from app.models import User
from app import db
from app.forms import UserForm, PasswordForm


bp = Blueprint("user_routes", __name__)


@bp.route("/delete/<int:id>")
def delete_user(id):
    user_to_delete = User.query.get_or_404(id)
    db.session.delete(user_to_delete)

    try:
        db.session.commit()
    except Exception as err:
        print(err)
        return 404
    flash("User Deleted Successfully!!")
    return redirect(url_for("user_routes.add_user"))


@bp.route("/update/<int:id>", methods=["GET", "POST"])
def update(id):
    name = None
    record = User.query.get_or_404(id)
    form = UserForm()

    if form.validate_on_submit():

        record.name = form.name.data
        record.email = form.email.data
        record.favorite_color = form.favorite_color.data
        record.password = form.password.data
        record.password_confirmation = form.password_confirmation.data
        db.session.commit()
        name = form.name.data

    return render_template("update.html", form=form, name=name, record=record)


@bp.route("/user/add", methods=["GET", "POST"])
def add_user():
    my_name = None
    form = UserForm()

    if form.validate_on_submit():

        user = User(
            name=form.name.data,
            email=form.email.data,
            favorite_color=form.favorite_color.data,
            password=form.password.data,
        )

        db.session.add(user)

        try:
            db.session.commit()
        except Exception as er:
            print(er)
            flash("Integrity Error!", "error")
            db.session.rollback()
        else:
            my_name = form.name.data

            form.name.data = ""
            form.email.data = ""
            form.favorite_color.data = ""
            form.password.data = ""
            form.password_confirmation.data = ""

            flash("User added succesfully!")

    our_users = db.session.query(User).order_by(User.date_added)

    return render_template(
        "add_user.html", form=form, name=my_name, our_users=our_users
    )


@bp.route("/test_password", methods=["GET", "POST"])
def test_password():
    user = None
    password = None
    passed = None
    form = PasswordForm()

    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        form.email.data = ""
        form.password.data = ""

        user = User.query.filter_by(email=email).first()

        passed = user.verify_password(password)

    return render_template(
        "test_password.html", form=form, user=user, password=password, passed=passed
    )
