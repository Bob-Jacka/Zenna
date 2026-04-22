import dataclasses
from enum import Enum

from Constants import (
    FULL_PATH_TO_ZENNA_FILE,
    Build_variants
)
from core.entities.profiles.Abstract_profile import Abstract_profile
from core.util.Utiltilies import int_user_input


class _Zenna_proto(str, Enum):
    NAMESPACE = 'namespace'
    BUILD_TYPE = 'build_types'
    NAME = 'name'
    VERSION = 'version'

    REQ = 'requires'
    B_SYSTEMS = 'build_systems'


@dataclasses.dataclass
class Zenna_profile(Abstract_profile):
    """
    Class wrapper for zenna profile
    """

    _namespace: str
    _profile_name: str
    _profile_version: str

    # complex types:
    _build_types: list[str]  # which type to build
    _build_systems: list[str]  # which build systems to use (ex. cmake or make)
    _build_requires: dict[str, str]

    def __init__(self):
        self._build_types = list()
        self._build_systems = list()
        self._build_requires = dict()

    def init_profile(self):
        """
        Initialize zenna profile with data file
        :return: None
        """
        with open(FULL_PATH_TO_ZENNA_FILE, 'r+') as file:
            file_data = file.readlines()  # ignore import directive and class signature TODO can cause a problem due to import directives in real files

            for field_line in file_data:
                field_parameters: list = field_line.split('=', 1)  # field might contain several '=' symbol, and then 1 split
                if len(field_parameters) > 1:
                    field_namespace_and_name = field_parameters[0].strip().split('.')  # clear unuseful whitespaces
                    field_value = field_parameters[1].strip()  # clear unuseful whitespaces

                    self._namespace = field_namespace_and_name[0]  # assign namespace to inner

                    match field_namespace_and_name[1]:  # search by field name
                        case _Zenna_proto.BUILD_TYPE:
                            self._build_types = field_value.split(', ')
                        case _Zenna_proto.NAME:
                            self._profile_name = field_value
                        case _Zenna_proto.NAMESPACE:
                            self._namespace = field_value
                        case _Zenna_proto.VERSION:
                            self._profile_version = field_value
                        case _Zenna_proto.REQ:
                            self._build_requires = self.__to_map(field_value.split(', '))  # TODO error, assign list to dict entity
                        case _Zenna_proto.B_SYSTEMS:
                            self._build_systems = field_value.split(', ')
                        case _:
                            print(f'Unknown parameter name "{field_namespace_and_name[1]}" with value "{field_value}"')

    def generate_conan_profile(self):
        """
        Generate conan profile file
        :return: None
        """
        pass

    def add_dependency(self, dependency_name: str, dependency_version: str = '') -> None:
        self._build_requires[dependency_name] = dependency_version

    def remove_dependency(self, dependency_name: str) -> None:
        del self._build_requires[dependency_name]

    def get_namespace(self) -> str:
        return self._namespace

    def get_dependencies(self) -> dict[str, str]:
        return self._build_requires

    def get_build_system(self) -> str | list[str]:
        """
        Get build system from Zenna profile
        :return: build system string value
        """
        if len(self._build_systems) > 1:
            print()  # just new line
            print('Detected several build systems, choose one to init:')
            int_counter = 0
            for build_sys in self._build_systems:
                print(f'{int_counter}: {build_sys}')
                int_counter += 1
            user_choice = int_user_input(0, len(self._build_systems) - 1)  # TODO can cause a problem
            return self._build_systems[user_choice]
        else:
            return self._build_systems[0]

    def get_build_types(self) -> list:
        return self._build_types

    @staticmethod
    def create_tmp_profile(build_type: Build_variants) -> None:
        """
        Create tmp conan file with default parameters
        TODO change to printer util class
        :return: None
        """
        print('Creating temporary zenna config file')
        with open(FULL_PATH_TO_ZENNA_FILE, 'w+') as file:
            file.write('profile.name = hello\n')
            file.write('profile.version = 0.1\n')
            file.write('profile.requires = qt\n')
            file.write('profile.build_systems = cmake\n')
            file.write(f'profile.build_types = {build_type}\n')

    @staticmethod
    def __to_map(to_conver: list[str]) -> dict:
        to_return: dict[str, str] = dict()
        for elem in to_conver:
            elem_name: str
            elem_ver: str
            split_elem_list = elem.split('\\')  # split by slash
            elem_name = split_elem_list[0].strip()
            if len(split_elem_list) != 1:
                elem_ver = split_elem_list[1].strip()
            else:
                elem_ver = ''
            to_return[elem_name] = elem_ver
        return to_return
