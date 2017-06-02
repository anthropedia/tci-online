from flask import request, Markup
from tcii18n.template import flask_methods

import gfm

from . import app


def get_translations_file():
    supported_languages = app.config.get('TRANSLATION_FILES').keys()
    lang = (request.accept_languages.best_match(supported_languages) or
            supported_languages[0])
    return app.config.get('TRANSLATION_FILES').get(lang)

flask_methods(app, get_translations_file)


@app.template_filter('markdown')
def markdown_filter(string):
    return Markup(gfm.markdown(gfm.gfm(string)))
