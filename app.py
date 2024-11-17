from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


app = Flask(__name__)
app.config["SECRET_KEY"] = "my super secret key that no one is supposed to know"


class NamerForm(FlaskForm):
    name = StringField("What's your name?", validators=[DataRequired()])
    submit = SubmitField("Submit")


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

    return render_template("name.html", name=my_name, form=form)
