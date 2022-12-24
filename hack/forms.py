from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField, IntegerField
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

class EditUserForm(FlaskForm):
    username = StringField('Updated text', validators=[DataRequired()])
    email = StringField('Updated text2', validators=[DataRequired()])
    points = IntegerField('Points')
    submit = SubmitField('Submit')

class EditQuesForm(FlaskForm):
    question = StringField('new_q', validators=[DataRequired()])
    ans = StringField('new_ans', validators=[DataRequired()])
    submit = SubmitField('Submit')

class ContactForm(FlaskForm):
    text = StringField('Query', validators=[DataRequired()])
    submit = SubmitField('Submit')
