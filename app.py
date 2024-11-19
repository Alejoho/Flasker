from flask import Flask, render_template, flash
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from my_secrets import My_Secrets


app = Flask(__name__)
# app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"

app.config["SQLALCHEMY_DATABASE_URI"] = (
    f"mysql+pymysql://{My_Secrets.user_name}:{My_Secrets.password}@localhost/{My_Secrets.db_name}"
)
app.config["SECRET_KEY"] = My_Secrets.key

db = SQLAlchemy(app)


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    date_added = db.Column(db.DateTime, default=datetime.utcnow())

    def __repr__(self) -> str:
        return f"<Name {self.name}>"


class UserForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    email = StringField(
        "Email",
        validators=[DataRequired("You need to enter your email")],
    )
    submit = SubmitField("Submit")


class NamerForm(FlaskForm):
    name = StringField("What's your name?", validators=[DataRequired()])
    submit = SubmitField("Submit")


@app.route("/update/<int:id>", methods=["GET", "POST"])
def update(id):
    print(id)
    return render_template("update.html")


@app.route("/user/add", methods=["GET", "POST"])
def add_user():
    my_name = None
    form = UserForm()

    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user is None:
            user = Users(name=form.name.data, email=form.email.data)
            db.session.add(user)
            db.session.commit()

        my_name = form.name.data
        form.name.data = ""
        form.email.data = ""
        flash("User added succesfully!")

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
