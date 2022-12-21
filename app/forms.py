from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, Form, TextAreaField, EmailField, validators
from wtforms.validators import DataRequired, Email

class LoginForm(FlaskForm):
    username  = StringField('Tunnus', validators=[DataRequired(message='* tunnus tarvitaan')])
    password = PasswordField('Salasana', validators=[DataRequired(message='* salasana tarvitaan')])
    submit = SubmitField('Kirjaudu')


class RegistrationForm(FlaskForm):
    username = StringField('Tunnus', validators=[DataRequired(message='* tunnus tarvitaan')])
    password = PasswordField('Salasana', validators=[DataRequired(message='* salasana tarvitaan')])
    submit = SubmitField('Rekisteröidy')

class ContactForm(FlaskForm):
  name = StringField("Nimi", validators=[DataRequired(message='* nimi tarvitaan')])
  email = StringField(label='Sähköposti', validators=[
      DataRequired('* sähköposti tarvitaan'), Email(granular_message=True)])
  subject = StringField("Aihe")
  message = TextAreaField("Viesti", validators=[DataRequired(message='* viesti puuttuu')])
  submit = SubmitField("Lähetä")