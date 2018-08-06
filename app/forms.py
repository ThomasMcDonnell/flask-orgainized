from flask_wtf import FlaskForm
from wtforms import (StringField, PasswordField, BooleanField, SubmitField,
                    TextAreaField)
from wtforms.fields.html5 import DateField
from wtforms.validators import (DataRequired, ValidationError, Email, EqualTo, 
                               Length)
from app.models import User


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password_two = PasswordField('Password Confrimation',
                                 validators=[DataRequired(),
                                             EqualTo('password')])
    submit = SubmitField('Sign Up')
    
    #check availability of username
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        #query expected to return None
        if user is not None:
            raise ValidationError('This username is already registered,'
                                  'please choose another.')
    
    #check availability of email
    def validate_emial(self, email):
        user = User.query.filter_by(email=email.data).first()
        #query expected to return None
        if user is not None:
            raise ValidationError('This email is already registered,'
                                  'please choose another.')


class TodoForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), 
                                             Length(min=1, max=64)])
    start = DateField('Start', format='%Y-%m-%d', validators=[DataRequired()])
    end = DateField('End', format='%Y-%m-%d', validators=[DataRequired()])
    actionable = TextAreaField('Any additional info...',
                               validators=[Length(min=1, max=140)])
    submit = SubmitField('Submit')
