from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    username = StringField(
        "Username", validators=[DataRequired("You need to fill the username locol")]
    )
    password = PasswordField(
        "password", validators=[DataRequired("You need to fill the password")]
    )
    submit = SubmitField("Submit")
