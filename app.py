from flask import Flask, render_template, request
from tcidatabase.models import Token, Score
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
        token_object = Token.objects.get(key=token, usage_date=None)
    except Token.DoesNotExist:
        return render_template('error.html')
    tci = get_tci(token_object.survey)
    questions = tci.get('questions')
    return render_template('survey.html', questions=questions, token=token)


@app.route('/end', methods=['post'])
def end():
    token = Token.objects.get(key=request.form.get('token'))
    answers = request.form.get('answers').split(',')
    times = request.form.get('times').split(',')
    Score(user=token.user, answers=answers, times=times).save()
    token.void()
    return render_template('end.html')
