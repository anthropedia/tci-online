from unittest import TestCase
from tcidatabase.models import User, SurveyToken, Client, Score

from core import app, db
from core.views import *


class TciTest(TestCase):
    def setUp(self):
        provider = User(email='user@test.net').save()
        client = Client(provider=provider, lastname='Jack').save()
        self.token = SurveyToken(client=client, provider=provider,
                                 survey='tcims').save()
        self.client = app.test_client()
        self.client.testing = True

    def tearDown(self):
        User.objects.first().delete()
        Client.objects.first().delete()
        SurveyToken.objects.first().delete()
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
        self.assertIn(b'Thank you for completing the test.', result.data)
        self.assertEqual(Score.objects.count(), 1)
        score = Score.objects.first()
        Score.objects.first().delete()
        self.assertEqual(score.answers, [2, 3, 4])
        self.assertEqual(score.times, [1000, 1500, 1600])
        self.assertEqual(score.survey, 'tcims')
        token = SurveyToken.objects.first()
        self.assertEqual(score.client.email, token.client.email)
        self.assertFalse(token.is_valid)

    def test_run_tci_with_page_reload(self):
        self.client.get('/' + self.token.key)
        result = self.client.get('/' + self.token.key)
        self.assertIn(b'Definitely True', result.data)
