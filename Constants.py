import os
from enum import Enum
from pathlib import Path
from typing import Final

UTIL_VERSIONS: Final[str] = '0.1.3'

STATIC_CONAN_NAME: Final[str] = 'conan'
STATIC_Zenna_NAME: Final[str] = 'config'
STATIC_CMAKE_NAME: Final[str] = 'cmake'
COMMAND_SPLITTER: Final[str] = ' '

OUTER_PATH: Final[str] = Path().cwd().parent.absolute().__str__() + os.path.sep
"""
Absolute outer of the app path
"""

INNER_PATH: Final[str] = Path().cwd().absolute().__str__() + os.path.sep
"""
Inner path to store some useful files
"""

STATIC_ZENNA_FILE_NAME: Final[str] = 'config.zen'
"""
Static name of the zenna file with extension
"""

STATIC_CONAN_FILE_NAME: Final[str] = 'conanfile.py'
"""
Static name of the conan file with extension
"""

FULL_PATH_TO_ZENNA_FILE: Final[str] = OUTER_PATH + STATIC_ZENNA_FILE_NAME
"""
Full path directly to zenna profile file
"""

FULL_PATH_TO_CONAN_FILE: Final[str] = OUTER_PATH + STATIC_CONAN_FILE_NAME
"""
Full path directly to conan profile (s) files
"""


class Build_variants(str, Enum):
    BUILD = 'build'
    RELEASE = 'release'
    DEBUG = 'debug'

    @staticmethod
    def create_build_variant(string_to_convert: str):
        match string_to_convert:
            case 'build':
                return Build_variants.BUILD
            case 'release':
                return Build_variants.RELEASE
            case 'debug':
                return Build_variants.DEBUG
            case _:
                raise Exception(f'Unknown type detected - {string_to_convert}')
