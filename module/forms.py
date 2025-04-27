from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, EmailField, IntegerField
from wtforms.validators import Length, DataRequired, Email, EqualTo, ValidationError
from module.models import User

class Login(FlaskForm):
    username= StringField('Username',validators=[DataRequired(),Length(4,20)])
    password = PasswordField('Password',validators=[DataRequired(),Length(6,30)])
    submit = SubmitField('submit')

class Register(FlaskForm):

    username= StringField('Username',validators=[DataRequired(),Length(4,20)])
    email = EmailField('Email address', validators=[DataRequired(),Email()])
    password = PasswordField('Password',validators=[DataRequired(),Length(6,30)])
    confirm_password = PasswordField('Confirm Password',validators=[EqualTo('password')])
    submit = SubmitField('submit')
