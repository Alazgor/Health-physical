# tests/test_utils.py
import unittest
from health.data_analysis import analyze_workouts  # Измените путь на правильный модуль
from datetime import datetime
import pandas as pd

class TestUtils(unittest.TestCase):
    def setUp(self):
        # Создание тестовых данных
        self.test_data = pd.DataFrame([
            {'Date': datetime(2024, 7, 28), 'Type': 'cycling', 'Duration': 45, 'Calories': 400},
            {'Date': datetime(2024, 7, 29), 'Type': 'running', 'Duration': 30, 'Calories': 300},
        ])

    def test_analyze_workouts(self):
        # Тестирование функции analyze_workouts
        recommendations = analyze_workouts(self.test_data)
        self.assertIsInstance(recommendations, list)
        self.assertGreater(len(recommendations), 0)

if __name__ == '__main__':
    unittest.main()

