import dataclasses
from enum import Enum

from Constants import (
    FULL_PATH_TO_ZENNA_FILE,
    Build_variants
)
from core.entities.profiles.Abstract_profile import Abstract_profile
from core.util.Utiltilies import int_user_input, print_list_elems, to_list, to_map


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

    namespace: str
    profile_name: str
    profile_version: str

    # complex types:
    build_types: list[str]  # which type to build
    build_systems: list[str]  # which build systems to use (ex. cmake or make)
    build_requires: dict[str, str]

    def __init__(self):
        self.namespace = ''
        self.profile_name = ''
        self.profile_version = ''
        self.build_types = list()
        self.build_systems = list()
        self.build_requires = dict()

    def init_profile(self):
        """
        Initialize zenna profile with data file
        :return: None
        """
        with open(FULL_PATH_TO_ZENNA_FILE, 'r+') as file:
            file_data = file.readlines()  # ignore import directive and class signature

            for field_line in file_data:
                field_parameters: list = field_line.split('=', 1)  # field might contain several '=' symbol, and then 1 split
                if len(field_parameters) > 1:
                    field_namespace_and_name = field_parameters[0].strip().split('.')  # clear unuseful whitespaces
                    field_value = field_parameters[1].strip()  # clear unuseful whitespaces

                    self.namespace = field_namespace_and_name[0]  # assign namespace to inner

                    match field_namespace_and_name[1]:  # search by field name
                        case _Zenna_proto.BUILD_TYPE:
                            self.build_types = to_list(field_value.split(', '))

                        case _Zenna_proto.NAME:
                            self.profile_name = field_value

                        case _Zenna_proto.NAMESPACE:
                            self.namespace = field_value

                        case _Zenna_proto.VERSION:
                            self.profile_version = field_value

                        case _Zenna_proto.REQ:
                            self.build_requires = to_map(field_value.split(', '))  # TODO error, assign list to dict entity

                        case _Zenna_proto.B_SYSTEMS:
                            self.build_systems = to_list(field_value.split(', '))

                        case _:
                            print(f'Unknown parameter name "{field_namespace_and_name[1]}" with value "{field_value}"')

    def init_profile_with_data(self, namespace, profile_name: str, profile_version, build_types, build_systems,
                               build_requires):
        self.namespace = namespace
        self.profile_name = profile_name
        self.profile_version = profile_version
        self.build_types = build_types
        self.build_systems = build_systems
        self.build_requires = build_requires

    def generate_conan_profile(self):
        """
        Generate conan profile file
        :return: None
        """
        pass

    def add_dependency(self, dependency_name: str, dependency_version: str = '') -> None:
        self.build_requires[dependency_name] = dependency_version

    def remove_dependency(self, dependency_name: str) -> None:
        del self.build_requires[dependency_name]

    def get_namespace(self) -> str:
        return self.namespace

    def get_dependencies(self) -> dict[str, str]:
        return self.build_requires

    def get_build_system(self) -> str | list[str]:
        """
        Get build system from Zenna profile
        :return: build system string value
        """
        if len(self.build_systems) > 1:
            print()  # just new line
            print('Detected several build systems, choose one to init:')
            for int_counter, build_sys in enumerate(self.build_systems):
                print(f'{int_counter}: {build_sys}')
            user_choice = int_user_input(0, len(self.build_systems) - 1)  # TODO can cause a problem
            return self.build_systems[user_choice]
        else:
            return ''

    def get_build_types(self) -> list:
        return self.build_types

    def swap(self, other: Zenna_profile):
        self.namespace = other.namespace
        self.profile_name = other.profile_name
        self.profile_version = other.profile_version
        self.build_types = other.build_types
        self.build_systems = other.build_systems
        self.build_requires = other.build_requires
        other = None

    def save_profile(self):
        """
        Save profile in outer directory of the project
        """
        with open(FULL_PATH_TO_ZENNA_FILE, 'w+') as save_file:
            save_file.write(f'profile.name = {self.profile_name}\n')
            save_file.write(f'profile.version = {self.profile_version}\n')
            save_file.write(f'profile.requires = {self.build_requires}\n')
            save_file.write(f'profile.build_systems = {print_list_elems(self.build_systems, False)}\n')
            save_file.write(f'profile.build_types = {print_list_elems(self.build_types, False, Build_variants.stringify)}\n')

    @staticmethod
    def create_tmp_profile(build_type: Build_variants) -> None:
        """
        Create tmp conan file with default parameters
        TODO change to printer util class
        :return: None
        """
        print('Creating temporary zenna config file')
        with open(FULL_PATH_TO_ZENNA_FILE, 'w+') as file:
            file.write('profile.name = temporary\n')
            file.write('profile.version = 1\n')
            file.write('profile.requires = qt\n')
            file.write('profile.build_systems = cmake\n')
            file.write(f'profile.build_types = {build_type.value}\n')
