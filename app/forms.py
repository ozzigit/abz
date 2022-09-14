from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import StringField, PasswordField, BooleanField, SubmitField, FileField, SelectField, validators, \
    HiddenField
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
    date_join = StringField("Date join yyyy-mm-dd", validators=[DataRequired(), validators.Length(min=10, max=10)])
    wage = StringField("Wage", validators=[DataRequired()])
    chief_part_name = StringField(
        "Because a list of employeers is too big Please input a part of chief's full name 5 chars min")
    chief_name = SelectField("Chief", choices=['', ''], validate_choice=False)
    # photo_url = FileField("Photo", validators=[FileAllowed(['jpg', 'png'], 'Images only!')])

    def validate_ar_wage(self, ar_params):
        try:
            # try to convert each part of the input to a float
            [float(x) for x in ar_params.data.split(',')]
        except ValueError:
            raise ValidationError('Invalid input. Please...')


class EditPersonForm(PersonForm):
    edit = SubmitField(label='Edit')
    delete = SubmitField(label='Delete')


class CreatePersonForm(PersonForm):
    create = SubmitField(label='Create')
