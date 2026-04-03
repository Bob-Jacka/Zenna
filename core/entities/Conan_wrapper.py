from os import PathLike


class Conan_wrapper:
    """
    Storage class for storing conan data
    """

    def __init__(self):
        pass

    @staticmethod
    def init_with_conan_file(path: str | PathLike):
        pass

    @staticmethod
    def write_conan_file():
        with open(path_to_conan_file, 'w+') as file:
            file.write('from conan import ConanFile\n\n')
            file.write('class HelloConan(ConanFile):\n')
            file.write('     name = "hello"\n')
            file.write('     version = "0.1"\n')
            file.write('     requires = ""\n')
            file.write('     generators = "CMakeDeps", "CMakeToolchain"\n')
