"""
Zenna backend
"""

from os.path import exists

from Constants import (
    IN_APP_SETTINGS_NAME,
    INNER_PATH, OUTER_PATH,
    STATIC_CONAN_FILE_NAME
)
from core.BotLogger import BotLogger
from core.entities.CMD import CMD
from core.entities.Cmake_cmd import Cmake_cmd
from core.entities.Conan_profile import Conan_profile
from core.entities.Make_cmd import Make_cmd
from core.entities.Meson_cmd import Meson_cmd
from core.util.Utiltilies import str_user_input
from core.util.Wrappers import (
    safe_log,
    log
)


class Backend:
    # Global backend entities:
    __cmd: CMD
    __profile: Conan_profile = Conan_profile(False)
    __backend_local_logger: BotLogger = BotLogger()

    @safe_log
    def build_sys_fabric(self, cmd_name: str = 'cmake'):
        """
        Build system fabric to build build system
        :param cmd_name: name of the build system
        :return: Build system object
        """
        match cmd_name:
            case 'cmake':
                self.__backend_local_logger.log('Choose cmake')
                return Cmake_cmd()
            case 'make':
                self.__backend_local_logger.log('Choose make')
                return Make_cmd()
            case 'meson':
                self.__backend_local_logger.log('Choose meson')
                return Meson_cmd()
            case _:
                raise NotImplementedError('Implement build system object first')

    @log
    def decide_build_system(self):
        if exists(INNER_PATH + IN_APP_SETTINGS_NAME):
            self.__backend_local_logger.log('In app settings exists')
            with open(IN_APP_SETTINGS_NAME, 'r') as settings:
                build_sys_name = settings.read().strip()
                self.__backend_local_logger.log(f'Choose build system from settings - {build_sys_name}')
                self.__cmd = self.build_sys_fabric(build_sys_name)
        else:
            while True:
                pass

    @log
    def create_app_settings(self):
        """
        Create application settings
        :return: None
        """
        with open(INNER_PATH + IN_APP_SETTINGS_NAME, 'w+') as settings_file:
            settings_file.write('cmake')  # write cmake as a default build system
            self.__backend_local_logger.log('Created in app settings')

    @log
    def init_conan(self):
        path_to_conan_file = OUTER_PATH + STATIC_CONAN_FILE_NAME  # outer path to conan file, outside Zenna project
        if exists(path_to_conan_file):
            print(f'Conan file exists on path "{path_to_conan_file}"')
        else:
            print('Conan file does not exists')
            print('Would you like to create temporary conan profile? (yes / y)')
            while True:
                user_input = str_user_input(True)
                if user_input == 'yes' or user_input == 'y':
                    while True:
                        print('Which build type create - (build or release)')
                        build_sys_type: str = str_user_input(False)
                        if build_sys_type == 'build' or build_sys_type == 'release':
                            Conan_profile.tmp_conan_file(build_sys_type)
                            break
                        else:
                            print('Try again')
                            continue
                    break
                else:
                    break
        self.__profile.init_with_conan_file()

    @log
    def add_dependencies(self, dep_name: str, dep_ver: str):
        """
        Add dependency into profile
        :param dep_name: name of the dependency
        :param dep_ver: dependency version
        :return: None
        """
        if dep_name != '' or (dep_name != '' and dep_ver != ''):
            self.__profile.conan_fields.add_dependency(dep_name, dep_ver)
        else:
            raise Exception('Dependency name or dependency version should not be empty string')

    @log
    def remove_dependencies(self, dep_name: str):
        """
        Remove dependency into profile
        :param dep_name: name of the dependency
        :return: None
        """
        if dep_name != '':
            self.__profile.conan_fields.remove_dependency(dep_name)
        else:
            raise Exception('Dependency name should not be empty string')

    @log
    def update_dependencies(self):
        """
        Update conan dependencies
        :return: None
        """
        self.__cmd.update_dependencies()

    @log
    def show_path_to_config(self):
        """
        View in console for path to config
        :return: None
        """
        self.__cmd.get_profile()
