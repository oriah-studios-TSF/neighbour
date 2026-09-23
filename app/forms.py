from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import DataRequired, Email, ValidationError, Length, Regexp, EqualTo
from app.models import User

class RegistrationForm(FlaskForm):
    full_name = StringField('Full Name *', validators=[DataRequired(), Length(min=2, max=100)])
    email = StringField('Email Address *', validators=[DataRequired(), Email()])
    phone_number = StringField('Phone Number *', validators=[DataRequired(), Regexp(r'^(\+27|0)[6-8][0-9]{8}$', message='Enter a valid South African phone number.')])
    community_id = SelectField('Neighbourhood *', coerce=int, validators=[DataRequired()])
    password = PasswordField('Password *', validators=[DataRequired(), Length(min=8, max=128)])
    confirm_password = PasswordField('Confirm Password *', validators=[DataRequired(), Length(min=8, max=128), EqualTo('password', message='Passwords must match.')])
    submit = SubmitField('Create Account')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')

    def validate_phone_number(self, phone_number):
        user = User.query.filter_by(phone_number=phone_number.data).first()
        if user is not None:
            raise ValidationError('Please use a different phone number.')

class LoginForm(FlaskForm):
    email = StringField('Email Address *', validators=[DataRequired(), Email()])
    password = PasswordField('Password *', validators=[DataRequired()])
    submit = SubmitField('Access Account')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('Invalid email address.')

    def validate_password(self, password):
        user = User.query.filter_by(email=self.email.data).first()
        if user is not None and not user.check_password(password.data):
            raise ValidationError('Invalid password.')

        if user is None:
            raise ValidationError('Invalid email address.')