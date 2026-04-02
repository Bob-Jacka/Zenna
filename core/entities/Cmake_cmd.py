from core.entities.CMD import (
    CMD,
    STATIC_CONAN_NAME,
    COMMAND_SPLITTER,
    Build_level
)


class Cmake_cmd(CMD):
    """
    Cmake realization for command line interface
    """
    command_line_builder: list[str]  # inner state of command line
    build_dir: str  # output directory for build files
    profile_lvl: Build_level

    def __init__(self):
        """
        Ugly looking command line tool
        """
        self.command_line_builder = list()

    def first_conan_start(self, build_dir: str, lvl: Build_level):
        """
        Initialize conan build directory
        :param build_dir: name of the build directory
        :param lvl: build level
        :return: None
        """
        self.build_dir = build_dir
        self.profile_lvl = lvl
        self.command_line_builder.append(STATIC_CONAN_NAME)
        self.command_line_builder.append('install . ')
        self.command_line_builder.append(f'-DCMAKE_TOOLCHAIN_FILE={build_dir}/conan_toolchain.cmake')
        self.__execute()

    def check_conan_installed(self):
        """
        Check that conan is installed
        :return: None
        """
        self.command_line_builder += STATIC_CONAN_NAME + ' --version'
        self.__execute()

    def update_dependencies(self):
        """
        Update conan dependencies  list
        :return:
        """
        self.command_line_builder.append(STATIC_CONAN_NAME + '')
        self.command_line_builder.append('install .')
        self.__execute()

    def refresh_project(self):
        self.__execute()

    def get_profile(self):
        self.command_line_builder.append(STATIC_CONAN_NAME + COMMAND_SPLITTER + 'profile ')
        self.__execute()

    def detect_profile(self):
        self.command_line_builder.append(STATIC_CONAN_NAME + COMMAND_SPLITTER + 'profile detect')
        self.__execute()

    def create_new_profile(self):
        self.command_line_builder.append(STATIC_CONAN_NAME + COMMAND_SPLITTER + f'profile new {self.profile_lvl} --detect')
        self.__execute()

    def __build_string(self):
        return str(self.command_line_builder)

    def __execute(self):
        try:
            exec(self.__build_string())
            self.command_line_builder.clear()  # clean command line state after execution
        except Exception as e:
            print(f'An exception occurred during execution command - {e}')


# Flag adders
def output_flag(source: str, folder_name: str):
    return f'{source} --output-folder={folder_name}'


def profile_flag(source: str, profile_str: str):
    return f'{source} --profile={profile_str}'
