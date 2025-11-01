from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, SelectField, IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, Optional, NumberRange
from app.models import User

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=64)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    first_name = StringField('First Name', validators=[DataRequired(), Length(min=1, max=64)])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(min=1, max=64)])
    location = SelectField('Location', choices=[
        ('', 'Select Location'),
        ('Lagos', 'Lagos'),
        ('Abuja', 'Abuja'),
        ('Port Harcourt', 'Port Harcourt'),
        ('Kano', 'Kano'),
        ('Ibadan', 'Ibadan'),
        ('Benin', 'Benin'),
        ('Enugu', 'Enugu'),
        ('Kaduna', 'Kaduna'),
        ('Other', 'Other')
    ], validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    agree_tos = BooleanField('I agree to the Terms of Service and Privacy Policy', validators=[DataRequired()])
    submit = SubmitField('Sign Up')
    
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')
    
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is already registered.')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class UpdateAccountForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=64)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    first_name = StringField('First Name', validators=[DataRequired(), Length(min=1, max=64)])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(min=1, max=64)])
    phone = StringField('Phone Number', validators=[Optional(), Length(max=20)])
    location = SelectField('Location', choices=[
        ('Lagos', 'Lagos'),
        ('Abuja', 'Abuja'),
        ('Port Harcourt', 'Port Harcourt'),
        ('Kano', 'Kano'),
        ('Ibadan', 'Ibadan'),
        ('Benin', 'Benin'),
        ('Enugu', 'Enugu'),
        ('Kaduna', 'Kaduna'),
        ('Other', 'Other')
    ])
    company = StringField('Company', validators=[Optional(), Length(max=100)])
    occupation = SelectField('Occupation', choices=[
        ('', 'Select Occupation'),
        ('Home Owner', 'Home Owner'),
        ('Contractor', 'Contractor'),
        ('Architect', 'Architect'),
        ('Engineer', 'Engineer'),
        ('Builder', 'Builder'),
        ('Developer', 'Developer'),
        ('Student', 'Student'),
        ('Other', 'Other')
    ], validators=[Optional()])
    bio = TextAreaField('Bio', validators=[Optional(), Length(max=500)])
    submit = SubmitField('Update Profile')

class ProfilePictureForm(FlaskForm):
    picture = FileField('Update Profile Picture', validators=[
        FileAllowed(['jpg', 'jpeg', 'png'], 'Images only!')
    ])
    submit = SubmitField('Update Picture')

class UserPreferencesForm(FlaskForm):
    preferred_block_type = SelectField('Default Block Type', choices=[
        ('9_inch_hollow', '9-inch Hollow Block'),
        ('6_inch_hollow', '6-inch Hollow Block')
    ])
    preferred_waste_percentage = SelectField('Default Waste Percentage', choices=[
        ('5', '5% (Very Efficient)'),
        ('10', '10% (Standard)'),
        ('15', '15% (Conservative)'),
        ('20', '20% (High Waste)')
    ])
    measurement_system = SelectField('Preferred Measurement System', choices=[
        ('feet', 'Feet and Inches'),
        ('meters', 'Meters')
    ])
    preferred_currency = SelectField('Preferred Currency', choices=[
        ('₦', 'Naira (₦)'),
        ('$', 'US Dollar ($)'),
        ('€', 'Euro (€)')
    ])
    email_notifications = BooleanField('Email Notifications')
    sms_notifications = BooleanField('SMS Notifications')
    marketing_emails = BooleanField('Marketing Emails')
    submit = SubmitField('Save Preferences')

class ChangePasswordForm(FlaskForm):
    current_password = PasswordField('Current Password', validators=[DataRequired()])
    new_password = PasswordField('New Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm New Password', validators=[DataRequired(), EqualTo('new_password')])
    submit = SubmitField('Change Password')