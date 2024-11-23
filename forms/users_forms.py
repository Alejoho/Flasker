from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    SubmitField,
    PasswordField,
    BooleanField,
    ValidationError,
)
from wtforms.validators import DataRequired, EqualTo, Length

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