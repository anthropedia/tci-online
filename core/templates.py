from flask import request
from tcii18n.template import flask_methods

from . import app


def get_translations_file():
    supported_languages = app.config.get('TRANSLATION_FILES').keys()
    lang = (request.accept_languages.best_match(supported_languages) or
            supported_languages[0])
    return app.config.get('TRANSLATION_FILES').get(lang)

flask_methods(app, get_translations_file)
