import os
from enum import Enum
from pathlib import Path
from typing import Final

UTIL_VERSIONS: Final[str] = '0.3.3'

STATIC_CONAN_NAME: Final[str] = 'conan'
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
    """
    Custom enum value for build variants
    """
    MIN_DEBUG = 'RelWithDebInfo'
    MIN_SIZE = 'MinSizeRel'
    RELEASE = 'Release'
    DEBUG = 'Debug'

    @staticmethod
    def create_build_variant(string_to_convert: str) -> Build_variants:
        """
        Convert string into build variant
        """
        match string_to_convert:
            case 'debug':
                return Build_variants.MIN_DEBUG
            case 'release':
                return Build_variants.RELEASE
            case 'RelWithDebInfo':
                return Build_variants.MIN_DEBUG
            case 'MinSizeRel':
                return Build_variants.MIN_SIZE
            case _:
                raise Exception(f'Unknown type detected in creating build variant - {string_to_convert}')

    @staticmethod
    def stringify(string_to_convert: Build_variants) -> str:
        """
        Convert build variant to string
        """
        match string_to_convert:
            case Build_variants.MIN_DEBUG:
                return 'RelWithDebInfo'
            case Build_variants.RELEASE:
                return 'release'
            case Build_variants.DEBUG:
                return 'debug'
            case Build_variants.MIN_SIZE:
                return 'MinSizeRel'
            case _:
                raise Exception(f'Unknown type detected in stringification - {string_to_convert}')
