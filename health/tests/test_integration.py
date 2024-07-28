# tests/test_integration.py
import unittest
from health import app, db
from health.models import User, Workout
from datetime import datetime

class TestIntegration(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        self.app_context = app.app_context()
        self.app_context.push()
        db.create_all()

        self.user = User(email='test@example.com', first_name='Test', last_name='User')
        self.user.set_password('password123')
        db.session.add(self.user)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_registration_and_login(self):
        response = self.app.post('/register', data={
            'email': 'newuser@example.com',
            'first_name': 'New',
            'last_name': 'User',
            'password': 'newpassword',
            'confirm_password': 'newpassword',
            'birth_date': '2000-01-01'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Congratulations, you are now a registered user!', response.data)

        response = self.app.post('/login', data={
            'email': 'newuser@example.com',
            'password': 'newpassword'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Login successful!', response.data)

    def test_workout_creation(self):
        response = self.app.post('/login', data={
            'email': self.user.email,
            'password': 'password123'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        response = self.app.post('/add_workout', data={
            'workout_type': 'running',
            'duration': 30,
            'date': '2024-07-28'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Workout added successfully!', response.data)

        workout = Workout.query.filter_by(user_id=self.user.id, workout_type='running').first()
        self.assertIsNotNone(workout)
        self.assertEqual(workout.duration, 30)

    def test_workout_analysis(self):
        response = self.app.post('/login', data={
            'email': self.user.email,
            'password': 'password123'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        workout = Workout(
            user_id=self.user.id,
            workout_type='cycling',
            duration=45,
            calories=400,
            date=datetime.strptime('2024-07-28', '%Y-%m-%d').date()
        )
        db.session.add(workout)
        db.session.commit()

        response = self.app.get('/workout_analysis')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Workout Analysis Page', response.data)
        self.assertIn(b'cycling', response.data)

if __name__ == '__main__':
    unittest.main()
