"""
Entry point into Zenna utility
"""
import sys


def print_help():
    print('Zenna application')
    print('Available flags in utility:')
    print('"--ui=" can be two variants in this flag (console or web)')


if __name__ == '__main__':
    cli_args = sys.argv  # command line arguments

    if len(cli_args) > 1 and len(cli_args) == 2:
        print('Conan wrapper started working, v0.0.3')
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
