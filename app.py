from flask import Flask, render_template
from tcidatabase.models import Token
from tcidatabase import db

app = Flask(__name__)

db.connect(db='tci', username='', password='', host='localhost',
           port=27017)


@app.route('/')
def home():
    return render_template('error.html')


@app.route('/<string:token>')
def survey(token):
    try:
        verify_token = Token.objects.get(key=token, usage_date=None)
    except Token.DoesNotExist:
        return render_template('error.html')
    return render_template('survey.html')


@app.route('/end', methods=['post'])
def end():
    return render_template('end.html')
