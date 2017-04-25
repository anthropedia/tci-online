from flask import Flask, render_template


app = Flask(__name__)


@app.route('/')
def home():
    return render_template('error.html')


@app.route('/<string:token>')
def survey(token):
    return render_template('survey.html')


@app.route('/end', methods=['post'])
def end():
    return render_template('end.html')
