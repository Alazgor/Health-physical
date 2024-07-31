from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, DateField, SelectField, IntegerField, FloatField, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError, Length, Optional
from health.models import User
from flask import flash

class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    birth_date = DateField('Birth Date (YYYY-MM-DD)', format='%Y.%m.%d', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    secret_question = TextAreaField('Secret Question', validators=[DataRequired(), Length(max=200)])
    secret_answer = StringField('Secret Answer', validators=[DataRequired(), Length(max=200)])
    is_admin = BooleanField('Admin Access')
    submit = SubmitField('Register')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            flash('This email is already registered. Please use a different email.')
            raise ValidationError('Please use a different email address.')

class VerifySecretForm(FlaskForm):
    secret_question = StringField('Secret Question', render_kw={'readonly': True})
    secret_answer = StringField('Answer to Secret Question', validators=[DataRequired()])
    submit = SubmitField('Verify')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    remember = BooleanField('Remember me')
    submit = SubmitField('Sign In')

class ResetPasswordRequestForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

class VerifySecretForm(FlaskForm):
    secret_question = StringField('Secret Question', render_kw={'readonly': True})
    secret_answer = StringField('Answer to Secret Question', validators=[DataRequired()])
    submit = SubmitField('Verify')

class ResetPasswordForm(FlaskForm):
    password = PasswordField('New Password', validators=[DataRequired(), Length(min=6)])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')

class UpdateUserRoleForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    role = SelectField('Role', choices=[('user', 'User'), ('admin', 'Admin')])
    submit = SubmitField('Update Role')

class EditUserForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    birth_date = DateField('Birth Date', format='%Y.%m.%d', validators=[DataRequired()])
    role = SelectField('Role', choices=[('user', 'User'), ('admin', 'Admin')], validators=[DataRequired()])
    password = PasswordField('New Password', validators=[Optional(), Length(min=6)])
    confirm_password = PasswordField('Confirm New Password', validators=[EqualTo('password', message='Passwords must match')])
    submit = SubmitField('Update User')

    def validate_email(self, email):
        if User.query.filter_by(email=email.data).first():
            raise ValidationError('Email already registered.')

    def update_user(self, user):
        user.first_name = self.first_name.data
        user.last_name = self.last_name.data
        user.email = self.email.data
        user.birth_date = self.birth_date.data
        user.role = self.role.data
        if self.password.data:
            user.set_password(self.password.data)
        db.session.commit()

class WorkoutForm(FlaskForm):
    workout_type = SelectField('Workout Type', choices=[
        ('bench_press', 'Bench Press'),
        ('squats', 'Squats'),
        ('deadlift', 'Deadlift'),
        ('running', 'Running'),
        ('cycling', 'Cycling'),
        ('swimming', 'Swimming'),
        ('pull_ups', 'Pull Ups'),
        ('push_ups', 'Push Ups'),
        ('jumping_jacks', 'Jumping Jacks'),
        ('burpees', 'Burpees'),
        ('rowing', 'Rowing'),
        ('yoga', 'Yoga')
    ], validators=[DataRequired()])
    duration = IntegerField('Duration (minutes)', validators=[DataRequired()])
    calories = FloatField('Calories Burned', validators=[DataRequired()])
    date = DateField('Date', format='%d.%m.%Y', validators=[DataRequired()])
    submit = SubmitField('Add Workout')

