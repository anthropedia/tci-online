from flask import render_template, request, abort, redirect, url_for, g
from tcidatabase.models import SurveyToken, Score
from tcidata import get_tci

from . import app


"""
The following 2 functions take care of automagically prepending the `lang_code`
into the url and reading from it.
See http://flask.pocoo.org/docs/0.12/patterns/urlprocessors/.
"""


@app.url_defaults
def add_language_code(endpoint, values):
    if 'lang_code' in values or not g.lang_code:
        return
    if app.url_map.is_endpoint_expecting(endpoint, 'lang_code'):
        values['lang_code'] = g.lang_code


@app.url_value_preprocessor
def pull_lang_code(endpoint, values):
    g.lang_code = (values.pop('lang_code',
                              app.config.get('DEFAULT_LANGUAGE', 'en')))


@app.route('/')
def default_home():
    return redirect(url_for('home'))


@app.route('/<string:token>')
def default_survey(token):
    return redirect(url_for('survey', token=token))


@app.route('/<string(length=2):lang_code>')
def home():
    return render_template('error.html'), 401


@app.route('/<lang_code>/<string:token>')
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


@app.route('/<lang_code>/end', methods=['post'])
def end():
    token = SurveyToken.objects.get(key=request.form.get('token'))
    answers = [int(a) for a in request.form.get('answers').split(',')]
    times = [int(t) for t in request.form.get('times').split(',')]
    Score(client=token.client, answers=answers, times=times,
          survey=token.survey).save()
    token.void()
    return render_template('end.html')
