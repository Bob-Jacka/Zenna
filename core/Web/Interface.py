from flask import Flask

from core.util.Wrappers import log

flasky: Flask


@log
def init_interface():
    global flasky
    flasky = Flask(__name__, static_url_path='static')


@flasky.route('/', methods=['GET'])
def home_page():
    pass
