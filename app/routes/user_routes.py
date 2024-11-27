from flask import Blueprint, render_template, redirect, url_for, flash
from app.models import User
from app import db
from app.forms import UserForm, PasswordForm, LoginForm
from flask_login import login_required, login_user, logout_user, current_user


bp = Blueprint("user_routes", __name__)


@bp.route("/delete/<int:id>")
# @login_required
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


@bp.route("/update", methods=["GET", "POST"])
@login_required
def update():
    name = None
    # record = User.query.get_or_404(id)
    form = UserForm()

    if form.validate_on_submit():

        current_user.name = form.name.data
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.favorite_color = form.favorite_color.data
        current_user.password = form.password.data
        current_user.password_confirmation = form.password_confirmation.data

        db.session.commit()

        flash("User Profile Updated")

        return redirect(url_for("user_routes.dashboard"))

    return render_template("update.html", form=form)


@bp.route("/user/add", methods=["GET", "POST"])
def add_user():
    my_name = None
    form = UserForm()

    if form.validate_on_submit():

        user = User(
            name=form.name.data,
            username=form.username.data,
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
            form.username.data = ""
            form.email.data = ""
            form.favorite_color.data = ""
            form.password.data = ""
            form.password_confirmation.data = ""

            flash("User Registration succesfully! \nPlease Login")

            return redirect(url_for("user_routes.login"))

    our_users = db.session.query(User).order_by(User.date_added).all()

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


@bp.route("/dashboard", methods=["GET", "POST"])
@login_required
def dashboard():
    form = UserForm()

    return render_template("dashboard.html", form=form, record=current_user)


@bp.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()

        if user is None:
            flash("Username doesn't exist.")
            return render_template("login.html", form=form)

        if user.verify_password(form.password.data) == False:
            flash("Password incorrect..")
            return render_template("login.html", form=form)

        login_user(user)
        flash("Login Succesfull!!")
        return redirect(url_for("user_routes.dashboard"))

    return render_template("login.html", form=form)


@bp.get("/logout")
@login_required
def logout():
    logout_user()
    flash("Logout Succesfull.")
    return redirect(url_for("user_routes.login"))
