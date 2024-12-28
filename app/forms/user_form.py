from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, EqualTo, Length


class UserForm(FlaskForm):
    name = StringField(
        "Name",
        validators=[
            Length(max=5, message="This field has to have less than 6 characters")
        ],
    )
    username = StringField("Username", validators=[DataRequired()])
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
