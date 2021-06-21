# udp/users/forms.py

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo
from wtforms import ValidationError
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from udp.dbs_handler import User


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField("LOGIN")
    
class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[EqualTo('password_confirm', message='Password and verify password do not match')])
    password_confirm = PasswordField('Password (repeat to verify)', validators=[DataRequired()])
    submit = SubmitField('SIGNUP')
    
    def check_email(self, field):
        if User.query.filter_by(email=field.email.data).first():
            raise ValidationError('This email has been registred already')
        
    def check_username(self, field):
        if User.query.filter_by(username=field.username.data).first():
            raise ValidationError('This username has been registerd already')
        
class UpdateUserForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    username = StringField('Username', validators=[DataRequired()])
    picture = FileField('Update profile picture', validators=[FileAllowed(['jpg','png'])])
    submit = SubmitField('UPDATE')
    
    def check_email(self, field):
        if User.query.filter_by(email=field.email.data).first():
            raise ValidationError('This email has been registered already')
        
    def check_username(self, field):
        if User.query.filter_by(email=field.username.data).first():
            raise ValidationError('This username has been registerd already')