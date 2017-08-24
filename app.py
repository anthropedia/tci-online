from core import app
from core import views, templates  # noqa: F401


# WSGI
application = app

if __name__ == '__main__':
    app.run(debug=app.config.get('DEBUG'), host=app.config.get('HOST'),
            port=app.config.get('PORT'))
