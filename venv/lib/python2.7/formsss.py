from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, InputRequired


class LoginForm(FlaskForm):
    username = StringField('Username',validators=[InputRequired(),Length(min=4,max=20)])
    password = PasswordField('Password',validators=[InputRequired(),Length(min=5,max=80)])
    remember = BooleanField('remember')

class RegisterForm(FlaskForm):
    username = StringField('Username',validators=[InputRequired(),Length(min=4,max=20)])
    password = PasswordField('Password',validators=[InputRequired(),Length(min=5,max=80)])
    email = StringField('Email',validators=[InputRequired(),Email()])


class imageBody(FlaskForm):
    username = StringField('author',validators=[InputRequired()])
    img = StringField('img_ID',validators=[InputRequired()])
    name = StringField('Name',validators=[InputRequired()])
    description = StringField('Description')


