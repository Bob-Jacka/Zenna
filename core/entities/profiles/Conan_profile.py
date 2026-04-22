import dataclasses
from enum import Enum
from typing import Literal

from Constants import (
    Build_variants,
    FULL_PATH_TO_CONAN_FILE
)
from core.entities.profiles.Abstract_profile import Abstract_profile
from core.util.Utiltilies import to_real_world_string


@dataclasses.dataclass
class _Fields:
    """
    Simple class for storing conan data field
    """

    Language = Literal['C', 'C++']  # literal type for language in conan file

    author: str
    name: str  # Name of the conan file
    version: str  # Version of the conan file
    requires: dict[str, str]  # Fields requires, key is dep name and value is version in string format
    generators: list[str]  # Build system generators
    homepage: str
    setting: str  # Settings field
    language: Language  # programming language

    deprecated: bool  # is profile deprecated

    def __init__(self):
        self.version = '"0.1"'
        self.requires = dict()
        self.generators = list()

    def enter_version(self, txt_ver: str) -> None:
        self.version = to_real_world_string(txt_ver)

    def add_generator(self, generator_str: str) -> None:  # TODO delete later
        self.generators.append(generator_str)

    def enter_name(self, new_name: str):  # TODO delete later
        self.name = new_name

    def contains_dependency(self, dependency_name: str) -> bool:
        return self.requires.__contains__(dependency_name)

    @staticmethod
    def to_gen_list(input_str: str) -> list:
        """
        Generators field
        :param input_str:
        :return:
        """
        return list()

    @staticmethod
    def to_req_dict(input_str: str) -> dict:
        """
        Requires field
        :param input_str:
        :return:
        """
        split_data = input_str.split(', ')
        return dict()


class _Conan_printer:
    """
    Print conan file with given fields parameters
    """
    is_print_by_fields: bool

    def __init__(self, is_print_fields: bool):
        """
        :param is_print_fields: is need to print separate methods or just fields in class
        """
        self.file_handler = None
        self.is_print_by_fields = is_print_fields

    def print(self, fields: _Fields) -> None:
        """
        Main entry point to printer class
        :param fields: fields in conan profile to print in file
        :return: None
        """
        self.file_handler = open(FULL_PATH_TO_CONAN_FILE)
        if self.file_handler is not None:
            self._file_write('from conan import ConanFile\n')
            self._file_write('from conan.tools.cmake import CMake, cmake_layout\n')
            self._file_write()
            self._file_write(f'class {fields.name}_profile(ConanFile):')
            if self.is_print_by_fields:
                self._print_with_fields()
            else:
                self._print_with_methods()
            self._file_write()
            # TODO
            self.file_handler.close()
        else:
            raise Exception('Print path is None')

    def _file_write(self, data: str = '\n', need_for_tab: bool = False) -> None:
        """
        Write to inner file
        :param data: data to write
        :return: None
        """
        if need_for_tab:
            self.file_handler.write('\t')
        self.file_handler.write(data + '\n')

    def _print_method_sig(self, method_name: str) -> None:
        pass

    def _print_with_methods(self):
        pass

    def _print_with_fields(self):
        pass


class _Conan_proto(str, Enum):
    """
    Conan prototype fields in profile
    """
    PROFILE_NAME = 'name'
    PROFILE_VER = 'version'
    PROFILE_REQ = 'requires'
    PROFILE_GEN = 'generators'

    PROFILE_OPT = 'options'
    PROFILE_SET = 'settings'
    PROFILE_AUT = 'author'
    # PROFILE_
    # PROFILE_
    # PROFILE_
    # PROFILE_
    # PROFILE_
    # PROFILE_
    # PROFILE_
    # PROFILE_


