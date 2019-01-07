from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField,SubmitField,BooleanField, TextAreaField
from wtforms.validators import DataRequired,Length, Email, EqualTo, ValidationError
from flask_login import current_user
from blog.models import User




class RegistrationForm(FlaskForm):
    username = StringField('Username', validators =[DataRequired(),Length(min=2, max = 15) ])
    email    = StringField('Email', validators =[DataRequired(),Email()])
    password = PasswordField('Password', validators= [DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators= [DataRequired(),EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user :
            raise ValidationError('This Username is taken, please choose another one!')


    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user :
            raise ValidationError('This Email Exist, please choose another one!')
            






class LoginForm(FlaskForm):
    email    = StringField('Email', validators =[DataRequired(),Email()])
    password = PasswordField('Password', validators= [DataRequired()])
    remember =  BooleanField('Remember me')
    submit = SubmitField('Login')


#update User Account form
class UpdateAccountForm(FlaskForm):
    username = StringField('Username', validators =[DataRequired(),Length(min=2, max = 15) ])
    email    = StringField('Email', validators =[DataRequired(),Email()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg','png','jpeg','gif'])])
    submit = SubmitField('Update')

    def validate_username(self, username): #Validates the update form from the database to avoid user repetition
        if username.data!= current_user.username:
                user = User.query.filter_by(username=username.data).first()
                if user :
                    raise ValidationError('This Username is taken, please choose another one!')


    def validate_email(self, email):
        if email.data!= current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user :
                raise ValidationError('This Email Exist, please choose another one!')





class RequestResetForm(FlaskForm):
    email = StringField('Email', validators =[DataRequired(),Email()])
    submit = SubmitField('Request Password Reset')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('This Email does not exist ')
            
class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators= [DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators= [DataRequired(),EqualTo('password')])
    submit = SubmitField('Reset')