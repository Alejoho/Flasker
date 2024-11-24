from flask import Blueprint, render_template

bp = Blueprint("index_routes", __name__)
# static_folder="/app/static", template_folder="/app/templates"


@bp.route("/")
def index():
    first_name = "Alejo"
    stuff = "This is <strong>bold</strong> Text"
    favorite_pizza = ["Pepperoni", "Cheese", "Mushrooms", 41]
    return render_template(
        "index.html",
        first_name=first_name,
        stuff=stuff,
        favorite_pizza=favorite_pizza,
    )
    # return "Hello world!!"