class Conan_profile(Abstract_profile):
    """
    Utility class for dealing with conan profile file
    """
    __conan_fields: _Fields
    __printer: _Conan_printer
    build_type: Build_variants  # duplicate in cmd

    def add_dependency(self, dependency_name: str, dependency_version: str = ''):
        """
        Add dependencies to conan profile
        :param dependency_name: name of the dependency
        :param dependency_version:
        :return:
        """
        self.__conan_fields.requires[dependency_name] = dependency_version

    def remove_dependency(self, dependency_name: str):
        """
        Delete dependency from conan profile
        :param dependency_name: dependency name
        :return: None
        """
        del self.__conan_fields.requires[dependency_name]

    @staticmethod
    def create_tmp_profile(build_type):
        """
        Create tmp conan file with default parameters
        TODO change to printer util class
        :return: None
        """
        with open(FULL_PATH_TO_CONAN_FILE, 'w+') as file:
            file.write('from conan import ConanFile\n\n')
            file.write('from conan.tools.cmake import CMake, cmake_layout\n\n')
            file.write('class Conan_profile(ConanFile):\n')
            file.write('     name = "hello"\n')
            file.write('     version = "0.1"\n')
            file.write('     requires = "qt"\n')
            file.write(f'     build = "{build_type}"\n')
            file.write('     generators = "CMakeDeps", "CMakeToolchain"\n')
        print('Creating temporary conan file')

    def __init__(self, is_print_fields: bool):
        self.__conan_fields = _Fields()
        self.__printer = _Conan_printer(is_print_fields)

    def init_profile(self, init_path_profile: str) -> None:
        """
        Initialize data from existing conan file from full path to conan file
        :return: None
        """
        data: dict[str, str] = self.__read_conan_file(init_path_profile)
        data.setdefault(_Conan_proto.PROFILE_NAME, '')
        data.setdefault(_Conan_proto.PROFILE_VER, '0.1')  # also set as default
        data.setdefault(_Conan_proto.PROFILE_REQ, '""')

        self.__conan_fields.name = data.get(_Conan_proto.PROFILE_NAME)
        self.__conan_fields.version = data.get(_Conan_proto.PROFILE_VER)

        self.__conan_fields.requires = _Fields.to_req_dict(data.get(_Conan_proto.PROFILE_REQ))
        self.__conan_fields.generators = _Fields.to_gen_list(data.get(_Conan_proto.PROFILE_GEN))

    def __rewrite_file(self):
        pass

    def is_need_for_rewrite(self):
        """
        Check for file modification time and give result
        :return: bool
        """
        pass

    def change_version(self, new_version: str) -> None:
        """
        Change conan file version
        :param new_version: new version to write
        :return: None
        """
        self.__conan_fields.enter_version(new_version)

    def save_profile(self):
        """
        Print profile in user filesystem
        :return: None
        """
        self.__printer.print(self.__conan_fields)

    @staticmethod
    def __read_conan_file(path_to_read_from: str) -> dict[str, str]:
        """
        Read conan file like text file
        :return: dict with key (conan field type) and value - value :)
        """
        data_to_return: dict[str, str] = dict()
        with open(path_to_read_from, 'r+') as file:
            file_data = file.readlines()  # ignore import directive and class signature TODO can cause a problem due to import directives in real files

            for field_line in file_data:
                field_parameters: list = field_line.split('=', 1)  # field might contain several '=' symbol, and then 1 split
                if len(field_parameters) > 1:

                    field_name = field_parameters[0].strip()  # clear unuseful whitespaces
                    field_value = field_parameters[1].strip()  # clear unuseful whitespaces
                    match field_name:
                        case _Conan_proto.PROFILE_NAME:
                            data_to_return[_Conan_proto.PROFILE_NAME] = field_value

                        case _Conan_proto.PROFILE_VER:
                            data_to_return[_Conan_proto.PROFILE_VER] = field_value

                        case _Conan_proto.PROFILE_GEN:
                            data_to_return[_Conan_proto.PROFILE_GEN] = field_value

                        case _Conan_proto.PROFILE_REQ:
                            data_to_return[_Conan_proto.PROFILE_REQ] = field_value

                        case _Conan_proto.PROFILE_AUT:
                            data_to_return[_Conan_proto.PROFILE_AUT] = field_value

                        case _Conan_proto.PROFILE_OPT:
                            data_to_return[_Conan_proto.PROFILE_OPT] = field_value

                        case _:
                            print(f'Unknown parameter name - "{field_name}" with value - "{field_value}"')
                else:
                    continue

        return data_to_return
