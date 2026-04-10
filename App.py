"""
Entry point into Zenna utility
"""
import sys
from os.path import exists

from Constants import (
    OUTER_PATH,
    STATIC_CONAN_FILE_NAME
)
from core.entities.Conan_profile import Conan_profile
from core.util.Utiltilies import str_user_input
from core.util.Wrappers import log


@log
def init_project():
    """
    Init project by searching conan.py file
    :return: None
    """
    path_to_conan_file = OUTER_PATH + STATIC_CONAN_FILE_NAME  # outer path to conan file, outside Zenna project
    if exists(path_to_conan_file):
        print(f'Conan file exists on path "{path_to_conan_file}"')
        return
    else:
        print('Conan file does not exists')
        print('Would you like to create temporary conan profile? (yes / y)')
        while True:
            user_input = str_user_input(True)
            if user_input == 'yes' or user_input == 'y':
                Conan_profile.tmp_conan_file()
                break
            else:
                break


def print_help():
    print('Zenna application')
    print('Available flags in utility:')
    print('"--ui=" can be two variants in this flag (console or web)')


if __name__ == '__main__':
    cli_args = sys.argv  # command line arguments

    if len(cli_args) > 1 and len(cli_args) == 2:
        print('Conan wrapper started working, v0.0.3')
        init_project()
        split_str = cli_args[1].split('=')
        # cli_flag_name = split_str[0].strip() # for future use
        cli_param = split_str[1].strip()

        if cli_param == 'web':
            from core.UI.Frontend import Web_interface

            interface = Web_interface()
            interface.run_app()

        elif cli_param == 'console':
            from core.UI.Frontend import Console_interface

            interface = Console_interface()
            interface.run_app()
        else:
            raise Exception(f'Unknown parameter - {cli_param}')
    else:
        print_help()

print('Bye')  # be polite with user and say goodbye to him
