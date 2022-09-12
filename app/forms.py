from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import StringField, PasswordField, BooleanField, SubmitField, FileField, SelectField, validators
from wtforms.validators import DataRequired, EqualTo, ValidationError
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
    name = StringField('Person Name', validators=[DataRequired(), validators.Length(min=5, max=45)])
    work_position = StringField("Work_position", validators=[DataRequired(), validators.Length(min=5, max=45)])
    date_join = StringField("Date join", validators=[validators.Length(min=10, max=10)])
    wage = StringField("Wage")
    chief_part_name = StringField(
        "Because a list of employeers is too big Please input a part of chief's full name 5 chars min")
    chief_name = SelectField("Chief", choices=["", ""])
    photo_url = FileField("Photo", validators=[FileAllowed(['jpg', 'png'], 'Images only!')])

    def validate_name(self, name):
        if name is None:
            raise ValidationError('Please enter a  username.')

    def validate_work_position(self, work):
        if work is None:
            raise ValidationError('Please enter a  work_position.')

    def validate_photo_url(self, path: str):
        if path and not path.endswith('.jpg'):
            raise ValidationError('Please choose a .jpg file.')


class EditPersonForm(PersonForm):
    edit = SubmitField('Edit')
    delete = SubmitField('Delete')


class CreatePersonForm(PersonForm):
    create = SubmitField('Create')
