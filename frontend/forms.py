from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError
from .model import Users


class RegisterForm(FlaskForm):

    def validate_username(form, field):
        if Users.check_username(field.data):
            raise ValidationError("Username is already taken.")

    username = StringField(label="Username", validators=[
                           Length(min=2, max=30), DataRequired(), validate_username])
    password = PasswordField(label="Password", validators=[
        Length(min=6), DataRequired()])
    submit = SubmitField(label="Create Account")


class LoginForm(FlaskForm):

    username = StringField(label="Username", validators=[DataRequired()])
    password = PasswordField(label="Password", validators=[DataRequired()])
    submit = SubmitField(label="Login")


class PurchaseForm(FlaskForm):
    submit = SubmitField(label="Purchase")
