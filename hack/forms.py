from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    email = StringField('Email',validators=[DataRequired()])
    password = PasswordField('Password',validators=[DataRequired()])
    submit = SubmitField("Log in")

class RegForm(FlaskForm):
    email = StringField('Email',validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password',validators=[DataRequired()])
    submit = SubmitField("Register")

class HuntForm(FlaskForm):
    ans = StringField('answer', validators=[DataRequired()])
    submit = SubmitField('submit')

class QuestionForm(FlaskForm):
    question = StringField('Question', validators=[DataRequired()])
    answer = StringField('Answer', validators=[DataRequired()])
    submit = SubmitField('Submit')
