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

from Constants import (
    OUTER_PATH,
    STATIC_CONAN_FILE_NAME
)
from core.BotLogger import BotLogger
from core.UI.Backend import Backend
from core.util.Utiltilies import (
    str_user_input,
    int_user_input
)
from core.util.Wrappers import (
    safe_log
)


class IInterface:
    """
    Abstract interface class
    """
    frontend_local_logger = BotLogger()  # local frontend logger
    backend: Backend = Backend()  # backend object to interact with logic

    @abc.abstractmethod
    def run_app(self):
        pass


class Web_interface(IInterface):
    __web_interface: Flask = Flask(__name__, static_url_path='/static')  # flask interface object

    def __init__(self):
        pass

    @safe_log
    def run_app(self):
        self.__web_interface.run()
        self.backend.init_conan()

    @__web_interface.route('/', methods=['GET'])
    def home_page(self=None):
        path_to_conan_file: str = OUTER_PATH + STATIC_CONAN_FILE_NAME
        if not exists(path_to_conan_file):
            return redirect(url_for('start_page'))
        return render_template('home.html')

    @__web_interface.route('/about', methods=['GET'])
    def about_page(self=None):
        return render_template('about.html')

    @__web_interface.route('/start_page', methods=['GET'])
    def start_page(self=None):
        data = request.data
        return render_template('start_page.html')

    @__web_interface.route('/parameters', methods=['GET'])
    def see_parameters_page(self=None):
        """
        Page with conan parameters
        :return: None
        """
        return render_template('parameters.html')


class Console_interface(IInterface):
    """
    Simple console interface to interact with
    """

    def __init__(self):
        pass

    @safe_log
    def run_app(self):
        self.backend.init_conan()
        while True:
            print('Choose action by its number:')
            print('1. Update dependencies')
            print('2. Remove dependency')
            print('3. Add dependency')
            print('4. Exit')
            user_choice = int_user_input(1, 4)
            match user_choice:
                case 1:
                    self.frontend_local_logger.log('User choose update dependency')
                    self.backend.update_dependencies()  # update conan state
                case 2:
                    self.frontend_local_logger.log('User choose remove dependency')
                    while True:
                        print('Write dependency name to remove:')
                        dep_to_rm = str_user_input()
                        if dep_to_rm != '':
                            self.backend.remove_dependencies(dep_to_rm)
                            break
                        else:
                            continue
                case 3:
                    self.frontend_local_logger.log('User choose add dependency')
                    dep_name: str = ''
                    dep_version: str = ''
                    while True:
                        print('Write dependency name to add:')
                        dep_to_add = input('>> ')
                        if dep_to_add != '':
                            dep_name = dep_to_add
                            break
                        else:
                            continue
                    while True:
                        print('Write dependency version or leave it blank:')
                        dep_ver_to_add = input('>> ')
                        if dep_to_add != '' or dep_ver_to_add == '':
                            dep_version = dep_ver_to_add
                            break
                        else:
                            continue
                    self.backend.add_dependencies(dep_name, dep_version)
                case 4:
                    break
                case _:
                    raise Exception('Unknown statement')  # might be just message
