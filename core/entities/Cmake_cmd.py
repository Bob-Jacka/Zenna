from core.entities.CMD import (
    CMD,
    STATIC_CONAN_NAME,
    Build_level
)


class Cmake_cmd(CMD):
    """
    Cmake realization for command line interface
    """

    def remove_dep(self):
        pass

    def __init__(self):
        """
        Ugly looking command line tool
        """
        pass

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

    def refresh_project(self):
        # TODO
        self.__execute()


# Flag adders
def output_flag(source: str, folder_name: str):
    return f'{source} --output-folder={folder_name}'


def profile_flag(source: str, profile_str: str):
    return f'{source} --profile={profile_str}'
