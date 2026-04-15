import abc

from Constants import (
    STATIC_CONAN_NAME,
    COMMAND_SPLITTER,
    Build_variants
)


class CMD(abc.ABC):
    """
    Abstract command line interface, also wraps conan specific functions
    """
    command_line_builder: list[str] = list()  # inner state of command line
    profile_lvl: Build_variants  # level of profile

    def __execute(self):
        """
        Execute command and clear state
        :return: None
        """
        try:
            print(f'Command arguments: {self.command_line_builder.__str__()}')
            exec(str(self.command_line_builder))
            self.command_line_builder.clear()  # clean command line state after execution
        except Exception as e:
            print(f'An exception occurred during execution command - {e}')

    def get_profile(self):
        """
        Prints conan path to profile
        :return: None
        """
        self.command_line_builder.append(STATIC_CONAN_NAME + COMMAND_SPLITTER + 'profile ')
        self.__execute()

    def detect_profile(self):
        """
        Detect conan profile
        :return: None
        """
        self.command_line_builder.append(STATIC_CONAN_NAME + COMMAND_SPLITTER + 'profile detect')
        self.__execute()

    def create_new_profile(self):
        """
        Create new conan profile
        :return: None
        """
        self.command_line_builder.append(STATIC_CONAN_NAME + COMMAND_SPLITTER + f'profile new {self.profile_lvl} --detect')
        self.__execute()

    def update_dependencies(self):
        """
        Update conan dependencies list
        :return: None
        """
        self.command_line_builder.append(STATIC_CONAN_NAME + '')
        self.command_line_builder.append('install')
        self.command_line_builder.append(' .')
        self.__execute()

    def check_conan_installed(self):
        """
        Check that conan is installed
        :return: None
        """
        self.command_line_builder.append(STATIC_CONAN_NAME + ' --version')
        self.__execute()

    # Flag adders:
    @staticmethod
    def output_flag(source: str, folder_name: str):
        return f'{source} --output-folder={folder_name}'

    @staticmethod
    def profile_flag(source: str, profile_str: str):
        return f'{source} --profile={profile_str}'

    @abc.abstractmethod
    def refresh_project(self):
        pass

    @abc.abstractmethod
    def first_conan_start(self, build_dir: str, lvl: Build_variants):
        pass
