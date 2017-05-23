from flask import render_template, request, abort
from tcidatabase.models import SurveyToken, Score
from tcidata import get_tci

from . import app


@app.route('/')
def home():
    return render_template('error.html'), 401


@app.route('/<string:token>')
def survey(token):
    try:
        token = SurveyToken.objects.get(key=token, usage_date=None)
    except SurveyToken.DoesNotExist:
        return render_template('error.html'), 401
    try:
        tci = get_tci(token.survey)
    except NotImplementedError:
        abort(501, 'The token has a inexisting "{}" survey associated.'.format(
              token.survey))
    questions = tci.get('questions')
    return render_template('survey.html', questions=questions, token=token)


@app.route('/end', methods=['post'])
def end():
    token = SurveyToken.objects.get(key=request.form.get('token'))
    answers = [int(a) for a in request.form.get('answers').split(',')]
    times = [int(t) for t in request.form.get('times').split(',')]
    Score(client=token.client, answers=answers, times=times,
          survey=token.survey).save()
    token.void()
    return render_template('end.html')
