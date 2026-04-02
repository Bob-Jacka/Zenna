"""
Main utility logic file
Entry point into application
"""

from os.path import exists

from core.BotLogger import BotLogger
from core.entities.Cmake_cmd import Cmake_cmd
from core.entities.Make_cmd import Make_cmd
from core.entities.Meson_cmd import Meson_cmd
from core.util.Wrappers import log

logger = BotLogger()


def int_user_input(max_variants: int = 5):
    try:
        int_input: int = int(input('>> '))
        if int_input <= max_variants:
            return int_input
        else:
            raise Exception(f'Wrong number - {int_input}')  # or print message into console with logger
    except Exception as e:
        logger.log(f'An exception during user input - {e}')


@log
def decide_build_system():
    while True:
        print('Choose your build system')
        print('1. Cmake')
        print('2. Make')
        print('3. Meson')
        print('4. Exit')
        user_input = int_user_input()
        match user_input:
            case 1:
                logger.log('Choose cmake')
                return Cmake_cmd()
            case 2:
                logger.log('Choose make')
                return Make_cmd()
            case 3:
                logger.log('Choose meson')
                return Meson_cmd()


# Global entities:
cmd = decide_build_system()


#


@log
def main_cycle():
    while True:
        print('Enter number:')
        print('1.Init conan')
        print('2.')
        print('3.')
        print('4. Exit utility')
        us_choice = int_user_input()
        match us_choice:
            case 1:
                pass
            case 2:
                pass


@log
def init_conan():
    pass


@log
def add_dependencies():
    pass


@log
def update_dependencies():
    cmd.update_dependencies()


@log
def show_path_to_config():
    while True:
        print('Enter number:')
        print()
        print()
        print()
        us_choice = int_user_input(3)
        match us_choice:
            case 1:
                pass
            case 2:
                pass
            case _:
                pass


@log
def init_project():
    """
    Init project by searching conan.py file
    :return: None
    """
    if exists('conanfile.py'):  # TODO взять "внешний" путь (вне директории проекта)
        print('Conan file exists')
        return
    else:
        print('Conan file does not exists')
        print('Creating temporary conan file')
        with open('conanfile.py', 'w+') as file:
            file.write('from conan import ConanFile\n\n')
            file.write('class HelloConan(ConanFile):\n')
            file.write('     name = "hello"\n')
            file.write('     version = "0.1"\n')
            file.write('     requires = ""\n')
            file.write('     generators = "CMakeDeps", "CMakeToolchain"\n')


if __name__ == '__main__':
    logger.log('Conan wrapper started working, v0.0.1')
    init_project()
    main_cycle()
    logger.log('Utility finished working')
