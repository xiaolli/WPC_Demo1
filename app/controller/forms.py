from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,BooleanField,SelectField,RadioField,DateTimeField,DateField
from wtforms.validators import DataRequired


class loginForm(FlaskForm):
    login_name = StringField('login_name',validators=[DataRequired()])
    login_password = PasswordField('login_password',validators=[DataRequired()])


class selectForm(FlaskForm):
    SelectField('',validators=[DataRequired()],)