from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, SelectField, DateField, TimeField, TextAreaField
from wtforms.validators import DataRequired, Email, Length

class RegistrationForm(FlaskForm):
    username= StringField("Username", validators=[DataRequired()])
    password= PasswordField("Password", validators=[DataRequired(), Length(min=6)])
    email= StringField("Email",validators=[DataRequired(),Email()] )
    submit= SubmitField("Register")

class LoginForm(FlaskForm):
    username= StringField("Username", validators=[DataRequired()]) 
    password= PasswordField("Password", validators=[DataRequired()])  
    submit = SubmitField("Login")

class AppointmentForm(FlaskForm):
    doctor = SelectField("Select Doctor", choices=[], coerce=int,validators=[DataRequired()])
    appointment_date = DateField("Appoointment Date", validators=[DataRequired()])
    appointment_time = TimeField("Appointment Time", validators=[DataRequired()])
    reason = TextAreaField("Reason", validators=[DataRequired()])
    submit = SubmitField("Submit")