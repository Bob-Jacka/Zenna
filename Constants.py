import os
from pathlib import Path
from typing import Final

IN_APP_SETTINGS_NAME: Final[str] = 'app_settings'
"""
Name of the app settings file
"""

OUTER_PATH: Final[str] = Path().cwd().parent.absolute().__str__() + os.path.sep
"""
Absolute outer of the app path
"""

INNER_PATH: Final[str] = Path().cwd().absolute().__str__() + os.path.sep
"""
Inner path to store some useful files
"""

STATIC_CONAN_FILE_NAME: Final[str] = 'conanfile.py'
"""
Static name of the conan file, also may be with .txt extension
"""

STATIC_CONAN_NAME: Final[str] = 'conan'
STATIC_CMAKE_NAME: Final[str] = 'cmake'
COMMAND_SPLITTER: Final[str] = ' '
