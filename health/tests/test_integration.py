import unittest
from health import app, db
from health.models import User

class IntegrationTestCase(unittest.TestCase):

    def setUp(self):
        self.app = app
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_registration(self):
        with self.app.test_client() as client:
            response = client.post('/register', data={
                'email': 'unique_testuser@example.com',
                'first_name': 'Test',
                'last_name': 'User',
                'password': 'password',
                'confirm_password': 'password',
                'birth_date': '2000.01.01'
            }, follow_redirects=True)

            # Добавить вывод данных формы
            print(response.data.decode())

            self.assertEqual(response.status_code, 200)

            # Проверка, что пользователь действительно создан
            user = User.query.filter_by(email='unique_testuser@example.com').first()
            self.assertIsNotNone(user)

if __name__ == '__main__':
    unittest.main()

