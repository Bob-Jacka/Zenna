"""
Zenna frontend
"""

import abc
from os.path import exists

from flask import (
    Flask,
    render_template,
    redirect,
    url_for,
    request
)

from App import OUTER_PATH
from core.BotLogger import BotLogger
from core.util.Wrappers import (
    safe_log,
    log
)


class Interface:
    """
    Abstract interface class
    """
    frontend_local_logger = BotLogger()

    @abc.abstractmethod
    def run_app(self):
        pass


class Web_interface(Interface):
    __web_interface: Flask = Flask(__name__, static_url_path='/static')

    @safe_log
    def run_app(self):
        self.__web_interface.run()

    @__web_interface.route('/', methods=['GET'])
    def home_page(self):
        path_to_conan_file = OUTER_PATH + 'conanfile.py'
        if not exists(path_to_conan_file):
            return redirect(url_for('start_page'))
        return render_template('home.html')

    @__web_interface.route('/about', methods=['GET'])
    def about_page(self):
        return render_template('about.html')

    @__web_interface.route('/start_page', methods=['GET'])
    def start_page(self):
        data = request.data
        return render_template('start_page.html')

    @__web_interface.route('/parameters', methods=['GET'])
    def see_parameters_page(self):
        """
        Page with conan parameters
        :return:
        """
        return render_template('parameters.html')


@log
class Console_interface(Interface):

    @safe_log
    def run_app(self):
        while True:
            print('Choose action by its number')
            print('1. Update dependencies')
            print('2. Remove dependencies')
            print('3. Update dependencies')
            print('4. Update dependencies')
            user_choice = int(input('>> '))
            match user_choice:
                case 1:
                    pass
                case 2:
                    pass
                case 3:
                    pass
                case 4:
                    pass
                case _:
                    pass
