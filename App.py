"""
Entry point into Zenna utility
"""
import sys

from Constants import UTIL_VERSIONS


def print_help():
    print(f'Zenna application - v{UTIL_VERSIONS}')
    print('Available flags in utility:')
    print('"--ui=" can be two variants in this flag (console or web)')


if __name__ == '__main__':
    cli_args = sys.argv  # command line arguments

    if len(cli_args) > 1 and len(cli_args) == 2:
        print(f'Conan wrapper started working, v{UTIL_VERSIONS}')
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
            raise Exception(f'Unknown ui parameter - {cli_param}')
    else:
        print('No valid flags to run in')
        print_help()

print('Bye')  # be polite with user and say goodbye to him
