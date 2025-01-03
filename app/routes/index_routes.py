from flask import Blueprint, render_template
from datetime import date, timezone, datetime
from pytz import UTC

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


@bp.route("/dates")
def dates():
    dates = {
        "my_date_zone": datetime.now(),
        "utc": datetime.now(timezone.utc),
        "utc_pytz": datetime.now(UTC),
    }

    return dates


@bp.get("/bootest")
def bootest():
    return render_template("bootest.html")
