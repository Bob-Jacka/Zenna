"""
Entry point into Zenna
"""
import os
from os.path import exists
from pathlib import Path
from typing import Final

from core.UI.Interface import run_web_app
from core.util.Wrappers import log

outer_path: Final[str] = Path().cwd().parent.absolute().__str__() + os.pathsep
"""
Absolute outer of the app path
"""


@log
def init_project():
    """
    Init project by searching conan.py file
    :return: None
    """
    path_to_conan_file = outer_path + 'conanfile.py'  # outer path to conan file, outside Zenna project
    if exists(path_to_conan_file):
        print('Conan file exists')
        return
    else:
        print('Conan file does not exists')
        print('Creating temporary conan file')


def print_help():
    pass


if __name__ == '__main__':
    print('Conan wrapper started working, v0.0.1')
    init_project()
    run_web_app()
    print('Utility finished working')
    print('Bye')  # be polite with user and say goodbye to him
