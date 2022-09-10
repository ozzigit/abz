from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, FileField, validators
import re
from wtforms.validators import DataRequired, EqualTo, Email, ValidationError
from app.models import Users


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = Users.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')


class PersonForm(FlaskForm):
    name = StringField('Person Name')
    work_position = StringField("Work_position")
    date_join = StringField("Date join")
    wage = StringField("Wage")
    chief_name = StringField("Chief")
    photo_url = FileField("Photo")
    submit = SubmitField('Register')

    def validate_name(self, person_name):
        user = Users.query.filter_by(username=person_name.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')
