from flask_wtf import FlaskForm
from wtforms import widgets, StringField, PasswordField, SubmitField, SelectField, SelectMultipleField, TextAreaField, IntegerField, DateField
from wtforms.validators import Length, DataRequired, ValidationError
from .model import Users, Games


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


class SearchForm(FlaskForm):
    game_name = StringField(label="game_name", validators=[DataRequired()])
    submit = SubmitField(label="Search")


class PurchaseForm(FlaskForm):
    submit = SubmitField(label="Purchase")


class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()


class GameForm(FlaskForm):

    def validate_name_field(form, field):
        if Games.check_for_duplicate_by_name(field.data):
            raise ValidationError("Game already exists!!")

    name = StringField(label="Name", validators=[
                       Length(min=2, max=30), DataRequired(), validate_name_field])
    genre = StringField(label="Genre", validators=[
                        Length(min=2, max=30), DataRequired()])
    pf = MultiCheckboxField(label="Platforms Supported", choices=[(
        "PC", "PC"), ("playstation", "Playstation"), ("xbox", "Xbox")])
    desc = TextAreaField(label="Description", validators=[
                         DataRequired(), Length(min=2, max=500)])
    pub = StringField(label="Publisher", validators=[
                      DataRequired(), Length(min=2, max=30)])
    price = IntegerField(label="Price", validators=[DataRequired()])
    r_date = DateField(label="Release Date", validators=[DataRequired()])

    submit = SubmitField(label="Add Game")


class GameEditForm(FlaskForm):

    og_name = StringField(label="og_name")
    name = StringField(label="Name", validators=[
                       Length(min=2, max=30), DataRequired()])
    genre = StringField(label="Genre", validators=[
                        Length(min=2, max=30), DataRequired()])
    pf = MultiCheckboxField(label="Platforms Supported", choices=[(
        "PC", "PC"), ("playstation", "Playstation"), ("xbox", "Xbox")])
    desc = TextAreaField(label="Description", validators=[
        Length(min=2, max=500)])
    pub = StringField(label="Publisher", validators=[
                      DataRequired(), Length(min=2, max=30)])
    price = IntegerField(label="Price", validators=[DataRequired()])
    r_date = DateField(label="Release Date", validators=[
                       DataRequired()], format="%Y-%m-%d")

    submit1 = SubmitField(label="Save Changes")


class GameDeleteForm(FlaskForm):
    game_name = StringField(label="game_name")
    submit2 = SubmitField(label="Delete")
