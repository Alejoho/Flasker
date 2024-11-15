from flask import Flask, render_template

app = Flask(__name__)


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
