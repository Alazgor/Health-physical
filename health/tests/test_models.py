# tests/test_models.py
import unittest
from datetime import datetime
from health import db, app
from health.models import User, Workout

class TestModels(unittest.TestCase):
    def setUp(self):
        # Создание тестовых данных
        self.test_data = pd.DataFrame([
            {'Date': datetime(2024, 7, 28), 'Type': 'cycling', 'Duration (minutes)': 45, 'Calories': 400},
            {'Date': datetime(2024, 7, 29), 'Type': 'running', 'Duration (minutes)': 30, 'Calories': 300},
        ])

    def tearDown(self):
        # Очистка базы данных после каждого теста
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_create_user(self):
        user = User.query.filter_by(email='test@example.com').first()
        self.assertIsNotNone(user)
        self.assertEqual(user.first_name, 'Test')
        self.assertTrue(user.check_password('password123'))

    def test_create_workout(self):
        workout = Workout(
            user_id=self.user.id,
            workout_type='running',
            duration=30,
            calories=300,
            date=datetime.now()
        )
        db.session.add(workout)
        db.session.commit()

        workout_from_db = Workout.query.filter_by(user_id=self.user.id).first()
        self.assertIsNotNone(workout_from_db)
        self.assertEqual(workout_from_db.workout_type, 'running')
        self.assertEqual(workout_from_db.duration, 30)
        self.assertEqual(workout_from_db.calories, 300)

    def test_user_workout_relationship(self):
        workout = Workout(
            user_id=self.user.id,
            workout_type='cycling',
            duration=45,
            calories=400,
            date=datetime.now()
        )
        db.session.add(workout)
        db.session.commit()

        user = User.query.filter_by(email='test@example.com').first()
        self.assertEqual(len(user.workouts), 1)
        self.assertEqual(user.workouts[0].workout_type, 'cycling')

if __name__ == '__main__':
    unittest.main()
