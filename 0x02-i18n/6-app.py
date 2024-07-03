#!/usr/bin/env python3
""" Basic Flask-Babel app """
import re
from flask import Flask, render_template, request, g
from flask_babel import Babel


class Config:
    """ Configurations for Flask-Babel app """
    LANGUAGES = ["en", "fr"]


app = Flask(__name__)
app.config_class = Config
app.config['LANGUAGES'] = Config.LANGUAGES
app.config['BABEL_DEFAULT_LOCALE'] = 'en'
app.config['BABEL_DEFAULT_TIMEZONE'] = 'UTC'
app.url_map.strict_slashes = False
babel = Babel(app)
users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}


def get_user(id=None):
    """ Returns a user dictionary """
    try:
        return users.get(int(id), None)
    except Exception:
        return None


@app.before_request
def before_request():
    """ Finds a user if any, and set it as a global on `flask.g.user` """
    queries = request.query_string.decode('utf-8').split('&')
    query_table = dict(map(
        lambda x: (x if '=' in x else '=').split('='),
        queries,
    ))
    login_id = query_table.get('login_as', '')
    user = get_user(login_id)
    setattr(g, 'user', user)


@babel.localeselector
def get_locale():
    """ Forces locale """
    queries = request.query_string.decode('utf-8').split('&')
    query_table = dict(map(
        lambda x: (x if '=' in x else '=').split('='),
        queries,
    ))
    locale = query_table.get('locale', '')
    if locale in app.config_class.LANGUAGES:
        return locale
    user_details = getattr(g, 'user', None)
    if user_details is not None:
        if user_details['locale'] in app.config_class.LANGUAGES:
            return user_details['locale']
    langs = re.split('[,;]', str(request.accept_languages))
    for lang in langs:
        if lang in app.config_class.LANGUAGES:
            return lang
    return app.config['BABEL_DEFAULT_LOCALE']


@app.route('/')
def index():
    """ Renders `6-index` page """
    user_details = getattr(g, 'user', None)
    ctxt = {
        'login_details': user_details,
    }
    return render_template('6-index.html', **ctxt)


if __name__ == '__main__':
    app.run()
