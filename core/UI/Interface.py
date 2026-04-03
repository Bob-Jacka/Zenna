from os.path import exists

from flask import (
    Flask,
    render_template,
    redirect,
    url_for,
    request
)

from App import outer_path
from core.BotLogger import BotLogger
from core.util.Wrappers import safe_log

__web_interface: Flask = Flask(__name__, static_url_path='/static')
frontend_local_logger = BotLogger()


# Zenna frontend

@safe_log
def run_web_app():
    __web_interface.run()


@__web_interface.route('/', methods=['GET'])
def home_page():
    path_to_conan_file = outer_path + 'conanfile.py'
    if not exists(path_to_conan_file):
        return redirect(url_for('start_page'))
    return render_template('home.html')


@__web_interface.route('/about', methods=['GET'])
def about_page():
    return render_template('about.html')


@__web_interface.route('/start_page', methods=['GET'])
def start_page():
    data = request.data
    return render_template('start_page.html')


@__web_interface.route('/parameters', methods=['GET'])
def see_parameters_page():
    """
    Page with conan parameters
    :return:
    """
    return render_template('parameters.html')
