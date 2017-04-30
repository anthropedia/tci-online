from unittest import TestCase
from tcidatabase.models import User, Token, Score

from core import app, db
from core.views import *


class TciTest(TestCase):
    def setUp(self):
        self.token = Token(user=User().save(), survey='tcims').save()
        self.client = app.test_client()
        self.client.testing = True

    def tearDown(self):
        database = db.connection.get_connection()
        database.drop_database('tci_test')

    def test_home_page(self):
        result = self.client.get('/')
        self.assertEqual(result.status_code, 401)

    def test_wrong_token(self):
        result = self.client.get('/wrongtoken')
        self.assertEqual(result.status_code, 401)

    def test_run_tci(self):
        result = self.client.get('/' + self.token.key)
        self.assertEqual(result.status_code, 200)

    def test_post_data(self):
        data = {'token': self.token.key,
                'answers': '2,3,4',
                'times': '1000,1500,1600'
                }
        self.assertEqual(Score.objects.count(), 0)
        result = self.client.post('/end', data=data)
        self.assertEqual(result.status_code, 200)
        self.assertIn(b'You have completed', result.data)
        self.assertEqual(Score.objects.count(), 1)
        score = Score.objects.first()
        self.assertEqual(score.answers, [2, 3, 4])
        self.assertEqual(score.times, [1000, 1500, 1600])
        self.assertEqual(score.survey, 'tcims')
        token = Token.objects.first()
        self.assertEqual(score.user, token.user)
        self.assertFalse(token.is_valid)

    def test_run_tci_with_page_reload(self):
        self.client.get('/' + self.token.key)
        result = self.client.get('/' + self.token.key)
        self.assertIn(b'Definitely True', result.data)
