"""
Entry point into Zenna
"""
import os
import sys
from os.path import exists
from pathlib import Path
from typing import Final

from core.util.Wrappers import log

OUTER_PATH: Final[str] = Path().cwd().parent.absolute().__str__() + os.path.sep
"""
Absolute outer of the app path
"""

STATIC_CONAN_FILE_NAME: Final[str] = 'conanfile.py'
"""
Static name of the conan file, also may be with .txt extension
"""


@log
def init_project():
    """
    Init project by searching conan.py file
    :return: None
    """
    from core.entities.Conan_wrapper import Conan_wrapper
    path_to_conan_file = OUTER_PATH + STATIC_CONAN_FILE_NAME  # outer path to conan file, outside Zenna project
    if exists(path_to_conan_file):
        print(f'Conan file exists on path "{path_to_conan_file}"')
        return
    else:
        print('Conan file does not exists')
        print('Creating temporary conan file')
        Conan_wrapper.tmp_conan_file()


def print_help():
    print('Zenna application')
    print('Available flags in utility:')
    print('"--ui=" can be two variants in this flag (console or web)')


if __name__ == '__main__':
    cli_args = sys.argv  # command line arguments

    if len(cli_args) > 1 and len(cli_args) == 2:
        print('Conan wrapper started working, v0.0.2')
        init_project()
        split_str = cli_args[1].split('=')
        # cli_flag_name = split_str[0].strip() # for future use
        cli_param = split_str[1].strip()
        if cli_param == 'web':
            from core.UI.Interface import Web_interface

            interface = Web_interface()
            interface.run_app()

        elif cli_param == 'console':
            from core.UI.Interface import Console_interface

            interface = Console_interface()
            interface.run_app()
        else:
            raise Exception(f'Unknown parameter - {cli_param}')
    else:
        print_help()

# be polite with user and say goodbye to him
