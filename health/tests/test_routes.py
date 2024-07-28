# tests/test_routes.py
import unittest
from health import app, db
from health.models import User, Workout
from flask_testing import TestCase

class TestRoutes(TestCase):

    def create_app(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        app.config['SECRET_KEY'] = 'secret'
        return app

    def setUp(self):
        db.create_all()
        self.client = app.test_client()
        user = User(email='test@example.com', first_name='Test', last_name='User')
        user.set_password('password')
        db.session.add(user)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_home_page(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Health Tracker', response.data)

    def test_workouts_page_requires_login(self):
        response = self.client.get('/workouts')
        self.assertEqual(response.status_code, 302)  # Redirect to login page

    # Add more tests here...

if __name__ == '__main__':
    unittest.main()
