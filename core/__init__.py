import os

from flask import Flask
from tcidatabase import db

app = Flask(__name__)
app.debug = True
app.root_path = os.path.dirname(__file__) + '/..'

db.connect(db='tci_test', username='', password='', host='localhost',
           port=27017)
