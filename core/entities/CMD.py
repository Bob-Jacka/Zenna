import abc
from typing import (
    Final,
    Literal
)

STATIC_CONAN_NAME: Final[str] = 'conan'
STATIC_CMAKE_NAME: Final[str] = 'cmake'
COMMAND_SPLITTER: Final[str] = ' '

type Build_level = Literal['release', 'debug']  # which pattern to use for building


class CMD(abc.ABC):
    """
    Abstract command line interface
    """

    @abc.abstractmethod
    def __execute(self):
        pass

    @abc.abstractmethod
    def refresh_project(self):
        pass

    @abc.abstractmethod
    def get_profile(self):
        pass