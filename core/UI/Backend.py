"""
Zenna backend entity
"""

from os.path import exists

from Constants import (
    FULL_PATH_TO_ZENNA_FILE,
    Build_variants
)
from core.BotLogger import BotLogger
from core.entities.Bison_cmd import Bison_cmd
from core.entities.CMD import CMD
from core.entities.Cmake_cmd import Cmake_cmd
from core.entities.Make_cmd import Make_cmd
from core.entities.Meson_cmd import Meson_cmd
from core.entities.profiles.Conan_profile import Conan_profile
from core.entities.profiles.Zenna_profile import Zenna_profile
from core.util.Utiltilies import str_user_input
from core.util.Wrappers import (
    safe_log,
    log
)


class Backend:
    # Global backend entities:
    __cmd: CMD
    __profile: Conan_profile = Conan_profile(False)  # TODO need to create profiles separately
    __zenna_profile: Zenna_profile = None
    __backend_local_logger: BotLogger = BotLogger()

    @safe_log
    def build_sys_fabric(self, cmd_name: str = 'cmake'):
        """
        Build system fabric to build build system
        :param cmd_name: name of the build system
        :return: Build system object
        """
        if cmd_name is None:
            raise Exception('Build system cannot be None')
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
            case 'bison':
                self.__backend_local_logger.log('Choose bison')
                return Bison_cmd()
            case _:
                raise NotImplementedError('Implement build system object first')

    @log
    def check_zenna_file(self):
        """
        Check for zenna config file existence and continue with conan initialize
        :return: None
        """
        if exists(FULL_PATH_TO_ZENNA_FILE):  # outer path to conan file, outside Zenna project
            print(f'Zenna config file exists on path "{FULL_PATH_TO_ZENNA_FILE}"')
        else:
            print('Conan file does not exists')
            print('Would you like to create temporary zenna profile? (yes / y) or (no / n)')
            while True:
                user_input = str_user_input(null_safe_check=True)
                if user_input == 'yes' or user_input == 'y':
                    while True:
                        print(f'Which build type create - select on of (Debug or Release)')
                        build_sys_type: str = str_user_input(null_safe_check=False)
                        if build_sys_type == Build_variants.DEBUG or build_sys_type == Build_variants.RELEASE:
                            Zenna_profile.create_tmp_profile(Build_variants.create_build_variant(build_sys_type))
                            break
                        else:
                            print(f'Wrong input string {build_sys_type}, Try again')
                            continue
                    break
                else:
                    print('Utility cannot continue without zenna file')
                    exit(0)
        self.__zenna_profile = Zenna_profile()  # create before act
        self.__zenna_profile.init_profile()  # read zenna profile
        self.__cmd = self.build_sys_fabric(self.__zenna_profile.get_build_system())

    @log
    def add_dependencies(self, dep_name: str, dep_ver: str):
        """
        Add dependency into profile
        :param dep_name: name of the dependency
        :param dep_ver: dependency version
        :return: None
        """
        if dep_name != '' or (dep_name != '' and dep_ver != ''):
            self.__zenna_profile.add_dependency(dep_name, dep_ver)
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
            self.__zenna_profile.remove_dependency(dep_name)
        else:
            raise Exception('Dependency name should not be empty string')

    @log
    def update_dependencies(self):
        """
        Update conan dependencies
        :return: None
        """
        if self.__cmd is not None:
            self.__cmd.update_dependencies()
        else:
            pass

    @log
    def get_dependencies(self) -> dict[str, str]:
        """
        Get profile dependencies
        :return: None
        """
        return self.__zenna_profile.get_dependencies()

    @log
    def show_path_to_config(self):
        """
        View in console for path to config
        :return: None
        """
        if self.__cmd is not None:
            self.__cmd.get_profile()
        else:
            pass

    @log
    def compile_conan_file(self):
        """
        Compile conan file (s) and create files
        :return: None
        """
        types_to_compile: list = self.__zenna_profile.get_build_types()
        if len(types_to_compile) > 0:
            for type in types_to_compile:
                print(f'Compiling type - {type}')
                self.__profile.save_profile()  # TODO change from tmp configs to real
        else:
            raise Exception('Cannot compile zero len compile list')

    @log
    def get_zenna_profile(self) -> Zenna_profile | None:
        if self.__zenna_profile is not None:
            return self.__zenna_profile
        else:
            return None
