from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, EqualTo, ValidationError
from .models import User

class RegistrationForm(FlaskForm):
    username = StringField('username', validators=[
                           InputRequired(message="username required"), Length(min=4, max=50, message="Username must be 4-50 characters long")])
    password = PasswordField('password', validators=[InputRequired(message="password required"), Length(
        min=4, message="Password must be at least 4 characters")])
    password2 = PasswordField('password2', validators=[
                              InputRequired(message="confirm your password"), EqualTo('password', message='passwords do not match')])
    submit_btn = SubmitField('signup')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username already exists')

