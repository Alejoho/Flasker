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


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 405


@app.errorhandler(500)
def page_not_found(e):
    return render_template("500.html"), 500
