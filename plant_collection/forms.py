from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms import validators
from wtforms.validators import DataRequired, Email

class UserLoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit_button = SubmitField()

class UserSignupForm(FlaskForm):
    first_name = StringField('First Name:', validators=[DataRequired()])
    last_name = StringField('Last Name:', validators=[DataRequired()])
    email = StringField('Email:', validators=[DataRequired(), Email()])
    password = PasswordField('Password:', validators=[DataRequired()])
    submit_button = SubmitField()

class PlantForm(FlaskForm):
    name = StringField('Name:', validators=[DataRequired()])
    room = StringField('Room in House:', validators=[DataRequired()])
    plant_type = StringField('Type of Plant:', validators=[DataRequired()])
    light = StringField('Light Needed:', validators=[DataRequired()])
    description = StringField('Description:', validators=[DataRequired()])
    water = StringField('Amount of Water Needed:', validators=[DataRequired()])
    fertilizer = StringField('Fertilizer:', validators=[DataRequired()])
    humidity = StringField('Humidity:', validators=[DataRequired()])
    pests = StringField('Pest Control:', validators=[DataRequired()])
    fun_fact = StringField('Fun Fact(s):', validators=[DataRequired()])
    submit_button = SubmitField()