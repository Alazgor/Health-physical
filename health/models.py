from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from health import db, login_manager
from datetime import datetime
from health.utils import generate_token, verify_token

class User(db.Model, UserMixin):
    __tablename__ = 'user'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(150))
    last_name = db.Column(db.String(150))
    email = db.Column(db.String(150), unique=True)
    password_hash = db.Column(db.String(150))
    birth_date = db.Column(db.Date, nullable=True)
    is_admin = db.Column(db.Boolean, default=False)
    role = db.Column(db.String(50), default='user')

    def __repr__(self):
        return '<User {}>'.format(self.email)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @staticmethod
    def generate_reset_password_token(email, expiration=600):
        return generate_token(email, expiration)

    @staticmethod
    def verify_reset_password_token(token):
        return verify_token(token)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class Workout(db.Model):
    __tablename__ = 'workout'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    workout_type = db.Column(db.String(50), nullable=False)
    duration = db.Column(db.Integer, nullable=False)  # duration in minutes
    calories = db.Column(db.Integer, nullable=False)
    date = db.Column(db.Date, nullable=False)

    user = db.relationship('User', backref=db.backref('workouts', lazy=True))

