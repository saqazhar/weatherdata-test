import unittest
from app import app

class WeatherAPITestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_get_weather(self):
        response = self.app.get('/api/weather')
        self.assertEqual(response.status_code, 200)
        # self.assertIn('data', response.json)

    def test_get_weather_stats(self):
        response = self.app.get('/api/weather/stats')
        self.assertEqual(response.status_code, 200)
        # self.assertIn('data', response.json)

if __name__ == '__main__':
    unittest.main()
