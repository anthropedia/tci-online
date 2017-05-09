#/bin/bash

import os

from flask import Flask, render_template
from tcidatabase import db
from tcidatabase.models import Token, User

db.connect(db='tci_test', username='', password='', host='localhost',
           port=27017)

database = db.connection.get_connection()
database.drop_database('tci_test')

token = Token(user=User().save(), survey='tcims').save()
print(token.key)
