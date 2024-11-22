from flask import Flask, render_template, flash, redirect, url_for, request
from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    SubmitField,
    PasswordField,
    BooleanField,
    ValidationError,
)
from wtforms.validators import DataRequired, EqualTo, Length
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone
from my_secrets import My_Secrets
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__)
# app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"

app.config["SQLALCHEMY_DATABASE_URI"] = (
    f"mysql+pymysql://{My_Secrets.user_name}:{My_Secrets.password}@localhost/{My_Secrets.db_name}"
)
app.config["SECRET_KEY"] = My_Secrets.key

db = SQLAlchemy(app)

migrate = Migrate(app, db)


class Users(db.Model):
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


class UserForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    email = StringField(
        "Email",
        validators=[DataRequired("You need to enter your email")],
    )
    favorite_color = StringField("Favorite Color")
    password = PasswordField(
        "Password",
        validators=[
            DataRequired(),
            EqualTo("password_confirmation", "Passwords Must Match!"),
        ],
    )
    password_confirmation = PasswordField(
        "Password confirmation", validators=[DataRequired()]
    )
    submit = SubmitField("Submit")


class PasswordForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Submit")


class NamerForm(FlaskForm):
    name = StringField("What's your name?", validators=[DataRequired()])
    submit = SubmitField("Submit")


@app.route("/delete/<int:id>")
def delete_user(id):
    user_to_delete = Users.query.get_or_404(id)
    db.session.delete(user_to_delete)
    try:
        db.session.commit()
    except Exception as err:
        print(err)
        return 404
    flash("User Deleted Successfully!!")
    return redirect(url_for("add_user"))


@app.route("/update/<int:id>", methods=["GET", "POST"])
def update(id):
    name = None
    record = Users.query.get_or_404(id)
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


@app.route("/user/add", methods=["GET", "POST"])
def add_user():
    my_name = None
    form = UserForm()

    if form.validate_on_submit():

        user = Users(
            name=form.name.data,
            email=form.email.data,
            favorite_color=form.favorite_color.data,
            password=form.password.data,
        )
        db.session.add(user)
        # try:
        db.session.commit()
        # except Exception as er:
        #     print(er)
        #     flash("Integrity Error!", "error")
        #     return 404
        # else:
        my_name = form.name.data
        form.name.data = ""
        form.email.data = ""
        form.favorite_color.data = ""
        form.password.data = ""
        form.password_confirmation.data = ""
        flash("User added succesfully!")
        our_users = Users.query.order_by(Users.date_added)
        return render_template(
            "add_user.html", form=form, name=my_name, our_users=our_users
        )

    our_users = Users.query.order_by(Users.date_added)

    return render_template(
        "add_user.html", form=form, name=my_name, our_users=our_users
    )


# filters of jinja
# safe
# capitalize
# lower
# upper
# title
# trim
# striptags


@app.route("/")
def index():
    first_name = "Alejo"
    stuff = "This is <strong>bold</strong> Text"
    favorite_pizza = ["Pepperoni", "Cheese", "Mushrooms", 41]
    return render_template(
        "index.html", first_name=first_name, stuff=stuff, favorite_pizza=favorite_pizza
    )


@app.route("/user/<name>")
def user(name):
    return render_template("user.html", user_name=name)


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 405


@app.errorhandler(500)
def page_not_found(e):
    return render_template("500.html"), 500


@app.route("/name", methods=["GET", "POST"])
def name():
    my_name = None
    form = NamerForm()

    if form.validate_on_submit():
        my_name = form.name.data
        form.name.data = ""
        flash("Form submitted succesfully!")

    return render_template("name.html", name=my_name, form=form)


@app.route("/test_password", methods=["GET", "POST"])
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

        user = Users.query.filter_by(email=email).first()

        passed = user.verify_password(password)

    return render_template(
        "test_password.html", form=form, user=user, password=password, passed=passed
    )
