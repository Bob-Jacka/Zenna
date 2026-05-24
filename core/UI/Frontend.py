"""
Zenna frontend entity
"""

import abc
from abc import ABC
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
    STATIC_ZENNA_FILE_NAME
)
from core.BotLogger import BotLogger
from core.UI.Backend import Backend
from core.entities.profiles.Zenna_profile import Zenna_profile
from core.util.Utiltilies import (
    str_user_input,
    int_user_input
)
from core.util.Wrappers import (
    log
)

_backend: Backend = Backend()  # Global backend object to interact with logic
_frontend_local_logger: BotLogger = BotLogger()  # local frontend logger


class Cache:
    profile_ptr: Zenna_profile = None


class IInterface(ABC):
    """
    Abstract interface class
    """

    @abc.abstractmethod
    def run_app(self):
        pass


class Web_interface(IInterface):
    __web_interface: Flask = Flask(__name__, static_url_path='/static')  # flask interface object

    def __init__(self):
        pass

    @log
    def run_app(self):
        self.__web_interface.run()

    @staticmethod
    @__web_interface.route('/', methods=['GET'])
    def home_page():
        path_to_zenna_file: str = OUTER_PATH + STATIC_ZENNA_FILE_NAME
        if not exists(path_to_zenna_file):
            return redirect(url_for('start_page'))
        return render_template('home_page.html')

    @staticmethod
    @__web_interface.route('/about_page', methods=['GET'])
    def about_page():
        return render_template('about_page.html')

    @staticmethod
    @__web_interface.route('/start_page', methods=['GET', 'POST'])
    def start_page():
        if request.method == 'POST':
            name = request.form.get('name')
            version = request.form['version']
            requires = request.form.getlist('requires[]')
            build_systems = request.form.getlist('build_systems[]')
            build_types = request.form.getlist('build_types[]')

            new_profile = Zenna_profile()
            new_profile.init_profile_with_data('', name, version, build_types, build_systems, requires)
            Cache.profile_ptr = new_profile

            if Cache.profile_ptr is not None:
                _frontend_local_logger.log('Using profile value from cache')
                zenna_profile_ptr = Cache.profile_ptr
            else:
                zenna_profile_ptr = None
            zenna_profile_ptr.swap(new_profile)  # swap existing profile with new one
            zenna_profile_ptr.save_profile()
            Cache.profile_ptr = zenna_profile_ptr
            return redirect(url_for('home_page'))
        return render_template('start_page.html')

    @staticmethod
    @__web_interface.route('/parameters_page', methods=['GET'])
    def see_parameters_page():
        """
        Page with zenna parameters
        :return: None
        """
        if Cache.profile_ptr is not None:
            _frontend_local_logger.log('Using profile value from cache')
            zenna_profile_ptr = Cache.profile_ptr
        else:
            zenna_profile_ptr = Zenna_profile()
            zenna_profile_ptr.init_profile()  # re init profile
            Cache.profile_ptr = zenna_profile_ptr
        if zenna_profile_ptr is None:
            return redirect(url_for('start_page'))
        return render_template('parameters_page.html', parameters=zenna_profile_ptr)

    @staticmethod
    @__web_interface.route('/change_config_page', methods=['GET', 'POST'])
    def change_config_page():
        if Cache.profile_ptr is not None:
            _frontend_local_logger.log('Using profile value from cache')
            zenna_profile_ptr = Cache.profile_ptr
        else:
            zenna_profile_ptr = _backend.get_zenna_profile()
            Cache.profile_ptr = zenna_profile_ptr

        if zenna_profile_ptr is None:
            return redirect(url_for('start_page'))

        # Post branch
        if request.method == 'POST':
            name = request.form.get('name')
            version = request.form['version']
            requires = request.form.getlist('requires[]')
            build_systems = request.form.getlist('build_systems[]')
            build_types = request.form.getlist('build_types[]')

            new_profile = Zenna_profile()
            new_profile.init_profile_with_data('', name, version, build_types, build_systems, requires)

            if zenna_profile_ptr != new_profile:
                new_profile.profile_version = str(int(version) + 1)  # ugly code to update config version only when update

            zenna_profile_ptr.swap(new_profile)
            zenna_profile_ptr.save_profile()

            Cache.profile_ptr = zenna_profile_ptr  # update cache
            return redirect(url_for('home_page'))
        return render_template('change_config_page.html', parameters=zenna_profile_ptr)

    @staticmethod
    @__web_interface.route('/conan_profile_page', methods=['GET'])
    def see_conan_profile_page():
        """
        Page for preview conan profile
        """
        if Cache.profile_ptr is not None:
            _frontend_local_logger.log('Using profile value from cache')
            zenna_profile_ptr = Cache.profile_ptr
        else:
            zenna_profile_ptr = _backend.get_zenna_profile()
            Cache.profile_ptr = zenna_profile_ptr
        if zenna_profile_ptr is None:
            return redirect(url_for('start_page'))
        return render_template('conan_profile_page.html')


class Console_interface(IInterface):
    """
    Simple console interface to interact with
    """

    def __init__(self):
        pass

    @log
    def dep_menu(self):
        while True:
            print()  # just new line
            print('Choose dependency action:')
            print('1. Add dependency')
            print('2. Remove dependency')
            print('3. Update dependency')
            print('4. View all dependencies')
            print('5. Exit menu')
            user_choice = int_user_input(1, 5)
            match user_choice:
                case 1:
                    _frontend_local_logger.log('User choose add dependency')
                    dep_name: str = ''
                    dep_version: str = ''

                    print('Write dependency name to add:')
                    dep_to_add = str_user_input(True)
                    dep_name = dep_to_add
                    while True:
                        print('Write dependency version or leave it blank:')
                        dep_ver_to_add = input('>> ')
                        if dep_to_add != '' or dep_ver_to_add == '':
                            dep_version = dep_ver_to_add
                            break
                        else:
                            continue
                    _backend.add_dependencies(dep_name, dep_version)

                case 2:
                    _frontend_local_logger.log('User choose remove dependency')
                    while True:
                        print('Write dependency name to remove:')
                        dep_to_rm = str_user_input(True)
                        _backend.remove_dependencies(dep_to_rm)

                case 3:
                    _frontend_local_logger.log('User choose update dependency')
                    _backend.update_dependencies()  # update conan state

                case 4:
                    deps: dict = _backend.get_dependencies()
                    if len(deps) > 0:
                        for depend_name, dep_ver in deps.items():
                            print(f'Dependency name: {depend_name} ',
                                  f'with version {dep_ver}' if dep_ver != '' else '')
                    else:
                        print('No dependencies found in config')

                case 5:
                    break

    @log
    def run_app(self):
        _backend.check_zenna_file()
        while True:
            print()  # just new line symbol
            print('Choose action by its number:')
            print('0. Compile conan file')
            print('1. Dependency menu...')
            print('2. Exit')
            user_choice = int_user_input(0, 2)
            match user_choice:
                case 0:
                    _frontend_local_logger.log('User choose compile conan file')
                    _backend.compile_conan_file()
                case 1:
                    self.dep_menu()
                case 2:
                    _frontend_local_logger.log('User choose exit this frontend menu')
                    break
                case _:
                    raise Exception('Unknown statement')  # might be just message
