from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField, SubmitField, SelectField
from wtforms.validators import DataRequired, EqualTo, Length, Regexp
from wtforms.fields import DateField

class RegistrationForm(FlaskForm):
    username = StringField(
        'Username',
        validators=[
            DataRequired(),
            Length(min=3, max=20, message="Username must be between 3 and 20 characters."),
            Regexp(r"^[\w@#$%^&+=!.,\-]+$", message="Username can only contain letters, numbers, and symbols: @#$%^&+=!.,-")
        ]
    )
    password = PasswordField(
        'Password',
        validators=[
            DataRequired(),
            Length(min=8, message="Password must be at least 8 characters long."),
            Regexp(r"^(?=.*[A-Za-z])(?=.*\d)(?=.*[@#$%^&+=!.,\-])[A-Za-z\d@#$%^&+=!.,\-]+$", 
                   message="Password must include at least one letter, one number, and one special character.")
        ]
    )
    confirm_password = PasswordField(
        'Confirm Password',
        validators=[DataRequired(), EqualTo('password', message="Passwords must match.")]
    )
    submit = SubmitField('Register')


class LoginForm(FlaskForm):
    username = StringField(
        'Username',
        validators=[
            DataRequired(),
            Regexp(r"^[\w@#$%^&+=!.,\-]+$", message="Username can only contain letters, numbers, and symbols: @#$%^&+=!.,-")
        ]
    )
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


class AddPatientForm(FlaskForm):
    name = StringField('Patient Name', validators=[DataRequired()])
    gender = SelectField('Gender', choices=[('male', 'Male'),('female', 'Female')], validators=[DataRequired()])
    birth_date = DateField('Birth Date', format='%Y-%m-%d', validators=[DataRequired()])  
    blood_type = SelectField('Blood Type', choices=[
        ('a-positive', 'A+'),
        ('a-negative', 'A-'),
        ('b-positive', 'B+'),
        ('b-negative', 'B-'),
        ('ab-positive', 'AB+'),
        ('ab-negative', 'AB-'),
        ('o-positive', 'O+'),
        ('o-negative', 'O-')
    ], validators=[DataRequired()])

    submit = SubmitField('Add Patient')

class EditPatientForm(FlaskForm):
    name = StringField('Patient Name', validators=[DataRequired()])
    gender = SelectField('Gender', choices=[('male', 'Male'), ('female', 'Female')], validators=[DataRequired()])
    birth_date = DateField('Birth Date', format='%Y-%m-%d', validators=[DataRequired()])
    blood_type = SelectField('Blood Type', choices=[
        ('a-positive', 'A+'),
        ('a-negative', 'A-'),
        ('b-positive', 'B+'),
        ('b-negative', 'B-'),
        ('ab-positive', 'AB+'),
        ('ab-negative', 'AB-'),
        ('o-positive', 'O+'),
        ('o-negative', 'O-')
    ], validators=[DataRequired()])


class DeletePatientForm(FlaskForm):
    id = IntegerField('Patient ID to Remove', validators=[DataRequired()])
    submit = SubmitField('Delete Patient')

class AddMedicalRecordForm(FlaskForm):
    details = StringField('Record Details', validators=[DataRequired()])
    submit = SubmitField('Add Record')
