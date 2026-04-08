from os import PathLike


class _Fields:
    """
    Simple class for storing conan data
    """
    version: str
    requires: tuple[str]
    generators: tuple[str]

    def enter_version(self, txt_ver: str):
        self.version = f'"{txt_ver}"'

    def enter_requires(self):
        pass

    def enter_generators(self):
        pass


class _Conan_printer:
    """
    Print conan file with given fields parameters
    """

    def __init__(self, out_path: str | PathLike):
        self.path = out_path

    def print(self, fields, file_handler):
        pass


class Conan_wrapper:
    """
    Utility class for dealing with conan
    """
    conan_fields: _Fields

    def __init__(self):
        self.conan_fields.version = '"0.1"'
        self.conan_fields.requires = tuple()
        self.conan_fields.generators = tuple()

    @staticmethod
    def init_with_conan_file(path: str | PathLike):
        """
        Initialize data from existing conan file
        :param path: full path to conan file
        :return: None
        """
        with open(path) as conan_file:
            pass

    def initialize_with_data(self):
        """
        Initialize data with existing conan file. Might be helpful in web to change parameters
        :return:
        """
        pass

    @staticmethod
    def tmp_conan_file():
        """
        Create tmp conan file with default parameters
        :return:
        """
        from App import OUTER_PATH
        with open(OUTER_PATH + 'conanfile.py', 'w+') as file:
            file.write('from conan import ConanFile\n\n')
            file.write('class HelloConan(ConanFile):\n')
            file.write('     name = "hello"\n')
            file.write('     version = "0.1"\n')
            file.write('     requires = ""\n')
            file.write('     generators = "CMakeDeps", "CMakeToolchain"\n')
