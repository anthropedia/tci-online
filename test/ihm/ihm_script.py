#/bin/bash

import os

from flask import Flask, render_template
from tcidatabase import db
from tcidatabase.models import Token, User
import tcidata

app = Flask(__name__)

db.connect(db='tci_test', username='', password='', host='localhost',
           port=27017)

database = db.connection.get_connection()
database.drop_database('tci_test')

token = Token(user=User().save(), survey='tcims').save()

os.system("node_modules/casperjs/bin/casperjs test test/ihm/tci.js "
          "--log-level=debug --token=" + token.key)
