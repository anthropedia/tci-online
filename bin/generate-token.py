import os

from flask import Flask
from tcidatabase import db
from tcidatabase.models import BaseToken, SurveyToken, Client, User

PROJECT_PATH = os.path.abspath(os.path.dirname(__file__) + '/..')
os.environ.setdefault('SETTINGS', PROJECT_PATH + '/settings.py')

app = Flask('tci-online')
app.config.from_envvar('SETTINGS')

app.root_path = PROJECT_PATH
app.secret_key = app.config['SECRET_KEY']

db.connect(**app.config['DATABASE'])

User.objects.delete()
provider = User().save()
client = Client(provider=provider, lastname='Jack').save()
survey = SurveyToken(client=client, provider=provider, survey='tcims').save()
print(survey)
