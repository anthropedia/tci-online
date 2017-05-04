from flask import Flask, render_template, request
from tcidatabase.models import Token
from tcidatabase import db
from tcidata import get_tci


app = Flask(__name__)

db.connect(db='tci', username='', password='', host='localhost', port=27017)


@app.route('/')
def home():
    return render_template('error.html')


@app.route('/<string:token>')
def survey(token):
    try:
        Token.objects.get(key=token, usage_date=None)
    except Token.DoesNotExist:
        return render_template('error.html')
    tci = get_tci('tcims')
    questions = tci.get('questions')
    return render_template('survey.html', questions=questions)


@app.route('/end', methods=['post'])
def end():
    return render_template('end.html')
